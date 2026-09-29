# Research Agent Kit

中文 · [English](README.md)

面向机器学习与图形学研究的 agent skills，可在 Codex 和 Claude Code 中使用。内容包括：接手代码仓库、推进实验、实现任务、记录各研究线的进展、把成果打包给外部规划模型、通过 Orca 协调远端 agent，以及制作学术报告。计算环境由 agent 在具体项目中确认。

## Skill 如何启动

- **需要你主动调用**：在请求里写出 skill 名。Codex 用 `$skill-name`，Claude Code 用 `/skill-name` 或直接写名字。这类 skill 对应一段需要你决定何时开始的流程。
- **也能按上下文自动启动**：对话内容符合 skill 的说明时，agent 可能自行调用。每个说明末尾附有几个中文关键词，用中文对话也能匹配上。自动调用并不总会发生，重要的时候请直接写出 skill 名。

## 需要你主动调用的 skills

| Skill | 用途 |
|---|---|
| [zhaorong-research-workflow](skills/zhaorong-research-workflow/SKILL.md) | 接手研究仓库，探索代码和数据，分析实验，整理下一步要研究的问题 |
| [research-task-implementation](skills/research-task-implementation/SKILL.md) | 按已确定的方案实现一个研究任务，同时记录检查清单和验证结果；研究工作流也会调用它 |
| [paper-code-bootstrap](skills/paper-code-bootstrap/SKILL.md) | 配置论文代码仓库，确认推理流程能跑通 |
| [research-pack](skills/research-pack/SKILL.md) | 把一段时间内多个分支的报告、代码改动和结果图打包，发给外部模型讨论，并把对方的建议整理回项目 |
| [academic-slides](skills/academic-slides/SKILL.md) | 梳理报告的逻辑、图表证据和讲稿，只改用户允许改动的部分，并检查最终文件 |

## 也能按上下文自动启动的 skills

| Skill | 何时启动 | 用途 |
|---|---|---|
| [frontline-ledger](skills/frontline-ledger/SKILL.md) | 一条研究线的结果、待定问题或待办事项越积越多；你问某条线进展到哪一步 | 每条研究线维护一份持续更新的进展文档，对话里只汇报新变化 |
| [orca-remote-bridge](skills/orca-remote-bridge/SKILL.md) | agent 在 Orca 里运行，或收到其他 agent 发来的消息 | 让本地的 Codex/Claude 桌面应用给远端服务器上 Orca 终端里的 agent 派活、提问，并取回结果文件 |
| [natural-expression](skills/natural-expression/SKILL.md) | 撰写或润色正文、slides、讲稿；`academic-slides` 写作时会调用 | 按页面文字、讲稿和正文各自的用途删去冗余，减少套话 |
| [japanese-expression](skills/japanese-expression/SKILL.md) | 文本是日语；`academic-slides` 处理日语内容时会调用 | 调整日语的主语省略、指代、句间衔接和朗读节奏 |

[templates/](templates/README.md) 提供两份指令模板，适用于 Codex 和 Claude Code 同时使用的仓库：一份两边共用的 `AGENTS.md`，以及一份只写 Claude 专属规则、通过 `@AGENTS.md` 引用共用部分的精简 `CLAUDE.md`。

## 安装

`-g` 表示用户级安装；`-a` 指定 agent：`codex` 或 `claude-code`。

研究代码工作流：

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s zhaorong-research-workflow research-task-implementation -y --copy
```

打开一个能识别这些 skills 的新会话，明确要求初始化仓库：

```text
用 $zhaorong-research-workflow 初始化这个已有研究仓库。先审查并拟定仓库工作流，暂不配置项目环境。
```

工作流会检查是否装有 Matt Pocock 的工程类 skills。如果缺少，先看工作流对这些依赖的说明，再安装：

```sh
npx skills add mattpocock/skills -g -a codex -s '*' -y --copy
```

然后继续初始化，出现提示时运行 `$setup-matt-pocock-skills`。先定好项目规则和工作流，再配置项目环境和计算任务。

进展文档、成果打包与 Orca 远端协作：

```sh
npx skills add LarsPh/research-agent-kit -g -a claude-code -s frontline-ledger research-pack orca-remote-bridge -y --copy
```

`orca-remote-bridge` 要同时装在桌面应用和远端服务器两侧，两种角色写在同一个 skill 里。

报告与表达类（建议一起安装。`academic-slides` 会读取另外两个 skill，只调整版式时则不会）：

```sh
npx skills add LarsPh/research-agent-kit -g -a codex -s academic-slides natural-expression japanese-expression -y --copy
```

使用示例：

```text
用 $academic-slides 检查这份报告的叙事与台词，先讨论，不直接改文件。
用 $natural-expression 润色这段正文，保留原意，减少重复与模板表达。
用 $japanese-expression 修改这段日语台词，保留句间连接和研究结论的范围。
```

安装前可以用 `npx skills add LarsPh/research-agent-kit -l` 查看有哪些 skills。如果用不了 `npx skills`，把需要的 `skills/` 子目录复制到 agent 的用户 skill 目录即可（Claude Code 是 `~/.claude/skills/`）。装好后在 agent 的 skill 列表里确认能看到名字；列表没刷新就开一个新会话再看。文件在磁盘上不代表 agent 已经识别。

## 研究工作流

1. 讨论下一个研究问题，随实验结果更新待探索的方向。
2. 选择范围明确的探索任务，或方案已经确定的实现任务。
3. 运行测试和实验，亲自查看有代表性的结果图。
4. 分析观察到的现象、可能的干扰因素，以及结论能推广到什么范围。
5. 根据证据决定继续、转向、延期、放弃或进入实现与审阅。

原始输出和 checkpoint 放在项目的持久化存储里，仓库里只保留审阅过的分析和有代表性的证据。

## 项目资料与公开边界

本仓库只放通用流程和去掉具体信息的示例。机器配置、作业命令、挂载点、数据路径、凭据和内部规定都留在各自的私有项目里。报告涉及的研究事实、术语和已定决策，也以项目自己的文档为准。
