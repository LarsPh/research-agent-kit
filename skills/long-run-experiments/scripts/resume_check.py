#!/usr/bin/env python3
"""Cron backstop: wake the agent when there is work and it has gone quiet. No model call while waiting.

Run every few minutes from cron. It re-reads state each time instead of waiting for an event, so a missed
wake-up is caught on the next tick. It wakes the agent only when all hold:

1. <run dir>/UNATTENDED exists;
2. there is work (same rule as the Stop hook): an unhandled finished job, or an idle GPU with a ready task
   or with no recorded reason to idle;
3. the agent has been quiet for --quiet-min: the newest file matching --activity is that old;
4. the last wake-up was at least --cooldown-min ago (lock in <run dir>/resume.json).

The wake-up runs --resume-cmd through the shell with {reason} replaced (shell-quoted), for example
  tmux send-keys -t agent {reason} Enter
  claude -p --resume SESSION_ID {reason}
so it works with any agent that can be resumed from a command line. --dry-run prints instead.
"""

import argparse
import glob
import os
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lrx_common as lc  # noqa: E402
from queue_check import pending_work  # noqa: E402

NAME = "resume_check"


def quiet_minutes(pattern):
    paths = [p for p in glob.glob(os.path.expanduser(pattern), recursive=True) if os.path.isfile(p)]
    if not paths:
        return None
    newest = max(os.path.getmtime(p) for p in paths)
    return (lc.now().timestamp() - newest) / 60


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--activity", required=True, help="glob of files the agent touches, e.g. its transcript")
    parser.add_argument("--resume-cmd", required=True, help="shell command; {reason} is replaced, quoted")
    parser.add_argument("--quiet-min", type=float, default=15)
    parser.add_argument("--cooldown-min", type=float, default=30)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    root = lc.run_dir()
    if not (root / "UNATTENDED").exists():
        return 0
    reason = pending_work(root)
    if not reason:
        return 0
    quiet = quiet_minutes(args.activity)
    if quiet is not None and quiet < args.quiet_min:
        return 0
    lock = lc.load_json(root / "resume.json", {})
    last = lc.parse_iso(lock.get("last"))
    if last and (lc.now() - last).total_seconds() / 60 < args.cooldown_min:
        return 0
    message = f"Long-run check: {reason} Run jobctl.py watch and continue with long-run-experiments."
    command = args.resume_cmd.replace("{reason}", shlex.quote(message))
    if args.dry_run:
        print(command)
        return 0
    lc.save_json(root / "resume.json", {"last": lc.iso(), "reason": reason})
    lc.log_hook(NAME, "wake", reason[:120], root)
    return subprocess.run(command, shell=True, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
