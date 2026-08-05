---
name: zhaorong-research-workflow
description: "Adaptive research-sprint orchestration for existing ML and graphics repositories. Use when Codex needs to initialize agent workflow in a migrated or legacy research repo, explore a codebase with new data and visual diagnostics, turn research discussion into a rolling bite-sized plan, analyze experiment evidence and revise direction, or run a formal implementation and review sprint without freezing the full roadmap."
---

# Zhaorong Research Workflow

Run research as a rolling evidence loop. Keep repository documents authoritative, expose uncertainty,
and plan only the frontier that current evidence makes decision-complete.

## Start Every Run

1. Read repository instructions, the documentation entry point, current direction or task document,
   relevant experiment reports, and `git status` before proposing changes.
2. Reconstruct facts from code, configs, data contracts, and recent history. Ask only for decisions that
   inspection cannot resolve.
3. Follow the repository's stated authority order. When an older overview conflicts with a newer accepted
   focused review or report, identify the supersession explicitly; do not silently choose or rewrite history.
4. Identify the current branch below. Read its reference completely before acting.
5. Use Chinese for plans, checklists, and experiment analysis by default. Follow an established team or
   repository language when it requires another language.
6. Preserve explicit user requirements. Surface `not done`, `skipped`, `deferred`, and `blocked` work.

When the user requests a read-only pass, inspect normally but return proposed authority-document updates,
the bounded validation budget, and explicit statuses without editing files, creating tickets, or launching jobs.

## Route the Work

### Initialize or Migrate a Repository

Read [initialization.md](references/initialization.md). Use this branch for an existing repository that is
moving machines, changing compute platforms, or gaining its first durable agent workflow.

Complete this branch only when repository authority and the next environment-onboarding step are clear.
Stop before configuring the project environment or running paid/heavy compute.

### Explore a Research Question

Read [sprint-lifecycle.md](references/sprint-lifecycle.md) and
[experiment-evidence.md](references/experiment-evidence.md). Use the exploration lane for new datasets,
diagnostics, bug localization, feasibility probes, and throwaway idea prototypes.

Complete this branch only when the question, evidence, interpretation, confounds, and next decision are
recorded. An exploration result is not a milestone or production implementation.

### Implement a Decision-Complete Bite

Read [sprint-lifecycle.md](references/sprint-lifecycle.md). Invoke `research-task-implementation` when it
is installed. Use the implementation lane only after the owning document contains a decision-complete
scope, checklist, acceptance evidence, and explicit out-of-scope items.

Complete this branch only after proportional static/CPU/accelerator checks, representative visual review
when semantics are visual, checklist reconciliation, and the required human acceptance boundary.

### Review Results or Change Direction

Read both [sprint-lifecycle.md](references/sprint-lifecycle.md) and
[experiment-evidence.md](references/experiment-evidence.md). Separate observations from interpretation,
retain plausible competing hypotheses, and update the living direction without rewriting accepted
reports or milestones.

Complete this branch only when the evidence-supported decision, superseded assumption, affected
authority documents, and next frontier are explicit.

## Use Companion Skills Deliberately

- Use `setup-matt-pocock-skills` once to establish tracker, triage, and domain-document seams.
- Use `grilling` for unresolved research choices; use `wayfinder` only for fog spanning multiple sessions.
- Use `research`, `prototype`, or `diagnosing-bugs` to answer bounded questions before production work.
- Use `codebase-design` for a new module, adapter, cache, artifact, trainer, or cross-component contract.
- Use `code-review` from a fixed point at risk-based review nodes; keep Standards and Spec separate.
- Use `domain-modeling` only when stable terminology or a durable trade-off actually changes.

If a required companion skill is missing, report the missing dependency and give an installation command.
Do not emulate a missing skill by inventing a competing local workflow.

## Guard the Claim Boundary

- Treat smoke runs, bounded probes, and untrained visuals as engineering evidence, not academic results.
- Preserve the documented model, data, rendering, loss, and training semantics. Label any approved
  reduced path `provisional smoke only` and list the production pieces it omits.
- Keep raw artifacts in the discovered persistent store. Put only reviewed analysis and representative
  evidence in Git.
- Require an agent to open and inspect representative visuals; generation alone is not visual review.
- Keep tracker tickets as coordination artifacts. Designs, checklists, experiment analyses, decisions,
  milestones, and deferred work stay in repository authority documents.
