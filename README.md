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

## 学术报告与表达

以下三个 skill 的正文、说明和默认提示使用中文，成稿语言按任务决定：

- [`academic-slides`](skills/academic-slides/SKILL.md)：学术叙事、图文证据、台词衔接、改稿边界及交付核验。
- [`natural-expression`](skills/natural-expression/SKILL.md)：区分页面文字、口头稿与正文，减少模板表达和无效修辞。
- [`japanese-expression`](skills/japanese-expression/SKILL.md)：日语主语省略、清楚指代、句间连接及朗读节奏。

PPT 主 skill 在写作时读取通用表达模块，涉及日语再读取日语模块；语言模块也可独立使用。
建议一起安装以保持依赖完整；无需先初始化研究代码仓库，也不需要安装 Matt 的全部 skills：

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s academic-slides natural-expression japanese-expression -y --copy
```

例如：`用 $academic-slides 检查这份报告的叙事与台词，先讨论，不直接改文件。`
只有排版修改时不加载语言模块。案例均为抽象化示例，具体研究事实和术语放在项目自身资料中。

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
