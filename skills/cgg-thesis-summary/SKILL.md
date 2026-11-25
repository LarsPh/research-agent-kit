---
name: cgg-thesis-summary
description: Applies a house standard, taken from written reviewer comments, to an English doctoral thesis summary read by examiners outside the field, covering top-down motivation, one claim across the studies, topics written in one place, self-contained background with figures, a figure for the main contribution, field-level outlook, and figure and table conventions. Use when drafting, revising, or checking a thesis summary, the introduction or conclusion of a thesis, or a review document for examiners. Triggers include 論文概要, 博論概要, thesis summary, 摘要.
---

# CGG Thesis Summary

This skill holds only rules that a reviewer gave while marking two versions of a ten-page English thesis
summary. Each rule in [rules](references/rules.md) carries its source code and its tier: the reviewer's own
short comments and message (tier A), or review documents the reviewer prepared with an AI assistant and sent
as shared guidance (tier B). Prefer A when the two differ. Sentence-level polish belongs to
[natural-expression](../natural-expression/SKILL.md).

Most examiners are outside the field. They judge whether the thesis tells one story and whether it reads
easily; the introduction and the conclusion matter most.

## 1. Fix the story before rewriting

Write the introduction and conclusion as one sentence per paragraph first, following
[story order](references/rules.md#a-story-and-structure), and agree on it with the supervisor before
rewriting prose.

Done when the outline answers: what current technology lacks, why these topics, what the shared problem is,
what the thesis claims, and how each study tests it.

## 2. Apply the rules by area

| Area | Covers |
|---|---|
| A. Story and structure | top-down motivation, topic grouping, related work placement, one claim |
| B. Readability | references to distant text, consistent names, defined terms, consequences |
| C. Self-contained background and figures | body-model section, a contribution figure, meaningful diagrams |
| D. Claims and evidence | claims matching numbers, studies named, evaluation described accurately |
| E. Conclusion | what was achieved, labelled limitations, long-term outlook |
| F. Figures, tables, wording | teaser caption, table captions above, standard terms |

Done when each edited paragraph satisfies the rules of every area it touches.

## 3. Report

List the rules applied and any rule that conflicts with a decision the user made (for example a point where
the user disagrees with the reviewer about a fact). Do not present tier B guidance as the reviewer's own
words, and do not add rules without a source code.
