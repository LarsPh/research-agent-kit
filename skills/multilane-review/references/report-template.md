# Report Template

Keep every heading. Under a lane that was off, write one line: `Off: <reason from the plan>`.

```markdown
## Plan

Lanes on, lanes off with the reason, lane E mode, and how the defaults were chosen.

## Must Read (5 or fewer)

Bugs:
1. `file:line`: problem. Status. Decision or action needed.

Decisions:
1. `file:line` / doc line: the choice (for example: change the code or change the doc), options, and the
   recommended one.

## Worth Reading (10 or fewer)

Medium bugs, top design topics, and missing key tests, one line each.

## Appendix

### Bugs (verified)

| # | file:line | issue | lane | status | proof path |
|---|---|---|---|---|---|

Unverified or below the top 8: short list.

### Intent and Flow (lane D)
### Tests (lane T)
### Operations and Security (lane E)
### Design (lane C)

Ranked topics with options, then "If you do only three things".

## Coverage

Files each lane opened versus files in the target; anything no lane read. State that the review was static
and name the findings whose proof path or mutation was not run.
```
