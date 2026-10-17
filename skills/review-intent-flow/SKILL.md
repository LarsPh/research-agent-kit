---
name: review-intent-flow
description: Read-only review of whether code still does what its docs say, end to end. Checks doc–code drift, missing or extra requirements, stage-to-stage path and format hand-offs along the README's main commands, and failures reported as success. Use alone to ask "does the documented workflow still work", or as lane D of multilane-review.
---

# Review Intent and Flow

Treat the repository docs as the statement of intent and check the code against them. Module-by-module
review misses problems that live between stages: one step writes a path the next step never reads, or a
failed stage still reports success.

## Protect the Target

Review read-only. Never edit, commit to, or push the target repository. Take the target from the user; ask
when none is named.

## 1. Get the Context

If a brief from multilane-review is provided, use it and do not reread the docs. Otherwise read the README,
the docs index and architecture docs, and the target file list, then note in 30 lines or fewer: the stated
purpose and requirements, the main command chain (the end-to-end commands the README tells a user to run, in
order, with the stage or script each invokes), and files the docs mention that are deliberately absent.

## 2. Check

1. **Doc–code drift.** Components, stages, APIs, or options the docs describe that the code no longer has,
   and the reverse. When the fix could go either way, name both (change the code, or change the doc) and
   leave the choice to the human.
2. **Requirements.** Requirements the docs state that the code does not meet, and features or flags the code
   adds beyond them. Matching the docs is not proof of correct math; leave formula checks to
   review-domain-bugs.
3. **Main command chain.** Walk it stage by stage. At each hand-off, check that the path, filename pattern,
   and format one stage writes are exactly what the next stage reads, including suffixes, ID zero-padding,
   and direction naming. Check that config defaults and CLI defaults agree, and that each documented example
   config or manifest would pass its loader.
4. **Failure reporting.** Exceptions caught and logged as warnings, `return` on missing input, exit code 0
   on failure, per-item errors swallowed so the run reports success. Say whether a failed stage is visible to
   the user.

Skip files the docs mention that are deliberately absent.

## 3. Report

One table, most severe first. 600 words or fewer.

| # | file:line (and doc line) | finding | kind | severity | evidence |
|---|---|---|---|---|---|

- `kind` is `bug` when a documented command or stage fails or silently does nothing; otherwise `drift` or
  `requirement`.
- `severity` is high, medium, or low.
- For a drift with two possible fixes, put both in `finding`.

When run alone, end with: "Static review; not verified by a second pass."

Done when every stage hand-off in the main command chain has been checked or listed as unchecked.
