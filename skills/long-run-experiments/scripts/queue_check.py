#!/usr/bin/env python3
"""Claude Code Stop hook: in an unattended run, do not let the agent stop while a GPU idles for no reason.

Acts only when <run dir>/UNATTENDED exists (create it when you leave, delete it when you are back), so it
never interrupts a conversation you are in. Then, when the agent tries to end its turn:

- stop allowed: the final message asks the user something (QUESTION_MARKERS), so it stays the last message
  the user sees; no idle GPU; an open question with "blocks": true and no ready task; or
  <run dir>/idle_ok.json says why idling is right, until a time not yet passed;
- stop refused with a short reason: a finished job is not handled; an idle GPU has a ready task; or an idle
  GPU has no ready task and no recorded reason.

A ready task must name its line, why, decision_if and dedup_checked (queue.json); the hook never asks for a
number of tasks, so it does not push the agent to invent work. Tasks created within PADDING_MIN after a
refusal are listed by `queue_check.py --suspects` for the user to review.
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
PADDING_MIN = 5
QUESTION_MARKERS = ("needs input", "❓", "待决问题", "需要你决定")


def asks_user(event):
    """True when this turn's final message puts a question to the user (Stop input: last_assistant_message)."""
    text = (event.get("last_assistant_message") or "").lower()
    return any(m in text for m in QUESTION_MARKERS)


def block_times(root):
    path = root / "hooks.log"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[1] == NAME and parts[2] == "block":
            t = lc.parse_iso(parts[0])
            if t:
                out.append(t)
    return out


def padding_suspects(root):
    """Queued tasks created within PADDING_MIN minutes after a refusal: possibly made up to satisfy the hook."""
    blocks = block_times(root)
    out = []
    for task in lc.queue(root):
        created = lc.parse_iso(task.get("created"))
        if created and any(b <= created <= b + dt.timedelta(minutes=PADDING_MIN) for b in blocks):
            out.append(task)
    return out


def recent_blocks(root):
    cutoff = lc.now() - dt.timedelta(hours=1)
    return sum(1 for t in block_times(root) if t >= cutoff)


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
                ". Record each result, then run jobctl.py handled <id>." + restate_hint(root))
    idle = lc.idle_gpus()
    if not idle:
        return None
    ready = lc.ready_tasks(root)
    if ready:
        return (f"GPU {idle} idle and ready task {ready[0]['id']} ({ready[0]['line']}: {ready[0]['why']}). "
                "Launch it with jobctl.py launch." + restate_hint(root))
    blocking = [q for q in lc.open_questions(root) if q.get("blocks") is True]
    if blocking or idle_ok(root):
        return None
    soft = [q for q in lc.open_questions(root) if q.get("blocks") is not True]
    hint = (f" Open question {soft[0].get('id')} is blocks: false; proceed with its default "
            f"({soft[0].get('default')!r}).") if soft else ""
    return (f"GPU {idle} idle and no ready task in queue.json.{hint} Queue a task only if it passes the four "
            "questions in questions-and-queue.md (ledger row that existed before now, decision_if, dedup "
            "checked, prerequisites met). If nothing passes, write idle_ok.json with reason and until; an idle "
            "GPU is cheaper than a duplicate run." + restate_hint(root))


def restate_hint(root):
    blocking = [q for q in lc.open_questions(root) if q.get("blocks") is True]
    if not blocking:
        return ""
    return (" Your final message must restate every open blocking question: "
            + "; ".join(f"{q.get('id')}: {str(q.get('question', ''))[:80]}" for q in blocking[:3]))


def decide(event, root):
    """Return a refusal reason, or None to let the agent stop."""
    if not (root / "UNATTENDED").exists() or event.get("stop_hook_active"):
        return None
    if asks_user(event):
        return None  # keep the question as the last message; do the queue work at the start of the next turn
    if recent_blocks(root) >= MAX_PER_HOUR:
        return None
    return pending_work(root)


def main():
    try:
        root = lc.run_dir()
        if sys.argv[1:] == ["--suspects"]:
            for task in padding_suspects(root):
                print(f"{task.get('id')}\tcreated {task.get('created')}\t{task.get('line')}: {task.get('why')}")
            return 0
        event = json.load(sys.stdin)
        reason = decide(event, root)
        detail = ("asks_user " if asks_user(event) else "") + (reason or "")[:120]
        lc.log_hook(NAME, "block" if reason else "allow", detail, root)
        if reason:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": reason}}))
    except Exception:  # noqa: BLE001 - a broken hook must never block the session
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
