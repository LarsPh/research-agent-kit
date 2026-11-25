# Rules

Source codes. Tier A (reviewer's own words): `V2-pN` = short comment on page N of version 2; `M` = the
reviewer's message on version 2. Tier B (review documents the reviewer prepared with an AI assistant and sent
as shared guidance; the reviewer noted that such text cannot be fully controlled): `R1`–`R3`, `T1`–`T4`, `F`
= the guidance document on version 2; `C1`–`C7` = the guidance document on version 1; `V2-pN+` = the
supplementary note attached to a version-2 comment. Version-2 guidance replaces version-1 guidance where
they differ (see A).

## A. Story and structure

- Show the motivation top-down. Derive the requirements from use cases, and give the reason for each
  condition (why only a few cameras, why interactive speed). Otherwise the requirements look chosen to fit
  the papers. `V2-p1` (「タスクの必要性の説明がやや強引」), `C1`, `T1`
- Say first what current technology lacks; map each topic to one lack; then state the problem the topics
  share. That shared problem is the reason for choosing these topics. `M` (「なぜこの 2 つのトピックを選んだ
  のか…説得力がまだ弱い」), `V2-p3`, `T1`
- Write each topic in one place. Per task: use case and requirement, input and output, what the input does
  not tell, and what that makes hard. Do not spread one topic over distant paragraphs. `M`, `V2-p1`
  (「1 段落で書く内容ではなく、分けた方がよい」), `R1`
- Treat parallel items the same way: if one task's input is defined, define the other's in the same form.
  `V2-p1` (「なんで second task についてだけ言及しているのか謎」)
- Do not put much related work in the introduction; it hides the main story. Keep one or two sentences on the
  broad approach per task there; move comparisons, mechanisms, and numbers to a related-work subsection at
  the start of each study's section. `M`, `V2-p1`, `R2`. This replaces the version-1 guidance to write the
  differences in the introduction (`C2`).
- Present two studies as complementary settings of one idea, not as two unrelated pieces; an unrelated look
  leaves a negative impression. State that they are parallel, not sequential. `V2-p3`, `C3`
- Do not assert the claim abstractly before the reader has what is needed to understand it; abstract early
  claims raise the reader's load. State it concretely after the background and the contribution figure, in
  terms of what the body model provides in each study. `V2-p2`, `T3`
- Put the central claim in the introduction, not first in the conclusion; describe the difference from prior
  work as a difference in how the shared tool is used. `C2`

## B. Readability

- Do not let 「this」「the claim」「the first」 point to text far back; readers, especially outside the field,
  cannot find the referent. Group the topic instead, and name things concretely (study names instead of
  「the first」「the task」). `M`, `V2-p1`, `V2-p2`, `V2-p3`, `R1`
- Call the same thing by the same name (「a few calibrated cameras」 vs 「sparse input images」). `V2-p1`,
  `C4`
- Say what problem a fact leads to, right where the fact is stated. `V2-p1`
- State a problem independently of a method the reader has not met yet. `V2-p1`
- Expand an abbreviation at its first use, and use it only after that. `V2-p2`, `V2-p3`
- Introduce a key tool before it appears anywhere else (figures, captions, earlier paragraphs). `V2-p2`

## C. Self-contained background and figures

- Give examiners outside the field a self-contained explanation of the key tool (here, the parametric body
  model) in its own subsection, with a figure, not text only. `M`, `V2-p1`, `T2`
- Give the main contribution a figure. A diagram of text boxes and lines is too abstract for a first-time
  outside reader; show concretely what the tool does in each method. `M`, `V2-p2`, `R3`
- Technical phrases (「bounds ray sampling」「informs visibility」) need a figure; keep the sentence plain.
  `V2-p2`, `V2-p2+`
- Every line in a diagram has a meaning; use arrows where direction is meant. Labels distinguish what
  actually differs (number of views, not "multi-view" twice). `V2-p2`

## D. Claims and evidence

- Do not just list what was done; abstract it one level and say what was achieved across the studies; two
  papers joined together are not a thesis. `M`, `T3`
- Describe the evaluation accurately: if both studies compare quantitatively, do not write it so that one
  looks quantitative-only and the other qualitative-only. `V2-p3`
- Match each claim to its evidence, per dataset and metric. `C5`
- Keep figures and text consistent (section numbers, labels). `C6`, `F`

## E. Conclusion

- Use a weightier verb for the overall result (「has demonstrated」). `V2-p8`
- Label limitations as limitations (a heading or an opening sentence) and use the word 「limitations」.
  `V2-p9`, `T4`
- Beyond near-term limitations and future work, give a long-term outlook for the field. `M`, `V2-p9`, `T4`
- State the conditions under which the claim does not hold. `C7`

## F. Figures, tables, wording

- The first sentence of a teaser caption speaks about the whole thesis. `V2-p1`
- Do not leave notes about how a figure was changed from its source; write 「adapted from [n]」. `V2-p1`
- Table captions go above tables, in every table. `V2-p2`, `V2-p5`, `V2-p6`
- Use the standard term (「ablation studies」). `V2-p3`
