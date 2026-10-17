#!/usr/bin/env python3
"""Record which files each review lane opened, and summarize it for the report's Coverage section.

hook:    Claude Code PostToolUse hook for Read|Grep|Glob. Reads the hook JSON on stdin and appends one line
         to <log dir>/<session_id>.jsonl. Never blocks the tool and never writes inside the target repo.
summary: print the files each agent opened, and the target files no agent opened.

Log dir: $MULTILANE_REVIEW_LOG_DIR, else <system temp>/multilane-review.
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path


def log_dir():
    return Path(os.environ.get("MULTILANE_REVIEW_LOG_DIR") or Path(tempfile.gettempdir()) / "multilane-review")


def hook():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool_input = event.get("tool_input") or {}
    record = {
        "time": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "agent": event.get("agent_type") or event.get("agent_id") or "main",
        "tool": event.get("tool_name"),
        "cwd": event.get("cwd"),
        "path": tool_input.get("file_path") or tool_input.get("path"),
        "pattern": tool_input.get("pattern"),
    }
    session = event.get("session_id") or "unknown-session"
    try:
        directory = log_dir()
        directory.mkdir(parents=True, exist_ok=True)
        with open(directory / f"{session}.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as error:
        print(f"log_coverage: could not write log: {error}", file=sys.stderr)
    return 0


def relative(path, root):
    if not path:
        return None
    p = Path(path)
    if not p.is_absolute() and root:
        p = Path(root) / p
    try:
        return p.resolve().relative_to(Path(root).resolve()).as_posix()
    except (ValueError, OSError):
        return p.as_posix()


def target_files(repo, ref_range):
    if ref_range:
        args = ["diff", "--name-only", ref_range]
    else:
        args = ["ls-files"]
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed in {repo}: {result.stderr.strip()}")
    return [line for line in result.stdout.splitlines() if line]


def summary(args):
    log = Path(args.log) if args.log else max(log_dir().glob("*.jsonl"), key=os.path.getmtime, default=None)
    if log is None or not log.exists():
        raise SystemExit("no coverage log found; pass --log")
    opened = defaultdict(set)
    searched = defaultdict(set)
    for line in log.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        path = relative(record.get("path"), args.repo)
        if record.get("tool") == "Read" and path:
            opened[record["agent"]].add(path)
        elif path:
            searched[record["agent"]].add(path)

    print(f"Coverage log: {log}")
    for agent in sorted(set(opened) | set(searched)):
        print(f"\n[{agent}] opened {len(opened[agent])} files")
        for path in sorted(opened[agent]):
            print(f"  {path}")
        if searched[agent]:
            print(f"  searched under: {', '.join(sorted(searched[agent]))}")

    targets = target_files(args.repo, args.range)
    read_anywhere = set().union(*opened.values()) if opened else set()
    unread = [path for path in targets if path not in read_anywhere]
    print(f"\nTarget files: {len(targets)}; opened by no agent: {len(unread)}")
    for path in unread:
        print(f"  {path}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hook", help="PostToolUse hook entry point (reads JSON on stdin)")
    s = sub.add_parser("summary", help="summarize a coverage log")
    s.add_argument("--repo", required=True, help="target repository root")
    s.add_argument("--range", help="ref range under review, e.g. main...feature; default: all tracked files")
    s.add_argument("--log", help="coverage log; default: newest log in the log dir")
    args = parser.parse_args()
    return hook() if args.command == "hook" else summary(args)


if __name__ == "__main__":
    sys.exit(main())
