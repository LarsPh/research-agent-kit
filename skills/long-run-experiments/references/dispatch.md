# Task Briefs

Every job and every sub-agent task starts from a brief in `runs/briefs/<id>.md`. `jobctl.py launch`
refuses to start without one that passes `check_brief.py`. Briefs exist because a sub-agent sees only what
it is given: each missing field below caused a rework in a real overnight run.

## Template

```markdown
line: L3
why: main table row 2 (night scene, d50); highest open priority in the ledger
goal: train d50 for 2k steps from checkpoint ckpt_1500 and evaluate on the 12 held-out views
outputs: runs/out/L3-d50/ (eval.json, renders/, train.log)
done_when: eval.json has psnr/ssim/lpips for all 12 views and renders/ has 12 PNGs
budget: 1 GPU for 3 h; paid API $0
time_limit: 3h; stop and report if not converging by step 1000
wait: detached; the dispatcher does not wait in its own session

## Rules for this task
- Do not read credential files (.env, *token*, *key*); use only the approved paid-API path.
- Evaluate with the same frame format as the user-study clips.
- Write the five statuses (done, partial, failed, skipped, blocked) in the README of the output folder.
```

## Fields

| Field | Required | Why |
|---|---|---|
| `line` | yes | ties the job to a research line in the ledger |
| `why` | yes | the priority or table cell it serves; jobs without a reason are padding |
| `goal` | yes | what to run, from what state |
| `outputs` | yes | where results go, so the next cycle finds them |
| `done_when` | yes | a checkable end state, not "train until good" |
| `budget` | yes, with a number | a concrete cap; "1.5× the last run" drifts upward |
| `time_limit` | yes, with a number | models have no sense of elapsed time |
| `wait` | no | `detached` (default) or `same session`; when a task says to wait, that overrides a general "hand back after launch" rule |
| project fields | per `brief_fields.txt` | for example `eval_frame_format` |

Keep briefs short and specific. Put rules that apply to every task in the project's `AGENTS.md` instead of
repeating them, and put only task-specific rules here.

## Sub-agents

A sub-agent that runs a job must launch it through `jobctl.py`, not as its own background command: a
background command started by a foreground sub-agent stops when that sub-agent's run ends (Claude Code
tools reference, "When a background command stops").
