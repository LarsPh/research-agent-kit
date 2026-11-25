# Rules

## A. Story and structure

- Show the motivation top-down. Derive each requirement from a use case and give the reason for every
  condition (why few inputs, why real-time). Requirements without reasons look chosen to fit the results.
- Say first what current technology lacks, map each problem or contribution to one lack, then state what
  the problems share. That shared problem is why these problems were chosen.
- Write each topic in one place. For each problem: use case and requirement, input and output, what the
  input does not tell, and what that makes hard. Do not spread one topic over distant paragraphs, and do not
  pack background, several requirements, and definitions into one paragraph.
- Treat parallel items the same way: if one problem's input is defined in its own sentence, define the
  other's in the same form.
- Keep related work out of the introduction except for one or two sentences on the broad approach per
  problem; detailed comparisons, mechanisms, and numbers hide the main story. Put them in a related-work
  section or at the start of the section they concern.
- Present several studies or contributions as complementary settings of one idea, not as unrelated pieces,
  and say whether they are parallel or sequential.
- Do not assert the claim abstractly before the reader has what is needed to understand it. State it
  concretely after the background and the main figure, saying what the key idea provides in each setting.
- Put the central claim in the introduction, not first in the conclusion, and describe the difference from
  prior work precisely (for a shared tool, the difference is how it is used).

## B. Readability

- Do not let "this", "the claim", "the first", or "the task" point to text far back; outside readers cannot
  find the referent. Group the topic instead, and name things concretely (method or study names).
- Call the same thing by the same name throughout ("a few calibrated cameras" and "sparse input images" read
  as two things).
- When stating a fact, say right there what problem it leads to.
- State a problem independently of a method the reader has not met yet.
- Expand every abbreviation at its first use and use it only after that.
- Introduce a key tool or concept before it appears anywhere else, including figures and captions.

## C. Background and figures

- Give outside readers a self-contained explanation of the key tool the work relies on, in its own
  subsection and with a figure, not text only.
- Give the main contribution a figure that shows concretely what happens. A diagram of text boxes and lines
  is too abstract for a first-time reader.
- When a sentence needs technical phrases to explain a mechanism, show it in a figure and keep the sentence
  plain.
- Every line in a diagram has a meaning; use arrows when a direction is meant. Labels name what actually
  differs between items (for example the number of views, not "multi-view" twice).

## D. Claims and evidence

- Do not only list what was done; abstract it one level and say what was achieved across the work. Two
  papers joined together are not a thesis.
- Describe the evaluation accurately. If both parts compare quantitatively, do not write it so that one
  looks quantitative-only and the other qualitative-only.
- Match the strength of each claim to its evidence, per dataset and metric.
- Keep figures and text consistent: section numbers, labels, names.

## E. Conclusion

- Use a verb with weight for the overall result ("has demonstrated").
- Mark limitations as limitations, with a heading or an opening sentence, and call them "limitations".
- State the conditions under which the claim does not hold.
- Beyond near-term limitations and future work, give a long-term outlook for the field, not a personal plan.

## F. Figures, tables, wording

- The first sentence of a teaser caption speaks about the whole work, not about the figure's contents.
- Do not leave notes on how a figure was changed from its source; write "adapted from [n]".
- Table captions go above tables, in every table.
- Use the standard term ("ablation studies", not invented variants).
