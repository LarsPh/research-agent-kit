# Research Agent Kit

Reusable agent instructions and skills for setting up and continuing research-code projects.

This repository is intentionally sanitized: hostnames, usernames, mount paths, and lab-specific details are represented as placeholders. Copy the templates into your own agent configuration and replace placeholders with local values.

## Contents

- `AGENTS.md` - generic research/GPU/uv workflow instructions for coding agents.
- `skills/paper-code-bootstrap` - set up a newly cloned paper-code repository with `uv`, checkpoints, CUDA extensions, and an inference smoke test.
- `skills/handoff` - create or resume concise project handoffs between coding agents.

## Install Into Codex

```fish
mkdir -p ~/.codex/skills
cp -R skills/paper-code-bootstrap ~/.codex/skills/
cp -R skills/handoff ~/.codex/skills/
cp AGENTS.md ~/.codex/AGENTS.md
```

If you already have `~/.codex/AGENTS.md`, merge the relevant sections instead of overwriting it.

## Example Prompts

```text
Use $paper-code-bootstrap to set up this new paper repository with uv, download checkpoints, and verify an inference demo.
```

```text
Use $handoff to write a HANDOFF.md so another coding agent can continue from here.
```

```text
Use $handoff to resume from HANDOFF.md before making changes.
```

## Notes

- Keep private machine names and paths out of this repository.
- Prefer repo-local `.venv` environments and `uv run`.
- Build CUDA extensions on GPU nodes, not file servers.
- Compile CUDA extensions for every GPU architecture that may use the shared environment.
