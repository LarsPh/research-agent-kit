---
name: review-ops-security
description: Read-only review of how code behaves in long or repeated runs and, for code that ships or loads others' files, its security and supply chain. Operations mode covers checkpoint and resume, log and I/O cost, worker and GPU setup, and recovery after errors; full mode adds unsafe deserialization, shell strings, and dependency pinning. Use alone to ask whether a training or service script will survive a long run, or as lane E of multilane-review.
---

# Review Operations and Security

Some problems show up only after hours of running or once other people use the code. Choose the mode first:
`operations` for research code that stays on its author's machines; `full` for code that is deployed,
published for others to run, or loads files from other people. Ask the user when unsure, and say which mode
you used.

## Protect the Target

Review read-only. Never edit, commit to, or push the target repository. Take the target from the user; ask
when none is named.

## 1. Get the Context

If a brief from multilane-review is provided, use it. Otherwise read the README, the run and install
instructions, and the target file list.

## 2. Check

**Operations (both modes).**

- Checkpointing and resume: periodic saves, and whether a crash loses the run.
- Idempotent re-runs: in-place overwrites of inputs or results.
- Log and artifact cost: files rewritten in full every step (quadratic I/O), memory retained across an
  epoch.
- Worker and device setup: fork after CUDA initialisation, identical seeds across workers.
- Recovery: one runtime error permanently disabling a loop or a renderer.
- Platform paths: non-ASCII and cross-drive paths.

**Security and supply chain (full mode only).**

- Unsafe deserialization: `torch.load(weights_only=False)`, `pickle`, `yaml.load`.
- `eval`/`exec`, shell commands built from strings, paths read from untrusted files.
- Unpinned or undeclared dependencies, a lockfile that is not enforced, reliance on private APIs of
  dependencies, development tools in runtime dependencies.
- Commit granularity: changes too large to review or revert.

Skip files the docs mention that are deliberately absent.

## 3. Report

State the mode, then one table, most severe first. 400 words or fewer.

| # | file:line | finding | kind | severity | failure scenario |
|---|---|---|---|---|---|

- `kind` is `bug` when the code will fail or lose work; otherwise `ops` or `security`.
- `severity` is high, medium, or low.

When run alone, end with: "Static review; not verified by a second pass."

Done when every check in the chosen mode has a finding or is noted as not applicable.
