# Research Agent Kit

中文 · [English](README.md)

面向机器学习与图形学研究的 agent skills，适用于 Codex 和 Claude Code：接手代码仓库、推进实验、实现任务、维护研究台账、为外部规划模型打包、通过 Orca 协调远端 agent，以及学术报告。具体计算环境由 agent 在项目中确认。

## Skill 如何启动

- **需要你主动调用**：在请求里点名 skill——Codex 用 `$skill-name`，Claude Code 用 `/skill-name` 或直接写 skill 名。这类 skill 执行一段由你决定开始的流程。
- **也能按上下文自动启动**：对话内容与 skill 的 description 相符时，agent 可能自行加载（每个 description 末尾附有几个中文触发词）。自动加载不保证发生，重要时请直接点名。

## 需要你主动调用的 skills

| Skill | 用途 |
|---|---|
| [zhaorong-research-workflow](skills/zhaorong-research-workflow/SKILL.md) | 接手研究仓库，探索代码和数据，分析实验，维护下一步研究问题 |
| [research-task-implementation](skills/research-task-implementation/SKILL.md) | 根据已确定的方案实现一个研究任务，记录检查项和验证证据；工作流也会调用它 |
| [paper-code-bootstrap](skills/paper-code-bootstrap/SKILL.md) | 配置论文代码仓库，验证可运行的推理流程 |
| [research-pack](skills/research-pack/SKILL.md) | 把一段时间内多分支的报告、diff 和已检查的图打包给外部研究 LLM，并接收其回传的指导 |
| [academic-slides](skills/academic-slides/SKILL.md) | 组织学术叙事、图文证据与台词，保护改稿边界并核验交付 |

## 也能按上下文自动启动的 skills

| Skill | 何时启动 | 用途 |
|---|---|---|
| [frontline-ledger](skills/frontline-ledger/SKILL.md) | 一条研究线积累了结果、未决问题或待办；你问某条线进展到哪 | 每条研究线维护一份滚动台账，对话只报增量 |
| [orca-remote-bridge](skills/orca-remote-bridge/SKILL.md) | agent 运行在 Orca 中，或收到其他 agent 带标记的消息 | 让桌面端 Codex/Claude app 驱动、询问远端 SSH 主机上 Orca 终端里的 agent，并拉回结果 |
| [natural-expression](skills/natural-expression/SKILL.md) | 撰写或润色正文、slides、台词；`academic-slides` 写作时加载 | 按页面文字、口头稿和正文的用途去冗，减少模板表达 |
| [japanese-expression](skills/japanese-expression/SKILL.md) | 文本是日语；`academic-slides` 处理日语写作时加载 | 调整日语主语省略、指代、句间连接与朗读节奏 |

[templates/](templates/README.md) 提供两边共用的 `AGENTS.md` 和很薄的 `CLAUDE.md` 桥接模板，适用于 Codex 与 Claude Code 同时工作的仓库。

## 安装

`-g` 表示用户级安装；`-a` 指定 agent：`codex` 或 `claude-code`。

研究代码工作流：

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s zhaorong-research-workflow research-task-implementation -y --copy
```

在能识别这些 skills 的新会话中，明确启动仓库初始化：

```text
用 $zhaorong-research-workflow 初始化这个已有研究仓库。先审查并拟定仓库工作流，暂不配置项目环境。
```

工作流会检查 Matt Pocock 的工程 skills。缺失时，先确认工作流说明的依赖用途，再安装：

```sh
npx skills add mattpocock/skills -g -a codex -s '*' -y --copy
```

继续初始化，并在提示时运行 `$setup-matt-pocock-skills`。先确认项目规则与工作流，再配置项目环境和计算任务。

台账、打包与 Orca 桥接：

```sh
npx skills add LarsPh/research-agent-kit -g -a claude-code -s frontline-ledger research-pack orca-remote-bridge -y --copy
```

`orca-remote-bridge` 需要同时装给桌面 app 的 agent 和远端主机上的 agent；两种角色在同一个 skill 里。

报告与表达（建议一起安装；`academic-slides` 通过相对引用读取两个表达 skill，纯布局修改不加载它们）：

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s academic-slides natural-expression japanese-expression -y --copy
```

使用示例：

```text
用 $academic-slides 检查这份报告的叙事与台词，先讨论，不直接改文件。
用 $natural-expression 润色这段正文，保留原意，减少重复与模板表达。
用 $japanese-expression 修改这段日语台词，保留句间连接和研究结论的范围。
```

安装前可用 `npx skills add LarsPh/research-agent-kit -l` 列出仓库中的 skills。若无法使用 `npx skills`，可将选中的 `skills/` 子目录复制到目标 agent 的用户 skill 目录（Claude Code 为 `~/.claude/skills/`）。安装后在 agent 的可用 skill 列表中确认名称，列表未刷新时开新会话检查；仅看到文件存在不代表已被识别。

## 研究工作流

1. 讨论下一个研究问题，维护随实验更新的待探索方向。
2. 选择范围明确的探索任务，或方案已经确定的实现任务。
3. 运行测试和实验，检查代表性结果图。
4. 分析观察、混杂因素与结论边界。
5. 根据证据决定继续、转向、延期、放弃或进入实现与审阅。

原始输出和检查点存入项目所用的持久化存储；仓库中保留经过审阅的分析与代表性证据。

## 项目资料与公开边界

本仓库保存通用流程和抽象化案例。机器配置、作业命令、挂载、数据路径、凭据及内部政策留在对应的私有项目中。报告中的研究事实、当前术语和已确认决定也由项目自身资料维护。
