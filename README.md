# Research Agent Kit

[中文](README.zh-CN.md) · English

Agent skills for machine-learning and graphics research, covering repository onboarding, experiments, implementation, handoffs, and academic presentations. Agents inspect the target project to establish its computing environment.

## Skills

| Skill | Purpose |
|---|---|
| [zhaorong-research-workflow](skills/zhaorong-research-workflow/SKILL.md) | Onboard a research repository, explore code and data, analyze experiments, and maintain the next research questions |
| [research-task-implementation](skills/research-task-implementation/SKILL.md) | Implement a research task from an agreed plan, with checklists and validation evidence |
| [paper-code-bootstrap](skills/paper-code-bootstrap/SKILL.md) | Set up a paper repository and verify a runnable inference path |
| [handoff](skills/handoff/SKILL.md) | Create or consume cross-agent work handoffs |
| [academic-slides](skills/academic-slides/SKILL.md) | Organize research narratives, visual evidence, and speaker notes; preserve editing boundaries and verify deliverables |
| [natural-expression](skills/natural-expression/SKILL.md) | Reduce repetition and formulaic language while respecting slide text, speech, and prose formats |
| [japanese-expression](skills/japanese-expression/SKILL.md) | Refine Japanese subjects, references, sentence connections, and spoken rhythm |

The README is available in Chinese and English. Each skill has one maintained text in its existing language. The three presentation and expression skills have Chinese instructions; the task determines the language of the output.

## Install the presentation and expression skills

Install these three modules together:

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s academic-slides natural-expression japanese-expression -y --copy
```

For writing tasks, `academic-slides` reads `natural-expression` and also reads `japanese-expression` when the text is Japanese. Layout-only edits do not load language modules. The language modules can also be used independently. This group does not require the research-code workflow.

Example requests:

```text
Use $academic-slides to review this presentation's narrative and speaker notes. Discuss changes before editing files.
Use $natural-expression to edit this prose, preserving its meaning while reducing repetition and formulaic language.
Use $japanese-expression to revise these Japanese speaker notes, preserving sentence connections and the scope of research claims.
```

## Install the research-code workflow

Start with the workflow and implementation modules:

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s zhaorong-research-workflow research-task-implementation -y --copy
```

In a new session that recognizes the skills, explicitly initialize the target repository:

```text
Use $zhaorong-research-workflow to initialize this existing research repository. Audit it and draft the repository workflow first; stop before configuring the project environment.
```

The workflow checks for Matt Pocock's engineering skills. If they are missing, review the workflow's explanation of the dependencies, then install them:

```sh
npx skills add mattpocock/skills -g -a codex -s '*' -y --copy
```

Resume initialization and run `$setup-matt-pocock-skills` when prompted. Establish the project rules and workflow before configuring the environment and compute jobs.

## Inspect and verify installation

List the available skills before installing:

```sh
npx skills add LarsPh/research-agent-kit -l
```

`-g` installs at user scope; `-a codex` selects Codex. If `npx skills` is unavailable, copy the selected folders under `skills/` into the target agent's user skill directory. Copy the presentation and expression modules together to preserve their relative references.

After installation, confirm the names in the target agent's available-skill list. If the list has not refreshed, check in a new session. Files on disk alone do not prove discovery.

## Research workflow

1. Discuss the next research question and update the directions to explore.
2. Select a bounded exploration task or an implementation task with an agreed plan.
3. Run tests and experiments, then inspect representative visuals.
4. Analyze observations, confounds, and claim boundaries.
5. Use the evidence to continue, pivot, defer, reject, or move into implementation and review.

Store raw outputs and checkpoints in the project's persistent artifact storage. Keep reviewed analysis and representative evidence in the repository.

## Project data and public boundaries

This repository holds reusable workflows and abstract examples. Machine configuration, job commands, mounts, data paths, credentials, and internal policies belong in the relevant private project. Research facts, current terminology, and agreed decisions for a presentation also remain in the project's own materials.
