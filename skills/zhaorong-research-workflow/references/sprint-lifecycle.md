# Rolling Research Sprint Lifecycle

Plan the visible frontier, not an imaginary fixed roadmap. A stage may change when evidence changes; an
accepted experiment report or milestone remains historical evidence.

## Define the Frontier

Start from a concrete research question, discrepancy, bottleneck, or implementation contract. Update the
living direction with:

- objective and why it matters now;
- established code/data facts;
- live hypotheses and important confounds;
- the decision this sprint should unlock;
- what evidence would support, reject, or leave the question unresolved.

Use `wayfinder` only when the path to that decision cannot fit in one session. Otherwise use focused
discussion or `grilling` and record the result directly.

## Cut an Agent-Sized Bite

A bite is ready when it has one cohesive question or contract and can produce independently interpretable
evidence. It must fit one agent context and a bounded validation run. Combine small changes when splitting
would leave only fragments that cannot be tested until later; split work when interfaces or evidence can be
verified independently.

Specify before code:

- inputs, outputs, identities, shapes, coordinate or data semantics, and failure behavior;
- real architecture and data flow, including losses and training ownership where relevant;
- checklist, acceptance evidence, visualization, runtime budget, and claim boundary;
- explicit out-of-scope and future routes.

Only the current decision-complete frontier becomes executable work. Do not create implementation tickets
for speculative later stages.

Before a probe or implementation, search accepted reviews and failure records for unresolved hard findings
on the same contract. If a finding would invalidate the probe's inputs, supervision, metric, or interpretation,
make its correction a prerequisite. If it is orthogonal, keep it visible as a confound or deferred item rather
than expanding the sprint automatically.

## Choose a Lane

### Exploration Lane

Use for new-data characterization, diagnostics, feasibility tests, and prototypes.

1. Discuss the question and write a minimal experiment or prototype plan.
2. Run the smallest truthful path that can answer it; label reduced paths and avoid production claims.
3. Generate diagnostic visuals when the semantics are spatial, temporal, geometric, or perceptual.
4. Inspect the visuals, analyze evidence, and record confounds and competing explanations.
5. Recommend continue, pivot, defer, reject, or promote to implementation.

Exploration may close autonomously with an experiment record and recommendation. It does not create a
milestone, claim production completion, or merge throwaway code into the main implementation path.

### Implementation Lane

Use only after the owning plan is decision-complete.

1. Update the Chinese checklist and, when coordination warrants it, create an executable issue linking the
   authority document.
2. Implement the documented architecture without replacing it with a convenient approximation.
3. Validate in layers using the repository's actual runtime; run real accelerator paths where CPU tests
   cannot prove the contract.
4. Produce and inspect representative visuals; explain every panel and its limitations in chat and docs.
5. Reconcile the checklist and report every incomplete state. Stop for the required user evidence review.
6. After acceptance, write the milestone, archive selected evidence, close the issue, inspect recent commit
   style, and commit only the intended files or hunks.

## Create Issues Selectively

Create issues for decision-complete multi-session work, ownership/coordination, blocking dependencies, or a
formal implementation bite. Keep tiny exploratory probes in authority documents unless coordination makes
an issue useful. Issues never replace designs, experiment records, or decisions.

## Trigger Review by Risk

Require an external research review and/or fixed-point two-axis code review at:

- a material direction pivot or claim promotion;
- a stable public interface, artifact, cache, data, camera, renderer, loss, or trainer contract;
- a cohesive production implementation batch;
- an experiment cluster that will determine the next stage.

Micro-probes need agent evidence analysis, not ceremonial review. Capture actionable findings in the owning
plan or a correction bite; do not leave them only in chat.

For a read-only planning sprint, return the proposed question, checklist, evidence and visualization gates,
runtime budget, claim boundary, and `completed` / `not done` / `skipped` / `deferred` / `blocked` status. Do not
claim that repository authority was updated.

## Preserve Pivot History

Update the living direction and near-term split when evidence changes. Keep accepted reports, reviews, and
milestones append-only. For a material pivot, record the triggering evidence, superseded assumption,
retained capabilities, abandoned path, and new frontier.
