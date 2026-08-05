# Experiment Evidence and Analysis

Make every run recoverable from persistent evidence even when the compute instance is disposable.

## Bind Provenance

Record enough information to distinguish code, environment, data, and runtime changes:

- repository remote, branch, commit, and relevant worktree diff identity;
- resolved config, command, seed policy, and task entry point;
- environment lock plus image or runtime identity when the platform exposes one;
- dataset/case/view manifest and preprocessing/cache identities;
- dependency/model/checkpoint identities and integrity hashes where practical;
- start/end status, resource request, runtime, logs, structured metrics, and failure reason;
- artifact root and an inventory of checkpoints, reports, and visuals.

Never store credentials, internal tokens, or restricted dataset contents in logs or public artifacts.

## Respect Ephemeral and Persistent Boundaries

Discover which filesystems survive a fresh instance. Build environments and caches only after their lifetime,
ownership, concurrency, quota, and invalidation semantics are known. Publish required outputs to persistent
storage before declaring a run complete, and verify important cache/artifact reads from a fresh instance.

Use semantic experiment directories rather than stage numbers alone. Keep partial and failed attempts
distinguishable from accepted evidence. Preserve immutable raw captures when derived visualizations may be
regenerated.

## Design Visual Evidence

Choose visuals that can falsify the intended semantics: view order, orientation, coordinate basis, crop and
mask alignment, temporal order, ownership, branch routing, failure regions, or the measured intervention.

For every representative figure:

1. Label dataset, case, view, branch, step, and diagnostic-only status where relevant.
2. Explain each panel, expected signal, observed signal, and what the panel cannot establish.
3. Open the actual output with visual tools and inspect legibility, alignment, flips, invalid regions, and
   misleading scales or occlusion.
4. Regenerate misleading figures before requesting user review; numerical gates do not excuse a bad figure.

## Analyze Before Deciding

Write the analysis in this order:

1. **Question:** the decision the experiment was meant to unlock.
2. **Setup:** data, code/runtime identity, intervention, baseline, and validation boundary.
3. **Observations:** measured numbers and visible facts without causal language.
4. **Interpretation:** the best current explanation and why it fits.
5. **Alternatives and confounds:** plausible competing hypotheses, weak controls, and missing evidence.
6. **Claim boundary:** engineering wiring, bounded feasibility, reconstruction quality, or formal research
   evidence; state which level is justified.
7. **Decision:** continue, pivot, defer, reject, or promote, with the next falsifiable step.

An experiment launch, successful process exit, generated image, or falling diagnostic loss is not by itself a
research conclusion.

## Archive Selectively

Keep raw outputs, full logs, caches, and checkpoints in the discovered persistent artifact store. Commit
compact analysis and representative visuals only when a result is promoted, accepted, or needed to preserve
a failure/pivot decision. Record paths and identities for exploratory evidence that remains outside Git.
