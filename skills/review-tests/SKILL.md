---
name: review-tests
description: Review whether a change's tests would actually catch it breaking, by mutation rather than by reading. Lists the documented behaviour and risky logic, mutates each point in a scratch copy and runs the tests, or does a paper mutation when the code cannot run, and names each missing test. Use after test-first development, or as lane T of multilane-review.
---

# Review Tests

Whether tests catch a regression is answered by experiment, not by reading: break the code on purpose and
see whether a test turns red. A mutation that stays green is a finding, and the finding names the missing
test.

## Protect the Target

Never edit, commit to, or push the target repository. Mutate only a copy in a scratch directory outside the
repository, and delete the copy when done. Take the target from the user; ask when none is named.

## 1. Get the Context

If a brief from multilane-review is provided, use it. Otherwise read the README, the docs that state
behaviour, the changed files, and the test layout.

## 2. Pick the Points

List 3–8 points where a wrong value would matter: behaviour the docs promise, and the riskiest logic in the
change. Prefer points a reader cannot check by eye: a sign or stencil direction, an inclusive versus exclusive
offset, a stage-to-stage path, a dtype, a default value. For each, write the mutation that would break it
(flip the sign, shift by one, change the path, drop a negation).

## 3. Run or Reason

- **Cheap to run** (CPU only, no datasets, the suite finishes in minutes): copy the repository to a scratch
  directory, apply one mutation at a time, run the relevant tests, record red or green, and restore before
  the next mutation.
- **Not cheap to run** (needs a GPU, a dataset, or long runs): do a paper mutation. For each point, name the
  test that should fail and quote the assertion that would catch it. If no such test exists, that is a
  finding, marked `not run`.

Also note tests that would pass for the wrong reason: assertions loose enough that an all-zero output
passes, mocks that replace the unit under test, and tests that grep source text.

## 4. Report

One table, most important first. 500 words or fewer.

| # | point (file:line) | mutation | result (red / green / not run) | missing or weak test |
|---|---|---|---|---|

Every `green` or `not run` row without a catching test is a finding. Mark its `kind` as `bug` when the
untested point is also wrong in the current code.

When run alone, end with: "Mutations run: N of M; the rest were reasoned, not run."

Done when every listed point has a result and every finding names the test that is missing.
