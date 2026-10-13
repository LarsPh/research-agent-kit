---
name: multilane-review
description: Review research or GPU code in four independent lanes (domain bugs with proof paths, generic correctness, end-to-end flow and engineering hygiene, design taste), then verify the top bug candidates. Use to review a branch, diff range, or directory when both bugs and design quality matter, or when one generic review pass is not enough. Triggers include 代码审查, 多线审查, 审一下这个分支, code review.
---

# Multilane Review

No single review pass covers the serious problems in research code. Domain math bugs, cross-stage path
mismatches, unsafe deserialization, and architecture drift each surface in a different lane. Give each lane
its own budget so bug hunting never crowds out design findings, and the reverse.

## Protect the Target

- Review read-only. Never edit, commit to, or push the target repository.
- Post nothing outside the session (issues, PR comments) unless the user asks.
- Take the target from the user: a ref range such as `base...feature`, a branch, or a directory. Ask when
  none is named.

## 1. Build One Shared Brief

Read the README, the docs index and architecture docs, the target repository's own agent instructions, and
the target file list once. Write a brief of 60 lines or fewer with:

- **Intent**: purpose, main data flow, entry points.
- **Main command chain**: the end-to-end commands the README tells a user to run, in order, with the stage
  or script each invokes.
- **References**: slower known-correct implementations (training code, CPU or float64 path, upstream repo,
  paper formulas quoted in the docs), with paths.
- **Conventions**: coordinate systems, units, dtype rules, and stated module boundaries, each with its doc
  file and line.
- **Map**: target files grouped by role (kernels, model, pipeline, UI, config, tests).
- **Known absences**: files the docs mention that are deliberately outside the target (vendored packages,
  binaries, assets). Lanes must not report these as missing.

Pass the brief verbatim to every lane. Done when a lane could start without rereading the docs.

## 2. Run Four Lanes

Run each lane with fresh context: as parallel sub-agents when the platform supports them, otherwise one after
another with the brief as the only shared state. Use the lane prompts in
[lane-prompts.md](references/lane-prompts.md).

| Lane | Looks for | Never reports |
|---|---|---|
| A. Domain bugs | formula parity against references, numerics, packing invariants, GPU handoffs, silent fallbacks; each with a proof path | style, design |
| B. Generic correctness | line-by-line defects, removed behaviour, broken callers; use the platform's built-in code review when it has one | design |
| C. Design taste | module boundaries, doc–code drift, dead or single-value options, duplicated logic, naming, test design | bugs |
| D. End-to-end and hygiene | stage-to-stage path and format hand-offs along the main command chain, failures reported as success, operations, security, dependencies, process | design |

Lane D may run on a cheaper model. Done when all four lanes have returned or their failure is recorded.

## 3. Verify the Bug Candidates

1. Merge lanes A, B, and D; deduplicate by location and cause. Never merge lane C.
2. Drop findings about the brief's known absences.
3. Rank by severity. For the top 8, reread the cited code and its callers and mark each `confirmed` (the
   failure follows from the code as written), `plausible` (depends on inputs or runtime state you cannot see),
   or `rejected` (the code handles it, or the lane's argument fails; quote the line).
4. Run a proof-path test only when it is cheap (CPU only, no datasets) and only from a scratch directory
   outside the repository.

Lanes make wrong arguments: invalid proofs, inflated memory estimates, impossible inputs. Done when each of
the top 8 carries a status and every `rejected` quotes its line.

## 4. Report

Use the layout in [report-template.md](references/report-template.md): verified bugs, end-to-end and hygiene
items, ranked design topics, and coverage. Keep bugs and design in separate sections; never rank one against
the other. State that the review was static and which findings were not run.

Expect roughly three times the tokens of a single-agent review. To save, run lane D on a cheaper model, cap
lane B's effort, and never let lanes reread what the brief already holds.
