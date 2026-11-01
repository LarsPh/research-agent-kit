#!/usr/bin/env python3
"""Check that a task brief has every required field before a job or sub-agent is launched.

A brief is a Markdown file whose top lines are `key: value` fields (template in references/dispatch.md).
Required everywhere: line, why, goal, outputs, done_when, budget, time_limit. A project adds its own required
keys, one per line, in <run dir>/brief_fields.txt (for example `eval_frame_format`).
`budget` and `time_limit` must contain a number: "1.5x the last run" is not a limit.

jobctl.py launch runs this check itself, so no hook is needed for jobs started through jobctl.
Usage: check_brief.py BRIEF.md   (exit 0 complete, 1 incomplete)
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lrx_common as lc  # noqa: E402

REQUIRED = ("line", "why", "goal", "outputs", "done_when", "budget", "time_limit")
NUMERIC = ("budget", "time_limit")
FIELD = re.compile(r"^\s*[-*]?\s*`?([A-Za-z_][\w-]*)`?\s*:\s*(.*)$")


def fields(text):
    found = {}
    for line in text.splitlines():
        match = FIELD.match(line)
        if match:
            found.setdefault(match.group(1).lower(), match.group(2).strip())
    return found


def required_keys(root=None):
    extra = (root or lc.run_dir()) / "brief_fields.txt"
    keys = list(REQUIRED)
    if extra.exists():
        keys += [k.strip().lower() for k in extra.read_text(encoding="utf-8").splitlines()
                 if k.strip() and not k.startswith("#")]
    return keys


def brief_problems(path, root=None):
    path = Path(path)
    if not path.is_file():
        return [f"brief not found: {path}"]
    have = fields(path.read_text(encoding="utf-8"))
    problems = [f"missing {key}" for key in required_keys(root) if not have.get(key)]
    for key in NUMERIC:
        if have.get(key) and not re.search(r"\d", have[key]):
            problems.append(f"{key} has no number: {have[key]!r}")
    return problems


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__)
        return 2
    problems = brief_problems(argv[0])
    print("\n".join(problems) if problems else "brief complete")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
