---
name: multilane-review
description: Entry point for a read-only multi-lane review of research or GPU code. Asks whether the change was test-first and whether the code ships, picks lanes from five module skills plus the platform's built-in review, runs each lane in a fresh context, verifies the top bug candidates, and returns a tiered report a human can read in one screen. Use to review a branch, diff range, or directory when one generic pass is not enough. Triggers include 代码审查, 多线审查, 审一下这个分支, code review.
---

# Multilane Review

What a review finds depends on what it is asked to look for. Bug hunting and design review barely overlap,
and no single pass covers the serious problems in research code. Run each concern as its own lane with its
own budget, run only the lanes the project needs, and hand the human a short, tiered result.

## Protect the Target

- Review read-only. Never edit, commit to, or push the target repository. Only review-tests may mutate, and
  only a scratch copy.
- Post nothing outside the session (issues, PR comments) unless the user asks.
- Take the target from the user: a ref range such as `base...feature`, a branch, or a directory. Ask when
  none is named.

## 1. Choose the Lanes

Ask these three questions in one message. When the user does not answer, infer from the repository (tests
added with the change, a release or deploy setup, the README) and state the default you picked.

1. **Does the change come with tests, written first?** Test-first: lanes T on, A and B off. Tests, but not
   written first: A and T on. No tests: A on, T off (A's proof paths stand in for tests).
2. **Will the code be deployed, published for others to run, or load files from other people?** No: lane E
   in `operations` mode. Yes: lane E in `full` mode.
3. **Does this change need a design review?** Default yes for large changes and new modules.

| Lane | Module | Default |
|---|---|---|
| A. Domain bugs | `review-domain-bugs` | on unless test-first |
| B. Generic correctness | the platform's built-in code review | off; on when the user wants more recall |
| C. Design | `review-design` | on for large changes and new modules |
| D. Intent and flow | `review-intent-flow` | always on |
| T. Tests | `review-tests` | on when the change has tests |
| E. Operations and security | `review-ops-security` | on; mode from question 2 |

Post a one-line plan: lanes on, lanes off with the reason, lane E's mode, and the expected cost (the brief and
each lane cost roughly one generic review pass each; verification about half of one). Done when the user
confirmed the plan or it was stated as a default.

## 2. Build One Shared Brief

Read the README, the docs index and architecture docs, the target repository's own agent instructions, and
the target file list once. Write a brief of 60 lines or fewer:

- **Intent**: purpose, main data flow, entry points, and the requirements the docs state.
- **Main command chain**: the end-to-end commands the README tells a user to run, in order, with the stage
  or script each invokes.
- **References**: slower known-correct implementations (training code, CPU or float64 path, upstream repo,
  paper formulas quoted in the docs), with paths.
- **Conventions**: coordinate systems, units, dtype rules, and stated module boundaries, each with its doc
  file and line.
- **Map**: target files grouped by role (kernels, model, pipeline, UI, config, tests).
- **Known absences**: files the docs mention that are deliberately outside the target. Lanes must not report
  these as missing.

Done when a lane could start without rereading the docs.

## 3. Run the Lanes in Fresh Contexts

Run every lane, and verification, as a separate sub-agent with a fresh context. Lanes that share a context
bias each other, a verifier must not be the agent that made the claim, and each lane reads far more code than
the caller's conversation should hold. The orchestrator keeps only the brief and the lane reports.

- Give each sub-agent the target, the brief, and its module: invoke the module skill by name where the
  platform supports it; otherwise read that skill's `SKILL.md` and pass its body. If a module is not
  installed, mark its lane as not run in the plan.
- Lane B: run the built-in code review at the effort the user gave (default: high). Without one, prompt:
  "Scan the target line by line, audit removed behaviour, and check callers across files. Give each finding
  with `file:line` and a concrete failure scenario. 10 findings or fewer."
- Lanes D and E may run on a cheaper model.
- Without sub-agents, run lanes one after another, keep only each lane's report, and discard its working
  notes. Running a lane inline in the caller's context is acceptable only for a single lane on a change of
  about 300 lines or fewer.

Done when every chosen lane has returned or its failure is recorded.

## 4. Verify the Bug Candidates

In a fresh sub-agent:

1. Merge the `bug` rows of lanes A, B, D, T, and E; deduplicate by location and cause. Never merge lane C.
2. Drop findings about the brief's known absences.
3. Rank by severity. For the top 8, reread the cited code and its callers and mark each `confirmed` (the
   failure follows from the code as written), `plausible` (depends on inputs or runtime state you cannot see),
   or `rejected` (the code handles it, or the lane's argument fails; quote the line).
4. Run a proof-path test only when it is cheap (CPU only, no datasets) and only from a scratch directory
   outside the repository.

Done when each of the top 8 carries a status and every `rejected` quotes its line.

## 5. Report in Tiers

Use [report-template.md](references/report-template.md). The human reads the first section only, so tier by
what happens if they skip an item, not by lane:

- **Must read** (5 or fewer): confirmed or plausible high-severity bugs; drifts or design choices that need
  the human's decision; security findings in `full` mode. One line each: location, problem, decision needed.
- **Worth reading** (10 or fewer): medium bugs, top design topics, missing key tests.
- **Appendix**: everything else, by lane.

Within a tier, list bugs and design separately; never rank one against the other. Under a lane that was off,
write one line saying why. State that the review was static and which findings were not run.

On Claude Code, optional hooks can log which files each lane opened and block an incomplete report; see
[claude-code-hooks.md](references/claude-code-hooks.md).

## Repeat Reviews

Stop after 3 rounds on the same change. From round 2, review only the diff since the previous round, and do
not repeat a finding the author already answered. When a real problem later turns out to have been missed,
add it to a miss list the user keeps, and check lane changes against that list before adopting them.
