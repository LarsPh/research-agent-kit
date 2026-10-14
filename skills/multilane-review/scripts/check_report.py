#!/usr/bin/env python3
"""Claude Code Stop hook: keep the agent working until a multilane review report is complete.

Acts only when the final message looks like a multilane report (it has a "## Bugs" heading). Then it
requires the four report sections, a status of confirmed / plausible / rejected on each of the top 8 bug
rows, a quoted line on every rejected row, and a Coverage section that says the review was static.
A missing item blocks the stop with the list of gaps as the reason, at most MAX_BLOCKS times per session,
so a report the agent cannot fix never traps it.

Run without stdin hook JSON to check a saved report: check_report.py --file report.md
"""

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

SECTIONS = ("## Bugs", "## End-to-End and Hygiene", "## Design", "## Coverage")
STATUSES = {"confirmed", "plausible", "rejected"}
STATUS_COLUMN = 4  # | # | file:line | issue | lane | status | proof path |
MAX_BLOCKS = 2


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if isinstance(part, dict))
    if isinstance(content, dict):
        return text_of(content.get("content") or content.get("text"))
    return ""


def last_assistant_text(event):
    if event.get("last_assistant_message"):
        return text_of(event["last_assistant_message"])
    path = event.get("transcript_path")
    if not path or not Path(path).exists():
        return ""
    last = ""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = entry.get("message") or {}
        if entry.get("type") == "assistant" or message.get("role") == "assistant":
            text = text_of(message.get("content"))
            if text.strip():
                last = text
    return last


def section(report, heading):
    start = report.find(heading)
    if start < 0:
        return ""
    end = report.find("\n## ", start + len(heading))
    return report[start : end if end >= 0 else len(report)]


def problems(report):
    found = [f"missing section {name!r}" for name in SECTIONS if name not in report]

    rows = []
    for line in section(report, "## Bugs").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not line.strip().startswith("|") or len(cells) <= STATUS_COLUMN:
            continue
        if cells[0] in {"#", ""} or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(cells)
    if not rows:
        found.append("the Bugs table has no rows (write 'none found' as a row if there are none)")
    for cells in rows[:8]:
        status = cells[STATUS_COLUMN].lower().strip("*` ")
        if status not in STATUSES and "none" not in " ".join(cells).lower():
            found.append(f"bug {cells[0]}: status {cells[STATUS_COLUMN]!r} is not confirmed/plausible/rejected")
        if status == "rejected" and not re.search(r"`[^`]+`|「[^」]+」|\"[^\"]+\"", " ".join(cells)):
            found.append(f"bug {cells[0]}: rejected without quoting the line that handles it")

    if "static" not in section(report, "## Coverage").lower():
        found.append("Coverage does not state that the review was static")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", help="check a saved report instead of reading hook JSON on stdin")
    args = parser.parse_args()

    if args.file:
        found = problems(Path(args.file).read_text(encoding="utf-8"))
        print("\n".join(found) or "report complete")
        return 1 if found else 0

    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    report = last_assistant_text(event)
    if "## Bugs" not in report:
        return 0
    found = problems(report)
    counter = Path(tempfile.gettempdir()) / "multilane-review" / f"{event.get('session_id', 'unknown')}.blocks"
    blocks = int(counter.read_text()) if counter.exists() else 0
    if found and blocks < MAX_BLOCKS:
        counter.parent.mkdir(parents=True, exist_ok=True)
        counter.write_text(str(blocks + 1))
        reason = "The multilane review report is incomplete:\n- " + "\n- ".join(found)
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
