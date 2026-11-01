# Questions and the Queue

## Two ways a run stalls on a question

1. **A dialog nobody answers.** A tool that waits for a click (Claude Code's AskUserQuestion, a
   permission prompt, the equivalent in other agents) stops the session until someone is there. For
   unattended sessions, remove the tool rather than reacting to it: start with
   `--disallowedTools AskUserQuestion`, allow the commands the night needs, and deny dangerous ones in the
   permission settings. In `claude -p` runs without a permission host, AskUserQuestion is not offered at all.
   When the user is present, keep the dialogs and add a notification (a `PermissionRequest` hook that
   plays a sound or sends a push) so a waiting dialog is noticed.
2. **A question that was not worth stopping for.** The agent asks in chat and ends its turn although it
   could have continued with a sensible default.

## Classify every question

| `blocks` | When | What the agent does |
|---|---|---|
| `true` | irreversible action (delete data, deploy, publish, push to a shared place); spending beyond the budget; changing the research direction or the claim | stop that line only; keep other lines running; notify the user |
| `false` | everything else: naming, which of two reasonable settings, extra comparisons, formatting | act on `default` now; report "did X by default, tell me to change it" |

Write the default as an action, not "wait". If you cannot name a safe default, the question blocks.

## The queue

Pressure to keep GPUs busy produces both the best and the worst tasks of a night. In one 15-hour run a hook
that demanded at least three queued tasks fired about ten times: of six tasks added under it, two repeated
delivered work, one re-diagnosed a retired idea, one only unified formats, one was launched before its
input existed, and two were the most valuable diagnostics of the day. Counting tasks cannot tell these
apart, so the hook never counts; the agent answers four questions before queueing.

### Four questions before queueing

If any answer is missing, the task is padding: write `idle_ok.json` instead.

1. **Which line and which next step?** Point at the ledger row it serves; the row existed before the hook
   fired. A reason written after the refusal is padding.
2. **Which decision does the result change?** Write it as `decision_if`: "if A, do X; if B, do Y".
   "More complete material" or "consistent formatting" changes no decision.
3. **Deduplicated?** Search `dead_ends.md`, the ledger and recent output folders for the same scene or
   question; set `dedup_checked: true` only after that search.
4. **Prerequisites met?** If an upstream result is still coming (the next hop of a chain, a running
   experiment), queue it as `blocked` and wait instead of launching a version that is stale on arrival.

### Signs that a real task is missing

- A line in the ledger is marked stalled, and its next step can run now (no user, no upstream wait).
- The user's top priority has nothing running while a GPU is idle.
- A new unexplained observation appeared, and no diagnostic for it is queued.

### Rules

- The Stop hook and cron ignore tasks without `line`, `why`, `decision_if` and `dedup_checked: true`.
- Order by the ledger's priorities, not by what is easiest to run.
- Record `created` on each task; list `queue_check.py --suspects` in the next report so the user can
  review tasks queued right after a refusal.

## When to stop a line

After several consecutive runs on one line without a gain beyond noise, stop queueing it and record a
`blocks: true` direction question with the evidence. Compute spent past that point rarely changes the
answer.
