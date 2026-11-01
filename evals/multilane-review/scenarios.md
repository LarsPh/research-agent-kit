# Evaluation Scenarios (drafted, not run)

Ground truth comes from bugs that are already known, so a run can be scored by recall and false positives.
The strongest source is the maintainer's earlier four-repository comparison of review methods, which
recorded which lane found which confirmed bug; turn it into fixtures by pinning each repository at the
reviewed commit and keeping the confirmed-bug list private to the grader.

## 1. Research repository with seeded domain bugs

Fixture: a small rendering or training repository with a reference implementation (CPU or float64 path)
and three seeded bugs: a sign error in a camera convention, an int32 offset overflow in a packing step, and
a silent zero fallback for missing data. No tests.
Prompt: "Use $multilane-review to review main...feature read-only."
Expected:
- asks the three lane questions, or states its defaults when unanswered; lane T off because there are no tests;
- finds at least two of the three seeded bugs, each with a proof path;
- does not edit the repository;
- the Must Read tier has 5 items or fewer.

## 2. Docs and code drift along the README commands

Fixture: a pipeline whose README runs three stages; stage 2 writes a file name stage 3 no longer reads, and
one stage exits 0 after an exception.
Prompt: "Review this branch before I merge it."
Expected:
- lane D traces the README chain and reports both the hand-off break and the failure reported as success;
- these appear in Must Read, not only in the appendix.

## 3. Test-first change with weak tests

Fixture: a change with tests written first, where one test asserts only the output shape.
Prompt: "Use $multilane-review; the change was test-first."
Expected:
- lane T on and lane A off per the presets;
- lane T mutates the shape-only test's target in a scratch copy and names the missing assertion;
- the review never mutates the original repository.

Baseline: the platform's built-in single-pass review on the same target. Compare recall of known bugs,
false positives, and tokens.
