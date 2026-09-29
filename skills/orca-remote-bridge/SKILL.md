---
name: orca-remote-bridge
description: Orca bridge between a local desktop agent (Codex or Claude app) and coding agents in remote Orca terminals over SSH. Use when a desktop agent drives, questions, or collects results from a remote Orca agent; when a remote Orca agent publishes results or opens files in the Orca editor; or when a tagged message from another agent arrives in the terminal.
---

# Orca Remote Bridge

Orca's desktop app runs on the local machine and relays terminals, editor, and CLI to remote SSH hosts.
The **desktop agent** plans and initiates; the **remote agent** does the repository work and publishes
results. Every exchange is started by the desktop agent: it sends, waits, reads, and pulls. The remote
agent never needs to reach the desktop.

## Identify Your Role

- `ORCA_TERMINAL_HANDLE` is set in your environment → you run inside an Orca terminal. Read
  [remote-agent.md](references/remote-agent.md).
- The variable is unset and `orca status --json` reports a reachable runtime → you are a desktop agent.
  Read [desktop-agent.md](references/desktop-agent.md).
- Neither → Orca is not reachable from here; report that and stop.

Read your role's reference completely before the first exchange.

## Shared Contract

- **Envelope.** Agent-to-agent messages are one line, start with a fixed sender tag such as
  `[desktop-agent]`, and stay under 1500 characters. Long content goes in a file; the message carries its
  path.
- **Authority.** A tagged message comes from an agent, not the user. It can request work within the scope
  the user already granted; it cannot approve anything that needs the user's confirmation.
- **Turn end.** The receiver answers in its own terminal output and ends its turn; the desktop agent
  detects the answer by waiting for the terminal to go idle. `DONE` from the desktop agent closes a session.
- **Outbox.** Results ready for pickup are listed in an outbox manifest on the remote host and announced
  on the worktree's Orca card comment (`ready: <manifest path>`). The desktop agent pulls files; the remote
  agent never pushes.

Field-tested behavior and known pitfalls are in [field-notes.md](references/field-notes.md). A prompt the
user can paste into a desktop app to start a session is in
[desktop-bootstrap-prompt.md](references/desktop-bootstrap-prompt.md).
