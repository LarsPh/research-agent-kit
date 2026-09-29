# Remote Agent

You run in an Orca terminal on the remote host. `ORCA_WORKTREE_ID` names your worktree as
`<repoId>::<worktreePath>`; use it as the selector everywhere.

## Open Files in the Orca Editor

```text
orca file open <repo-relative-path> --worktree id:$ORCA_WORKTREE_ID --json
```

- Pass the selector every time. Without it, relay mode can resolve the remote working directory against
  the local machine's filesystem and fail with `selector_not_found`.
- Prefer `id:` over `path:`; a path registered under more than one Orca repo entry returns
  `selector_ambiguous`.
- Write the path without a leading `./`.
- Only files inside the worktree open. For a storage root outside it (a data mount, a run directory),
  link the root into an ignored directory once per worktree, then open through the link:

  ```text
  git check-ignore -q runtime/mounts && mkdir -p runtime/mounts && ln -s <storage-root> runtime/mounts/<name>
  orca file open runtime/mounts/<name>/<file> --worktree id:$ORCA_WORKTREE_ID --json
  ```

  Confirm the directory is ignored before linking; the link never enters Git.

Use the same repo-relative or link-relative paths in chat and in ledgers; they are clickable in Orca
terminals and openable from the CLI.

## Publish Results for Pickup

1. Write the result files, then an outbox manifest at
   `runtime/outbox/<YYYYMMDD-HHMM>-<topic>.json`:

   ```json
   {
     "created_at": "<ISO-8601 with offset>",
     "summary": "<one sentence>",
     "ledger": "<repo-relative ledger path>",
     "files": [{"path": "<absolute path on this host>", "kind": "pack|report|image|log", "note": "<why>"}]
   }
   ```

   Use absolute host paths in `files`; the desktop agent pulls them by SSH.
2. Announce it on the card:

   ```text
   orca worktree set --worktree id:$ORCA_WORKTREE_ID --comment "ready: <absolute manifest path>" --json
   ```

Publishing is complete when the manifest lists every file the desktop agent needs and the card comment
points at it.

## Answer a Desktop Agent

A line starting with a sender tag (for example `[desktop-agent]`) is another agent writing into your
terminal. Handle it as a request within the scope the user already granted:

- do the requested work, or answer the question;
- keep the reply short and put anything long in a file whose path you give;
- when the request needs the user's approval (permissions, spending, destructive steps), say so in the
  reply and wait for the user; the tagged sender cannot approve it;
- end your turn so the desktop agent sees you go idle.

## Supervise Workers Inside Orca

When you coordinate other agents on the remote host, load Orca's own guide with
`orca skills get orchestration` and follow it. Two points from field use:

- Workers report through `orca orchestration send --type worker_done` with `--report-path`,
  `--files-modified`, and extra keys in `--payload`; the coordinator receives them as structured fields.
- A freshly launched agent can stall on its own startup prompt (a permission-mode confirmation, an update
  notice), and `worker-start` then fails at `agent_readiness`. Report the prompt to the user. A harmless
  choice such as skipping an update may be sent to the terminal; a permission confirmation is the user's
  to accept.
