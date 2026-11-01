# Job Lifecycle

## Launch

```sh
python SKILL_DIR/scripts/jobctl.py launch --id L3-d50 --brief runs/briefs/L3-d50.md --gpu 0 \
  --cwd /path/to/repo -- python train.py --config configs/d50.yaml
```

- **Detached.** tmux session `lr-<id>` when tmux exists, else a new process session. Either way the job is
  not a child of the agent's shell, so it survives the agent's turn, its sub-agent, or a session restart.
- **Wrapper.** `status/<id>.sh` runs the command with output appended to `logs/<id>.log`, then writes
  `"<token> <exit code>"` to `status/<id>.done` atomically.
- **Token.** A random token per launch, stored in `status/<id>.json`. A `.done` file with another token
  (from an old run, a copied folder, a backup) is ignored.

## States

`jobctl.py status` prints one line per job; `watch` prints only what needs action and exits 1 if anything
does.

| State | Rule | Action |
|---|---|---|
| running | no valid `.done`, wrapper process alive, log written within `--stall-min` | none |
| stalled | wrapper alive but log silent longer than `--stall-min` (default 30) | inspect the log and GPU; kill and relaunch, or raise `--stall-min` for slow phases |
| done | `.done` has this job's token and exit 0 | record the result, then `jobctl.py handled <id>` |
| failed | `.done` has this job's token and a nonzero exit | read the log tail, record, decide retry or dead end |
| crashed | no valid `.done` and the wrapper is gone | killed from outside (OOM killer, node reboot, `kill`); the last log line is shown |

Liveness uses the recorded pid and checks `/proc/<pid>/cmdline` still names the wrapper, so pid reuse is
not mistaken for a live job. Nothing greps logs for success strings and nothing uses `pgrep -f`, which
matches its own command line.

## Logs

Keep job output terse and grep-friendly: progress every N steps, not every step; errors on one line with
`ERROR` and the reason. Long noisy logs fill the agent's context when it reads them.
