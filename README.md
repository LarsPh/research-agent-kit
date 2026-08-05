# Research Agent Kit

Platform-neutral Codex skills for evidence-driven machine-learning and graphics research. The kit supports
existing-repository onboarding, rolling exploratory sprints, decision-complete implementation, and agent
handoffs without assuming a particular compute platform.

## Skills

- `zhaorong-research-workflow` — initialize a migrated research repository, explore code and new data,
  manage a rolling frontier, analyze experiments, and trigger implementation/review at the right boundary.
- `research-task-implementation` — implement one decision-complete research bite from its authority document
  while maintaining checklist and validation evidence.
- `paper-code-bootstrap` — bootstrap an external paper repository and validate a runnable inference path.
- `handoff` — create or consume concise cross-agent handoffs.

## Recommended Installation Order

Install the workflow and implementation skills at user scope first:

```fish
npx skills add LarsPh/research-agent-kit -g -a codex -s zhaorong-research-workflow research-task-implementation -y --copy
```

Then start a fresh Codex session and initialize the target repository explicitly:

```text
Use $zhaorong-research-workflow to initialize this existing research repository. Audit first, draft the
repository workflow, and stop before configuring the project environment.
```

The workflow will check for Matt Pocock's engineering skills. When they are absent, install them after the
workflow has explained why they are needed:

```fish
npx skills add mattpocock/skills -g -a codex -s '*' -y --copy
```

Restart Codex again, resume the repository initialization, and run `$setup-matt-pocock-skills` when prompted.
The project-specific environment and compute workflow come only after repository authority is initialized
and reviewed.

To inspect the package before installation:

```fish
npx skills add LarsPh/research-agent-kit -l
```

If `npx skills` is unavailable, copy only the selected folders under `skills/` into the Codex user skill
directory. Restart Codex and verify that both names appear in the available-skill list. File presence alone
does not prove discovery.

## Workflow Shape

The workflow deliberately avoids a fixed all-stage plan:

1. discuss the next research question and record a rolling frontier;
2. choose a bounded exploration or a decision-complete implementation bite;
3. run truthful tests/experiments and inspect representative visuals;
4. analyze observations, confounds, and claim boundaries;
5. continue, pivot, defer, reject, or promote through a risk-based review node.

Raw outputs and checkpoints belong in the target platform's discovered persistent artifact store. Only
reviewed analysis and representative evidence should enter Git.

## Public/Private Boundary

Keep this repository generic and public. Site-specific images, job commands, mounts, caches, data paths,
secrets, and internal policies belong only in the private target repository after the workflow has explored
the real environment.
