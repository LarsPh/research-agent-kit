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

- A ready task names its `line` and `why` (the priority or table cell it serves). The Stop hook and cron
  ignore tasks without them, so padding the queue does not keep the agent busy.
- Before queueing, check `dead_ends.md` and the ledger for the same idea.
- Order by the ledger's priorities, not by what is easiest to run.
- When nothing is worth running, write `idle_ok.json` with the reason and an expiry instead of inventing
  diagnostic jobs.

## When to stop a line

After several consecutive runs on one line without a gain beyond noise, stop queueing it and record a
`blocks: true` direction question with the evidence. Compute spent past that point rarely changes the
answer.
