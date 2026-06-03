---
name: research-task-implementation
description: "Repeatable workflow for research-code sessions that start from a fresh agent context: inspect repository documentation and code, read a task/agent plan document, produce or refine an implementation plan when requested or in planning mode, then implement, verify, and report concrete commands. Use when the user asks an agent to understand a research repository from docs plus code before modifying experiments, configs, training scripts, model code, evaluation code, accelerator/GPU workflows, or task documents."
---

# Research Task Implementation

Use this skill for research engineering tasks where the agent must rebuild context from repository artifacts, follow a task document, and then make a careful code/config change.

## Workflow

1. Ground in the repository before asking questions:
   - Read repo-local agent instructions first if present.
   - Read the task document named by the user.
   - Inspect nearby docs, configs, entrypoints, model/loss/dataset code, and recent related plans.
   - Use fast search and targeted file reads. Prefer facts from the repo over questions.
   - Check the worktree status before edits and avoid touching unrelated dirty files.

2. Reconstruct the current system:
   - Identify the existing behavior, relevant flags, config schema, interfaces, data flow, and tests.
   - Compare the task document against actual code; note drift instead of assuming the document is current.
   - Resolve discoverable ambiguities through inspection.
   - Ask the user only for high-impact product or experiment choices that cannot be inferred safely.

3. Plan at the right level:
   - If the session is in planning mode or the user asks for a plan, produce a decision-complete plan before editing.
   - Otherwise, make a compact internal plan and implement directly once enough context is gathered.
   - Keep the plan behavior-level: what changes, public interfaces/config keys, edge cases, tests, and assumptions.
   - Preserve the user's experiment intent; do not expand scope into adjacent research ideas unless required.

4. Implement conservatively:
   - Follow existing repo patterns and naming.
   - Keep changes narrowly scoped to the task.
   - Add config keys with backward-compatible defaults.
   - Preserve checkpoint/config compatibility unless the task explicitly changes it.
   - Do not re-enable disabled losses, ablations, code paths, or training features unless the task asks for it.
   - Use explicit patch/edit tooling rather than ad hoc shell writes for manual edits.

5. Validate in layers:
   - Run cheap static checks first, for example:
     ```sh
     uv run python -m py_compile path/to/file.py
     ```
   - Load new YAML/config files with the repository's config loader.
   - Run CPU smoke tests locally when possible.
   - For accelerator builds, accelerator runtime checks, or training/debug renders, use the appropriate compute node, check device availability first, and choose one idle device.
   - Do not launch heavy jobs blindly; prefer a minimal smoke test before a full experiment.

6. Final response:
   - State what changed and name the key files.
   - List verification commands run and their results.
   - Give runnable next-step commands for smoke tests or experiments.
   - Mention any unrun accelerator validation and the exact command the user can run.
   - Call out unrelated dirty/untracked files only when relevant to avoid confusion.

## Defaults

- Prefer the repository's documented environment manager; if none is documented, prefer `uv run python ...` for Python projects.
- Keep commands shell-compatible and label shell-specific syntax when needed.
- Use one accelerator device per job unless the user explicitly requests multi-device execution.
- Treat user-created docs, task plans, and untracked experiment notes as user work; do not rewrite them unless asked.
