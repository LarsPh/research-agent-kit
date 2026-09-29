# Field Notes

Observed in September 2026 with the Orca desktop app 1.4.x on a Windows machine relaying to a Linux SSH
host, a Codex desktop app on the Windows side, and Claude Code and Codex CLI in remote Orca terminals.
Re-test when versions change.

## Worked

- `orca file open <relative> --worktree id:$ORCA_WORKTREE_ID` opened Markdown, PNG, and Git-ignored files,
  and files reached through a symlink from an ignored directory to a storage root outside the worktree.
- Relative and absolute paths printed by a remote Claude Code session were clickable in the Orca terminal.
- A remote coordinator started a Codex worker with `orchestration worker-start`; the worker's
  `worker_done` arrived with `reportPath`, `filesModified`, and custom payload keys merged into one JSON
  payload; `check --wait`, `--ack`, and `worker-release` settled it in about a minute.
- A desktop Codex agent read card comments via `worktree ps`, got `satisfied: true` from `terminal wait`
  on a remote Claude Code terminal, and exchanged tagged one-line messages with it via
  `terminal send` / `terminal read`.
- `orca computer` executes on the local desktop, not on the SSH host.

## Failed, and Why

| Symptom | Cause | Remedy |
|---|---|---|
| `selector_not_found` naming a local-drive form of the remote path | CLI inferred the worktree from cwd in relay mode | pass `--worktree id:$ORCA_WORKTREE_ID` |
| `selector_ambiguous` with `path:` | the same path registered under two Orca repo entries (e.g. a stale SSH connection) | use `id:`; remove the stale host setup in Orca |
| `invalid_relative_path` | path outside the worktree, or a leading `./` | link the root into an ignored dir; drop `./` |
| `worker-start` fails at `agent_readiness` | Claude Code waiting on its permission-mode confirmation; Codex waiting on an update notice | user handles the prompt once; skipping an update is safe to send |
| desktop agent: `no_active_sender_terminal`, `consumer_fenced` | orchestration mailbox requires an Orca terminal identity | use terminal conversation + outbox |
| `scp` hangs; with `BatchMode` returns `Permission denied (publickey)` although the right key is offered | inferred: key is passphrase-protected and absent from the local ssh-agent (fix not yet re-tested) | user runs `ssh-add <key>` once |
| Orca session search finds Codex sessions only | index covered one agent type on that host | do not rely on it for Claude history; keep decisions in the ledger |
