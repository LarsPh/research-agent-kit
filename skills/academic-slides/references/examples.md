# Academic Slides Edge Cases

These examples are abstracted and state no facts about any specific project. Example sentences stay in their original language; the notes around them explain the judgment.

## Polishing keeps the scientific meaning

- Input intent: 用图像模型生成观测，减少多帧误差累积。
- Faithful wording: 使用图像生成模型，目标是抑制跨帧偏差累积。
- Distorted wording: 无需训练昂贵的视频模型。
- Judgment: the distorted wording adds a claim about training cost and changes what the method is; go back to the input intent.

## Goals, observations, and conclusions

"本次样例在第 3 步开始出现接缝" keeps the claim scoped to this case; "该方法最多支持两步" needs additional evidence.
When the research moved from large to small camera motion because large-motion experiments were unstable, explain how the experiments led to the change; the original goal can stay as part of the research history.

"可选形式有 A 与 B" should read as a list of options, not as "使用 A 和 B 生成". "效果尚待验证" keeps its pending-verification status; do not turn it into "尚未开始验证". When motivation is expressed with 「狙い」, it needs no extra generic disclaimer.

## Dividing content and transitions

End of previous slide: "接下来考虑构建三维所需观测的形式。"
Start of next slide: "可选形式包括透视图和全景图。"
Both sentences discuss the same object, so the second picks up the first. If the previous slide already ends naturally, the next slide can start directly with its content; no extra preview is needed.

## Figures and cutting time

Three consecutive slides show the same kind of result: the first introduces input, output, and what to look for; each of the other two states one new phenomenon. Cut time this way, by removing repeated explanation, rather than by trimming connectives or asking the speaker to talk faster.
A single-slide results overview is laid out by the assets' aspect ratios; wide images and videos need not be squeezed into three equal columns. Add a zoom-in box only when the audience needs to compare a specific local region.

## Sources behind this skill

The main file's organization follows the steps, completion criteria, single source of truth, and on-demand reading principles of [Matt Pocock writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents); the figure-to-claim correspondence follows [Assertion–Evidence](https://writing.engr.psu.edu/assertion_evidence_EA.html). Titles need not all be conclusion sentences, and bullets remain allowed.
