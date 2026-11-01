#!/usr/bin/env python3
"""Claude Code Stop hook: in an unattended run, do not let the agent stop while a GPU idles for no reason.

Acts only when <run dir>/UNATTENDED exists (create it when you leave, delete it when you are back), so it
never interrupts a conversation you are in. Then, when the agent tries to end its turn:

- stop allowed: no idle GPU; or an open question with "blocks": true and no ready task; or
  <run dir>/idle_ok.json says why idling is right, until a time not yet passed;
- stop refused with a short reason: a finished job is not handled; an idle GPU has a ready task; or an idle
  GPU has no ready task and no recorded reason.

A ready task must name its line and why (queue.json), so padding the queue does not satisfy the hook.
Loop guards: nothing happens when stop_hook_active is true, and at most MAX_PER_HOUR refusals per hour.
Any error exits 0 silently: this hook must never trap the session or eat a message.
"""

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lrx_common as lc  # noqa: E402
import jobctl  # noqa: E402

NAME = "queue_check"
MAX_PER_HOUR = 2


def recent_blocks(root):
    path = root / "hooks.log"
    if not path.exists():
        return 0
    cutoff = lc.now() - dt.timedelta(hours=1)
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[1] == NAME and parts[2] == "block" and lc.parse_iso(parts[0]) >= cutoff:
            count += 1
    return count


def idle_ok(root):
    note = lc.load_json(root / "idle_ok.json", None)
    until = lc.parse_iso(note.get("until")) if note else None
    return bool(note and note.get("reason") and until and until > lc.now())


def pending_work(root):
    """What the agent should be doing now, or None when stopping is fine. Shared with resume_check.py."""
    unhandled = []
    for meta in jobctl.jobs(root):
        if meta and not meta.get("handled"):
            info = jobctl.classify(root, meta)
            if info["state"] in jobctl.FINISHED:
                unhandled.append(jobctl.describe(meta, info))
    if unhandled:
        return ("Finished jobs are not handled yet: " + "; ".join(unhandled[:3]) +
                ". Record each result, then run jobctl.py handled <id>.")
    idle = lc.idle_gpus()
    if not idle:
        return None
    ready = lc.ready_tasks(root)
    if ready:
        return (f"GPU {idle} idle and ready task {ready[0]['id']} ({ready[0]['line']}: {ready[0]['why']}). "
                "Launch it with jobctl.py launch.")
    blocking = [q for q in lc.open_questions(root) if q.get("blocks") is True]
    if blocking or idle_ok(root):
        return None
    soft = [q for q in lc.open_questions(root) if q.get("blocks") is not True]
    hint = (f" Open question {soft[0].get('id')} is blocks: false; proceed with its default "
            f"({soft[0].get('default')!r}).") if soft else ""
    return (f"GPU {idle} idle and no ready task in queue.json (each needs line and why).{hint} Queue the next "
            "useful task; if nothing is worth running, write idle_ok.json with reason and until, or record a "
            "blocks: true question.")


def decide(event, root):
    """Return a refusal reason, or None to let the agent stop."""
    if not (root / "UNATTENDED").exists() or event.get("stop_hook_active"):
        return None
    if recent_blocks(root) >= MAX_PER_HOUR:
        return None
    return pending_work(root)


def main():
    try:
        event = json.load(sys.stdin)
        root = lc.run_dir()
        reason = decide(event, root)
        lc.log_hook(NAME, "block" if reason else "allow", (reason or "")[:120], root)
        if reason:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": reason}}))
    except Exception:  # noqa: BLE001 - a broken hook must never block the session
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
