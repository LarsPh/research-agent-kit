#!/usr/bin/env python3
"""Block until enough GPUs are idle, then exit, so a background run of this script wakes the agent.

Polls nvidia-smi locally (no model calls, no tokens). Run it as a background command; Claude Code tells
the agent when it exits. Background commands in unattended runs are capped at 2 hours, so the default
timeout is 110 minutes: exit 3 then means "still busy", and the cron resume_check.py remains the backstop.

exit 0: prints the idle GPU indices · exit 3: timed out
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lrx_common as lc  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--max-mem-mb", type=int, default=1000)
    parser.add_argument("--max-util", type=int, default=5)
    parser.add_argument("--interval", type=float, default=60)
    parser.add_argument("--timeout-min", type=float, default=110)
    args = parser.parse_args(argv)
    deadline = time.monotonic() + args.timeout_min * 60
    while True:
        idle = lc.idle_gpus(args.max_mem_mb, args.max_util)
        if len(idle) >= args.count:
            print("idle GPUs: " + ",".join(map(str, idle)))
            return 0
        if time.monotonic() + args.interval > deadline:
            print(f"timed out; idle GPUs now: {idle}")
            return 3
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
