# Waking Up Without Polling

The model should never spend tokens to wait. Two mechanisms, from cheap to robust:

## In the session: wait_for_gpu.py

```sh
python SKILL_DIR/scripts/wait_for_gpu.py --count 1 --max-mem-mb 1000
```

Run it as a background command. It polls `nvidia-smi` locally every 60 s and exits when enough GPUs are
idle; Claude Code tells the agent when a background command exits. Limits: background commands in
unattended runs (`-p`, SDK, cloud) stop after at most 2 hours, so the script times out at 110 minutes with
exit 3; the Monitor tool's watches end after at most 30 minutes. Interactive terminal sessions have no
limit. Use it for waits you expect to be short.

## Outside the session: resume_check.py from cron

```cron
*/5 * * * * cd /path/to/repo && LONGRUN_DIR=runs python SKILL_DIR/scripts/resume_check.py \
  --activity '~/.claude/projects/<project>/*.jsonl' \
  --resume-cmd 'tmux send-keys -t agent {reason} Enter' >> runs/cron.log 2>&1
```

Each tick it wakes the agent only when `runs/UNATTENDED` exists, there is work (an unhandled finished job,
or an idle GPU with a ready task or without a recorded reason to idle), the agent has been quiet for
`--quiet-min` minutes, and the last wake-up is older than `--cooldown-min`. It reads state rather than
waiting for an event, so nothing is missed: a wake-up skipped now is taken on the next tick. The same rule
restarts an agent that stopped by itself.

`--resume-cmd` is any command that delivers a message to your agent:

- an open interactive session in tmux: `tmux send-keys -t agent {reason} Enter`;
- a headless Claude Code session: `claude -p --resume <session-id> {reason}`;
- another agent CLI: its own resume command.

`--activity` is a glob of files the agent writes while working, usually its transcript. Test the line with
`--dry-run` first.
