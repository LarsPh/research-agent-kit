---
name: research-task-implementation
description: "Repeatable workflow for research-code sessions that start from a fresh agent context: inspect repository documentation and code, read the owning task or plan, maintain its checklist, implement the documented experiment or model change, verify it on the repository's truthful runtime, and report skipped or deferred work. Use for decision-complete changes to research configs, data, models, losses, renderers, training, evaluation, or accelerator workflows."
---

# Research Task Implementation

Use this skill after a research bite is decision-complete. For open-ended direction finding, begin with the
repository's research-sprint workflow instead.

## Protect User Control

- Treat explicit requirements and “must do this time” items as hard constraints.
- Ask after targeted inspection when ambiguity changes experiment behavior, architecture, interfaces, data,
  outputs, runtime cost, evaluation meaning, or claim scope.
- Preserve the documented model, feature/token flow, camera/render math, dataset semantics, loss, and
  trainer. Never replace them with a convenient scaffold without approval.
- Label an approved reduced path `provisional smoke only`; list every production piece it omits.
- Use Chinese for plan/checklist/milestone prose unless the repository or team requires another language.
- Report `not done`, `skipped`, `deferred`, and `blocked` work explicitly.

## Rebuild Context

1. Read repository instructions, the documentation entry point, the owning plan, prior milestone/review,
   relevant failures/deferred records, and `git status`.
2. Extract the plan checklist as the authoritative work list.
3. Inspect actual entry points, configs, types, data flow, model/loss/trainer code, tests, and recent related
   commits. Record drift between docs and code.
4. Resolve discoverable facts through inspection. Ask before choosing research intent.

## Freeze the Executable Contract

Before editing, ensure the owning plan defines:

- scope, out-of-scope, inputs/outputs, identities, shapes, data or coordinate semantics, and failures;
- real architecture and data flow, including feature sources, intermediate states, fusion, losses, and
  training ownership where relevant;
- config or public-interface changes, compatibility, validation layers, visuals, and runtime budget;
- checklist plus acceptance, review, and user-stop boundaries.

Update the owning document rather than creating a competing task plan. Mark unresolved items blocked; do not
code through them.

## Implement Conservatively

- Follow existing naming, module boundaries, config patterns, and dependency seams.
- Keep the diff scoped; preserve unrelated dirty files and exact user-created hunks.
- Preserve checkpoint/config compatibility unless the plan explicitly changes it.
- Keep smoke scaffolds behind explicit debug/provisional controls; never expose them as production defaults,
  official APIs, checklist completions, or acceptance evidence.
- Update checklist status only after the corresponding implementation and verification are true.

## Validate in Layers

1. Run cheap syntax, schema/config-load, static, and focused CPU/reference tests first.
2. Run broader relevant tests and entry-point help/import checks.
3. Use the repository's documented compute path for accelerator builds, rendering, gradients, mini-training,
   and performance. Inspect the actual runtime before choosing commands or devices.
4. Run a minimal truthful smoke before a long experiment; preserve formal batch/data contracts rather than
   substituting singleton fixtures.
5. Generate diagnostic visuals for spatial, temporal, perceptual, camera, or branch semantics and open them
   for visual inspection.
6. Record commands, runtime identity, results, failed attempts, and any validation that could not run.

Passing engineering gates proves implementation wiring at their stated boundary; it does not automatically
prove reconstruction quality or a research claim.

## Stop and Close Correctly

Before user acceptance:

- reconcile every checklist item;
- explain representative visuals and limitations in chat and docs;
- state completed, not-done, skipped, deferred, and blocked work;
- stop at the repository's human evidence-review gate.

After acceptance, perform only the authorized closure actions: milestone, selected Git evidence, tracker
closure, and commit. Before committing, inspect recent related commit subjects, stage exact files or hunks,
and check the cached diff.
