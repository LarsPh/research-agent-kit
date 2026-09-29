# Desktop Agent

You run in a desktop app on the local machine and reach the remote host through the `orca` CLI and SSH.
You initiate every exchange.

## Preflight

1. `orca status --json` → runtime `reachable: true`.
2. `orca worktree ps --json` → find the worktree by path or display name; note its `worktreeId` and card
   comment.
3. `orca terminal list --worktree id:<worktreeId> --json` → pick the terminal whose title or agent marks
   the remote agent; note its `handle`. Handles change when Orca restarts; re-list on
   `terminal_handle_stale`.
4. Confirm the SSH pull path once (see **Pull Files**).

Preflight is complete when you hold a live handle, a working `orca terminal read` on it, and one
successful pull.

## Converse

For each message:

1. `orca terminal wait --terminal <handle> --for tui-idle --timeout-ms <ms> --json`. Continue only when
   `satisfied` is `true`; a timed-out wait still prints a result, so read the field. Re-wait with a larger
   timeout when the remote agent is mid-task.
2. `orca terminal send --terminal <handle> --text "<[desktop-agent] one-line message>" --enter --wait-submit 10 --json`.
   Newlines submit early, so keep the message on one line; put long content in a file on the remote host
   (or reference one there) and send its path.
3. Wait for idle again, then `orca terminal read --terminal <handle> --limit 80 --json` and take the
   remote agent's latest reply from the tail. Page with the returned cursors when the reply is long.
4. Send `[desktop-agent] DONE` to close the session.

Never resend on silence. `accepted: true` proves input arrived; idle after it proves the turn ended.

## Discover and Pull Results

1. Poll `orca worktree ps --json` for a card comment of the form `ready: <manifest path>`.
2. Pull the manifest, then every file it lists:

   ```text
   scp -o BatchMode=yes -o ConnectTimeout=15 <ssh-host-alias>:<absolute path> <local inbox dir>
   ```

   `BatchMode` makes authentication failures return at once instead of hanging on a hidden prompt.
3. Read what you pulled before planning the next step; open images, do not infer them from filenames.

The SSH key must be usable without a prompt. When `Permission denied (publickey)` appears although
`ssh -v` shows the right key being offered, the key is passphrase-protected and not loaded in the local
ssh-agent: ask the user to run `ssh-add <key>` once in their own terminal. Leave passphrases to the user.

## Start a Remote Agent

To open a new agent on the remote host, use Orca's handoff commands (`orca skills get orca-cli`):
`orca worktree create --agent <agent> --prompt "<brief>" --json` for a new checkout, or
`orca terminal create --worktree id:<worktreeId> --command "<agent>" --json` in an existing one, then wait
for `tui-idle` before the first send. A startup prompt on the new agent (update notice, permission-mode
confirmation) blocks it; show it to the user.

## Channels That Do Not Fit This Role

- The Orca orchestration mailbox (`orchestration run-create`, `check`, `send`) binds to an Orca terminal
  identity. From a desktop app it fails with `no_active_sender_terminal` or `consumer_fenced`; use the
  terminal conversation and the outbox instead.
- Driving a chat app's upload dialog with `orca computer` is brittle, competes with the user for the
  desktop, and posts content unreviewed. Hand the pulled pack to the user, or read it yourself when you are
  the planner.
