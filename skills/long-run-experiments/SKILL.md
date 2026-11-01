---
name: long-run-experiments
description: Runs research experiments unattended for hours or overnight without stalling, losing track, or reporting too early. Launches jobs detached from the agent session with per-job done markers, keeps GPUs busy only with tasks that name their line and reason, turns questions into blocking or default-and-continue, resumes from disk after compaction or idle periods, and gates conclusions. Use when the user leaves experiments running overnight or for hours, when jobs or sub-agents must keep going without the user, or when a long run stalled, idled, or repeated work. Triggers include 长跑, 挂一晚上, 自主实验, 夜间实验, GPU 空闲, 看门狗.
---

# Long-Run Experiments

A long run fails in quiet ways: a job dies with the session that started it, a stale log looks like
success, a question waits for an answer nobody is there to give, a GPU idles, or a single-seed result
becomes a conclusion. The cure is to keep every fact on disk under the run directory (`runs/`, or
`$LONGRUN_DIR`) and let small scripts read it, so nothing depends on the agent's memory.

This skill covers the run itself. Plan with `research-evidence-loop`, implement with
`research-task-implementation`, keep the line's ledger with `frontline-ledger`, and diagnose wrong-looking
images with `graphics-debug`.

## Before the User Leaves

1. Set up `runs/` as in [state-files.md](references/state-files.md): `queue.json`, `questions.json`,
   `decisions.md`, `dead_ends.md`. Add project-specific brief fields to `runs/brief_fields.txt`.
2. Turn off tools that wait for a click: start the session with `--disallowedTools AskUserQuestion`, and
   put the commands the night needs in the permission allow list and dangerous ones in the deny list, so no
   prompt appears with nobody to answer it.
3. Create `runs/UNATTENDED`. The Stop hook and the cron backstop act only while it exists.
4. Run one small known-good job first (smallest config, known result) to prove the environment works.

## Every Cycle

Copy this checklist and work through it each time you wake or finish a step:

```
Long-run cycle:
- [ ] 1. jobctl.py watch: handle every finished, failed, crashed or stalled job
- [ ] 2. Record each result; run the report gate before calling anything a conclusion
- [ ] 3. Update the ledger and dead_ends.md; jobctl.py handled <id>
- [ ] 4. Answer or re-default open questions; blocking ones stop only their own line
- [ ] 5. Queue next tasks (line + why), checking dead_ends.md first
- [ ] 6. Launch onto idle GPUs with jobctl.py launch, one brief per job
- [ ] 7. Nothing to run: write idle_ok.json with the reason, or wait_for_gpu.py in the background
```

### Launch only through jobctl

Write a brief from [dispatch.md](references/dispatch.md), then
`scripts/jobctl.py launch --id <id> --brief <brief> --gpu <n> -- <command>`. It refuses an incomplete brief,
starts the job in tmux or its own session so it outlives the agent or sub-agent that launched it, and
writes `status/<id>.done` with a per-job token and the exit code when the command ends. Never start long
jobs with a bare `&` or from a foreground sub-agent's background command: those stop when that sub-agent
ends. Details in [job-lifecycle.md](references/job-lifecycle.md).

### Ask without stalling

Every question goes into `questions.json` with `blocks`, `default` and `line`. Only three kinds block: an
irreversible action, spending beyond the budget, or a change of research direction. For anything else, act
on the default now and say so in the report ("did X by default; tell me to change it"). A blocking question
stops only its line. Rules and examples in [questions-and-queue.md](references/questions-and-queue.md).

### Report only what the evidence carries

Before a result changes a ranking, a decision or a claim, pass [report-gate.md](references/report-gate.md):
images inspected and paths written, known confounders ruled out, a gain inside the noise band confirmed on a
second seed, a single scene labelled as such. Otherwise write "preliminary". After N runs on one line with
no gain, stop that line and ask a blocking direction question instead of burning more compute.

### Write down what failed

Append every abandoned approach to `dead_ends.md` (what, result, why dropped). Read it before queueing:
repeating a dead end is the most common waste in long runs.

## Waking Up Without Polling

Waiting costs no tokens when nothing model-side waits:

- In the session: run `scripts/wait_for_gpu.py` as a background command; the agent is told when it exits.
- Outside the session: cron runs `scripts/resume_check.py` every few minutes. It checks the state files,
  not events, so a missed wake-up is caught on the next tick, and wakes a quiet agent with your resume
  command. Setup in [resume.md](references/resume.md).

## Optional Claude Code Hooks

Two hooks, loaded only for the experiment session: a Stop hook (`queue_check.py`) that refuses to stop
while a GPU idles for no recorded reason, and a SessionStart hook (`context_inject.py`) that re-injects the
run state from disk after compaction or resume. Both stay silent when nothing is wrong. Install, side
effects, and why other checks are not hooks: [claude-code-hooks.md](references/claude-code-hooks.md).

## Done When

- every job in `jobctl.py status` is running or handled, and every handled result is in the ledger;
- every open question has `blocks`, `default` and `line`, and no line waits on a non-blocking one;
- each reported conclusion passed the report gate, and each abandoned approach is in `dead_ends.md`;
- idle GPUs have either a ready task or a current `idle_ok.json`.
