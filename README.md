# Research Agent Kit

Reusable agent instructions and skills for research-code projects: bootstrap a fresh paper repository, hand off context between agents, and carry a task from repository inspection through implementation and validation.

This kit is meant to be copied into your own Codex or coding-agent setup and adapted to your lab. The included `AGENTS.md` is a template, so replace placeholder machine names, usernames, mount paths, CUDA locations, queue policies, and other environment-specific details with values that match your actual workflow.

## Contents

- `AGENTS.md` - template research/GPU/uv workflow instructions for coding agents.
- `skills/paper-code-bootstrap` - set up a newly cloned paper-code repository with `uv`, checkpoints, CUDA extensions, and an inference smoke test.
- `skills/research-task-implementation` - rebuild context from a research repo and task document, then implement, validate, and report concrete commands.
- `skills/handoff` - create or resume concise project handoffs between coding agents.

## Install Into Codex

```fish
mkdir -p ~/.codex/skills
cp -R skills/paper-code-bootstrap ~/.codex/skills/
cp -R skills/research-task-implementation ~/.codex/skills/
cp -R skills/handoff ~/.codex/skills/
cp AGENTS.md ~/.codex/AGENTS.md
```

If you already have `~/.codex/AGENTS.md`, merge the relevant sections instead of overwriting it.

## Example Prompts

```text
Use $paper-code-bootstrap to set up this new paper repository with uv, download checkpoints, and verify an inference demo.
```

```text
Use $research-task-implementation with docs/tasks/adapter_ablation.md, inspect the repo first, then implement the requested config and training changes.
```

```text
Use $handoff to write a HANDOFF.md so another coding agent can continue from here.
```

```text
Use $handoff to resume from HANDOFF.md before making changes.
```

## Notes

- Treat this repository as a starting point, not a drop-in description of your environment.
- Fill in concrete hostnames, paths, CUDA/toolchain locations, and GPU usage rules before relying on the template in real projects.
- Prefer repo-local `.venv` environments and `uv run`.
- Build CUDA extensions on GPU nodes, not file servers.
- Compile CUDA extensions for every GPU architecture that may use the shared environment.
