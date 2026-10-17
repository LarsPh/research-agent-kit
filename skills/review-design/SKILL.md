---
name: review-design
description: Read-only design and maintainability review that reports no bugs and gives the human options instead of verdicts. Looks at module boundaries, dependency direction, dead or single-value options, duplicated logic, naming, and test design, ranked by cost to a maintainer. Use alone before or after a large refactor, or as lane C of multilane-review.
---

# Review Design

Design has no answer key, so this review lays out choices for the human rather than ruling on them. Keep it
separate from bug hunting: in one shared output, bugs crowd design findings out.

## Protect the Target

Review read-only. Never edit, commit to, or push the target repository. Take the target from the user; ask
when none is named.

## 1. Get the Context

If a brief from multilane-review is provided, use it. Otherwise read the README, the architecture docs, and
the target file list, and note the module boundaries the docs state.

## 2. Check

Do not report bugs. Leave doc–code drift to review-intent-flow and test adequacy to review-tests. Look at:

- module boundaries and dependency direction (private access across modules, cycles);
- leftover or dead interfaces, options with a single legal value, options only tests use;
- duplicated logic that must stay in sync, and what breaks if one copy changes;
- names that no longer match behaviour;
- test design: tests that grep source, mock away the unit under test, or lock in implementation details.

## 3. Report

Group findings into topics, not lines, and rank topics by their cost to a maintainer over the next year.
500 words or fewer. For each topic give:

- evidence (`file:line`);
- why it matters;
- options: the simplest fix and at least one alternative, each with its cost. Recommend one when the case
  is clear, and say the choice is the human's.

End with "If you do only three things".

Done when every topic has evidence and at least two options.
