#!/usr/bin/env python3
"""Claude Code SessionStart hook (matcher "compact|resume"): re-inject the run's state from disk.

Compaction summarizes the conversation and can drop details. This prints, as plain text that Claude Code
adds to context, the facts that live in the run directory: job states, ready tasks, open questions with
their blocks/default, the latest decisions, and where the dead-end log is. It reads files only, so it is
always current and costs nothing between compactions. Output stays under MAX_CHARS so it is never cut.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lrx_common as lc  # noqa: E402
import jobctl  # noqa: E402

MAX_CHARS = 1500


def tail_items(path, n):
    if not path.exists():
        return []
    items = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip().startswith("- ")]
    return items[-n:]


def render(root):
    out = ["[long-run state from the run directory: background, not the user's words; answer the user first]"]
    mode = "unattended" if (root / "UNATTENDED").exists() else "attended"
    out.append(f"mode: {mode}")
    for meta in jobctl.jobs(root):
        if meta:
            info = jobctl.classify(root, meta)
            if not (meta.get("handled") and info["state"] in jobctl.FINISHED):
                out.append("job " + jobctl.describe(meta, info))
    ready = lc.ready_tasks(root)
    if ready:
        out.append("ready: " + ", ".join(f"{t['id']} ({t['line']})" for t in ready[:5]))
    for q in lc.open_questions(root)[:5]:
        out.append(f"question {q.get('id')} blocks={q.get('blocks')} default={q.get('default')!r}: "
                   f"{str(q.get('question', ''))[:120]}")
    decisions = tail_items(root / "decisions.md", 5)
    if decisions:
        out.append("latest decisions:")
        out += [f"  {d[:160]}" for d in decisions]
    dead = root / "dead_ends.md"
    if dead.exists():
        out.append(f"dead ends: {len(tail_items(dead, 10_000))} recorded in {dead}; check before queueing")
    text = "\n".join(out)
    return text if len(text) <= MAX_CHARS else text[: MAX_CHARS - 20] + "\n[cut; run jobctl.py status]"


def main():
    try:
        root = lc.run_dir()
        if root.exists():
            print(render(root))
            lc.log_hook("context_inject", "inject", "", root)
    except Exception:  # noqa: BLE001 - never break session start
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
