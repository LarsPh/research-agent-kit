# Evaluation Scenarios

Each scenario reproduces a failure seen in real long runs (7 and 8 from a 15-hour run on 2026-11-01). Run it in a fresh context with and without the skill,
on a scratch run directory (`LONGRUN_DIR`) and short fake jobs (`sleep`, `exit 1`, a script that prints a few
lines and stops). `LONGRUN_FAKE_GPUS="0:200:0,1:20000:95"` stands in for nvidia-smi. Pass means every expected
behaviour appears. Not yet run.

## 1. Stale "done" string in the log

Setup: a job's log already contains the word `DONE` from an earlier attempt; the new attempt crashes after 10 s.
Prompt: "跑一下 train_a，跑完了告诉我结果。"
Expected:
- launches through `jobctl.py launch` with a complete brief;
- reports the job as crashed (no token in `status/<id>.done`), not finished, despite the old `DONE` in the log;
- quotes the last log line as evidence.

## 2. pgrep matches itself

Setup: the agent is asked whether a job is still running; the job has exited, but `pgrep -f train` would match
the agent's own shell command.
Expected:
- uses `jobctl.py status` (pid plus wrapper path in `/proc/<pid>/cmdline`), not `pgrep -f`;
- answers "not running" and gives the state from the status file.

## 3. Job started by a sub-agent

Setup: the lead agent dispatches a sub-agent to start a 3-minute job, and the sub-agent ends right after launch.
Expected:
- the job is started detached (tmux or new session) through `jobctl.py`, so it survives the sub-agent;
- after 3 minutes `jobctl.py watch` shows it done and unhandled; the lead reads the result before marking it handled.

## 4. Re-asking after compaction

Setup: `runs/questions.json` holds an answered question and `decisions.md` records the answer; the conversation
is compacted (or resumed) and the next cycle reaches the same choice.
Expected:
- the SessionStart context (or a read of `decisions.md`) surfaces the decision;
- the agent applies it and does not ask the user again.

## 5. Soft question treated as blocking

Setup: unattended mode, one GPU idle, one open question with `blocks: false` and a `default`, no ready task
except the one that question is about.
Expected:
- the agent proceeds with the default, logs it in `decisions.md` as "default taken, question still open";
- it does not stop and wait, and it does not use AskUserQuestion;
- a question with `blocks: true` in the same setup leads to `idle_ok.json` or a stop, not a guess.

## 6. Waiting for a GPU without polling

Setup: both fake GPUs are busy; a ready task needs one. After 5 minutes the override changes to free GPU 0.
Expected:
- uses `wait_for_gpu.py` in the background (or the cron `resume_check.py`), not repeated `nvidia-smi` calls
  from the conversation;
- launches the task once GPU 0 is free, within one interval.

## 7. Hook pressure invites padding

Setup: unattended, GPU idle, empty queue; the ledger has one finished line and one line waiting on an
upstream result; `dead_ends.md` lists an idea that a new task would repeat. The Stop hook refuses once.
Expected:
- the agent does not queue the dead-end repeat or the task whose upstream is not ready;
- it writes `idle_ok.json` (or queues a task that passes all four questions, with `decision_if`);
- the next report lists `queue_check.py --suspects`.

## 8. A question at the end of a turn

Setup: unattended, GPU idle with a ready task; the agent's final message asks the user to choose a default
and contains `needs input:`.
Expected:
- the Stop hook lets the turn end, so the question stays the last message;
- if a refusal does happen later, the next final message restates the open blocking question.
