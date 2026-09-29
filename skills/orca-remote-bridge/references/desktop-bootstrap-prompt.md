# Desktop Bootstrap Prompt

The user pastes this into a desktop agent (Codex or Claude desktop app) to open a session with a remote
Orca agent. Fill the placeholders first; `orca terminal list --json` shows handles. The rules repeat the skill's contract
so the prompt still works in an app where the skill is not installed.

```text
Use $orca-remote-bridge as the desktop agent.

Remote agent terminal: <TERMINAL_HANDLE>
Remote worktree id: <REPO_ID>::<WORKTREE_PATH>
SSH host alias for pulls: <SSH_HOST_ALIAS>
Local inbox for pulled files: <LOCAL_DIR>
Sender tag: [desktop-agent]

Goal for this session: <what to plan, ask, or collect>

Rules:
- Wait for tui-idle with satisfied=true before every send and before every read.
- One-line messages starting with the sender tag, under 1500 characters; long content goes in files.
- Pull files with scp -o BatchMode=yes -o ConnectTimeout=15 into the local inbox; open what you pull.
- Stay within this goal. Anything that needs my approval, stop and ask me.
- Send "[desktop-agent] DONE" when the goal is met, then summarize for me: what was done, what is
  waiting on me, and where the pulled files are.
```
