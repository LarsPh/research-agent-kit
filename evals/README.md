# Evals

Scenario sets for testing skills with and without the skill loaded, following Anthropic's skill-authoring
guidance (build evaluations first, at least three scenarios, compare against a baseline). They live outside
`skills/` so installing a skill does not copy them.

Evals call models, cost tokens, and vary between runs, so CI does not run them. Run a skill's set by hand
before a large change to that skill, and record the result next to its scenarios.

| Skill | Status |
|---|---|
| [graphics-debug](graphics-debug/scenarios.md) | 3 scenarios with fixtures; run 2026-11-01 ([results](graphics-debug/results-2026-11-01.md)) |
| [multilane-review](multilane-review/scenarios.md) | scenarios drafted, not run |
| [research-task-implementation](research-task-implementation/scenarios.md) | scenarios drafted, not run |

## Running a Scenario

1. Build the fixture into a fresh directory per run.
2. Start one agent with the skill and one without, each in a fresh context, with the same prompt.
3. Grade each run against the scenario's expected behaviours; note the process differences as well as
   whether the answer is right.
