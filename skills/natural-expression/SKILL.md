---
name: natural-expression
description: Strip AI-sounding patterns and redundancy from prose and calibrate its tone, handling template phrasing, empty parallelism, defensive writing, and stacked punctuation against the user's own samples. Use when writing or polishing slide text, speaker scripts, body text, emails, or application materials; or when the user says text reads as templated, padded, or machine-written. Triggers include 润色, 去 AI 感, AI 味, 去冗, 语气.
---

# Natural Expression

## 1. Identify each text's purpose

Keep the user's target language, samples, and edit boundaries. Within one task, tell apart the different kinds of text:

| Purpose | Form to keep |
|---|---|
| Titles, bullets, captions | Short phrases, noun structures, needed parallel items; built for scanning |
| Spoken script | Natural sentences, fitting connectives, needed signposting; built for listening |
| Written body text | Full paragraphs, explicit logic, tone matched to the setting |

Done when each passage's purpose and allowed degree of change are clear. Text that already reads naturally can stay as it is.

## 2. Edit by what each piece of information does

Work on how information relates across the whole passage first, then on words and sentences. Keep facts, causality, scope, comparison dimensions, and the author's stance; ask about missing facts or mark them for verification.

| Pattern | Edit target and what to keep |
|---|---|
| Defensive writing | State the fact directly and drop self-justification that bears on nothing; keep conditions and limits that affect the conclusion, and genuine analysis of alternatives |
| Empty evaluation | Express the contribution through the concrete content already present; delete unsupported claims of significance |
| Empty parallelism | Merge synonymous items; list real multiple dimensions, steps, or results as usual |
| Template phrasing | Delete rhetorical question-then-answer, "not X but Y" contrasts (不是……而是……), previews (接下来我们将……), and summaries that add no information; keep real comparisons and needed signposting |
| Stacked punctuation | Organize body text through clear sentence relationships instead of chains of dashes, bars, and colons (——, ｜, ：); keep symbols that labels, technical names, units, and citations need |
| Editing residue | The final text holds only reader-facing content; raise working instructions and open questions separately with the user |

A contrast, a three-item list, or a punctuation mark on its own is no reason to edit. When keeping versus deleting is hard to call, read [edge cases](references/examples.md).

Done when every edit can be justified by an information or readability gain, beyond swapping synonyms, and nothing omitted loses a fact or inflates a claim.

## 3. Check, then deliver

Check that removing redundancy kept the needed connections and left the user's habits intact. [japanese-expression](../japanese-expression/SKILL.md) owns Japanese subjects and syntax; when this skill runs on its own and the text is Japanese, read that skill before writing or rewriting. If it is missing, say so and report its checks as not run.

Return the finished text the task needs plus the key changes; give scores, multiple drafts, or a full checklist only when asked. For file tasks, write back as the user requests; when embedded in another task, follow that task's delivery format.
