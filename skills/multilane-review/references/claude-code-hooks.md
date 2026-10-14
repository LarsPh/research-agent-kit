# Optional Claude Code Hooks

Two opt-in hooks for Claude Code. Other platforms skip this file; the skill works without them.

| Hook | Event | What it does |
|---|---|---|
| `scripts/log_coverage.py hook` | PostToolUse on `Read\|Grep\|Glob` | Appends each read or search, with the agent that made it, to `<temp>/multilane-review/<session>.jsonl` |
| `scripts/check_report.py` | Stop | When the final message is a multilane report, blocks the stop until the four sections exist, each of the top 8 bugs has a status, every `rejected` quotes its line, and Coverage says the review was static |

Neither hook writes inside the target repository. `check_report.py` ignores messages without a `## Bugs`
heading and blocks at most twice per session, so it never traps an unrelated conversation.

## Install for one review session

Load the hooks only for the review, not in user or project settings, so they never run in unrelated
sessions. Save this as `multilane-review-hooks.json`, with `SKILL_DIR` replaced by the installed skill path
(for example `~/.claude/skills/multilane-review`):

```json
{
  "hooks": {
    "PostToolUse": [
      {"matcher": "Read|Grep|Glob",
       "hooks": [{"type": "command", "command": "python3 SKILL_DIR/scripts/log_coverage.py hook"}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "python3 SKILL_DIR/scripts/check_report.py"}]}
    ]
  }
}
```

Start the review with `claude --settings multilane-review-hooks.json`. Hooks also fire inside sub-agents, and
the hook input then names the sub-agent's type, so each lane's reads are logged under its own name.

## Fill the Coverage section

After the lanes return, summarize the log against the target:

```sh
python3 SKILL_DIR/scripts/log_coverage.py summary --repo <target repo> --range main...feature
```

It prints the files each agent opened and the target files no agent opened. Copy the second list into the
report's Coverage section. To check a saved report by hand: `check_report.py --file report.md`.

## Limits

- The log records what a lane opened, not what it understood. An opened file is not a reviewed file.
- `Grep` and `Glob` entries record the searched path, not every file they matched.
- Without the `agent_type` hook field (older Claude Code), all reads are logged under `main`.
