# Research Agent Kit

[中文](README.zh-CN.md) · English

Agent skills for machine-learning and graphics research with Codex and Claude Code: repository onboarding,
experiments, implementation, research ledgers, packs for external planning models, remote-agent
coordination through Orca, and academic presentations. Agents inspect the target project to establish its
computing environment.

## How Skills Start

- **You invoke it**: name the skill in your request — `$skill-name` in Codex, `/skill-name` or the skill's
  name in Claude Code. These skills run a workflow you decide to start.
- **It can start from context**: the agent may load the skill on its own when the conversation matches its
  description; each description also lists a few Chinese keywords so Chinese conversations match too.
  Automatic loading does not always happen; name the skill when it matters.

## Skills You Invoke

| Skill | Purpose |
|---|---|
| [zhaorong-research-workflow](skills/zhaorong-research-workflow/SKILL.md) | Onboard a research repository, explore code and data, analyze experiments, and maintain the next research questions |
| [research-task-implementation](skills/research-task-implementation/SKILL.md) | Implement a research task from an agreed plan, with checklists and validation evidence; the workflow also starts it |
| [paper-code-bootstrap](skills/paper-code-bootstrap/SKILL.md) | Set up a paper repository and verify a runnable inference path |
| [research-pack](skills/research-pack/SKILL.md) | Pack a period of multi-branch reports, diffs, and inspected visuals for an external research LLM, and ingest its guidance |
| [academic-slides](skills/academic-slides/SKILL.md) | Shape a talk's storyline, figure evidence, and speaker script; change only what the user allows and check the final files |

## Skills That Also Start From Context

| Skill | Starts when | Purpose |
|---|---|---|
| [frontline-ledger](skills/frontline-ledger/SKILL.md) | a research line piles up results, open questions, or pending tasks; you ask where a line stands | Keep one running ledger per research line so chat reports only what changed |
| [orca-remote-bridge](skills/orca-remote-bridge/SKILL.md) | an agent runs inside Orca, or a message from another agent arrives | Let a desktop Codex/Claude app drive, question, and collect results from agents in Orca terminals on a remote SSH host |
| [natural-expression](skills/natural-expression/SKILL.md) | you write or polish prose, slides, or speeches; `academic-slides` loads it for writing tasks | Reduce repetition and formulaic language while respecting slide text, speech, and prose formats |
| [japanese-expression](skills/japanese-expression/SKILL.md) | the text is Japanese; `academic-slides` loads it for Japanese writing | Refine Japanese subjects, references, sentence connections, and spoken rhythm |

[templates/](templates/README.md) holds a shared `AGENTS.md` and a thin `CLAUDE.md` bridge for repositories
that Codex and Claude Code both work in.

## Install

`-g` installs at user scope. `-a` selects the agent: `codex` or `claude-code`.

Research-code workflow:

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s zhaorong-research-workflow research-task-implementation -y --copy
```

In a new session that recognizes the skills, initialize the target repository explicitly:

```text
Use $zhaorong-research-workflow to initialize this existing research repository. Audit it and draft the repository workflow first; stop before configuring the project environment.
```

The workflow checks for Matt Pocock's engineering skills. If they are missing, review the workflow's
explanation of the dependencies, then install them:

```sh
npx skills add mattpocock/skills -g -a codex -s '*' -y --copy
```

Resume initialization and run `$setup-matt-pocock-skills` when prompted. Establish the project rules and
workflow before configuring the environment and compute jobs.

Ledger, pack, and Orca bridge:

```sh
npx skills add LarsPh/research-agent-kit -g -a claude-code -s frontline-ledger research-pack orca-remote-bridge -y --copy
```

Install `orca-remote-bridge` both for the desktop app's agent and for the agents on the remote host; both
roles live in the same skill.

Presentation and expression (install together; `academic-slides` reads the expression skills by relative
reference, and layout-only edits load neither):

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s academic-slides natural-expression japanese-expression -y --copy
```

Example requests:

```text
Use $academic-slides to review this presentation's narrative and speaker notes. Discuss changes before editing files.
Use $natural-expression to edit this prose, preserving its meaning while reducing repetition and formulaic language.
Use $japanese-expression to revise these Japanese speaker notes, preserving sentence connections and the scope of research claims.
```

List the available skills before installing with `npx skills add LarsPh/research-agent-kit -l`. If
`npx skills` is unavailable, copy the selected folders under `skills/` into the agent's user skill directory
(for Claude Code, `~/.claude/skills/`). After installation, confirm the names in the agent's available-skill
list, in a new session if the list has not refreshed. Files on disk alone do not prove discovery.

## Research Workflow

1. Discuss the next research question and update the directions to explore.
2. Select a bounded exploration task or an implementation task with an agreed plan.
3. Run tests and experiments, then inspect representative visuals.
4. Analyze observations, confounds, and claim boundaries.
5. Use the evidence to continue, pivot, defer, reject, or move into implementation and review.

Store raw outputs and checkpoints in the project's persistent artifact storage. Keep reviewed analysis and
representative evidence in the repository.

## Project Data and Public Boundaries

This repository holds reusable workflows and abstract examples. Machine configuration, job commands,
mounts, data paths, credentials, and internal policies belong in the relevant private project. Research
facts, current terminology, and agreed decisions for a presentation also remain in the project's own
materials.
