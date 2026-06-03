---
name: handoff
description: Create or consume concise coding-agent handoffs. Use when the user asks to hand off work between Codex, Cursor, Codex CLI, or another coding agent; when ending a coding session; when resuming from HANDOFF.md; or when a repository contains handoff notes that should guide continuation.
---

# Handoff

Use this skill to preserve actionable project state without replaying a full chat transcript.

## Ending A Session

Create or update `HANDOFF.md` in the repository root unless the project already uses a specific handoff path.

Do not dump the full conversation. Keep only the state another agent needs to continue safely:

1. Current goal
2. Repository, branch, and environment
3. Files changed, inspected, or intentionally left alone
4. Key design decisions and rejected alternatives
5. Commands run and important results
6. Test and verification status
7. Known issues, risks, and blockers
8. Next concrete steps
9. Do-not-change warnings

If a full transcript is useful, save it separately under `agent-history/YYYY-MM-DD-short-topic.md` and treat it as archive only.

## Resuming A Session

Before editing code:

1. Read `AGENTS.md` or any repo-local agent instructions.
2. Read `HANDOFF.md` or the named handoff file.
3. Inspect files referenced in the handoff.
4. Restate the current state in 5-10 lines.
5. Continue from the listed next steps.

Never rely only on the user's prompt if a handoff exists.

## Handoff Format

Use this structure unless the project already has a stricter template:

```md
# HANDOFF

## Current Goal

## Repository / Environment

## Current State

## Files Changed / Touched

## Key Design Decisions

## Commands Already Run

## Test / Verification Status

## Known Issues / Risks

## Next Steps

## Do Not Change / Caution
```
