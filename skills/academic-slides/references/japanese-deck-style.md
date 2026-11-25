# Japanese Deck Style

The user's own conventions for Japanese research decks, collected over review rounds, rehearsals, and lab
talks. They sit on top of the lab standard in [cgg-japanese-slides](../../cgg-japanese-slides/SKILL.md);
where the two disagree, the lab standard wins unless the user decides otherwise.

## Review rounds

- A reviewer marks only a few instances of each habit. For each comment, state the general rule, scan the
  whole deck for it, then fix the marked page.
- Keep a comparison table (comment → change → status) and re-check every row on the exported file before
  handing it over; never report a round as done with rows still open.
- Never merge, drop, or shorten slides to save time without listing the cuts and getting agreement. When a
  new rule overturns an old one, note which.
- Answer a reviewer's question first from what is already known, then make the change.

## Story

- When the field name is broad, add a page that classifies the field and marks where this work sits; the
  first question otherwise is how the field is defined.
- Keep parallel tasks symmetric: if one gets a definition, example, or difficulty page, so does the other.
- Related work: group by the analysis axes the papers themselves use. Show a method first, then reveal its
  problem by click; the reveal script starts with 「しかし」 and covers only what is new. When one method gets a
  detailed page, say why in the script and signal the return to the overview.
- Chapter summaries, the overall summary, and contributions carry result figures. Technical outlook and
  social application go on separate pages.
- Keep claim strength identical to the papers; state per metric who is best.

## Page layout

- Content starts directly under the message line; use leftover space by enlarging the figure.
- The same figure on consecutive pages keeps the same position and size.
- When a figure has several points, give each point its own call-out box next to the part it explains, with
  a short leader line; no numbered discs with a list beside the figure.
- Method pages use three layers: a top bullet with the purpose (and where the result is used later); the
  figure with each operation's text box directly above the part it explains; remaining explanations in a
  separate box, one line each. When converting a text-heavy page, first list where every old bullet goes
  (bullet, on-figure, box, script) so nothing is silently dropped.
- Size every box to its text with equal left and right padding, measured with the real fonts (including the
  space at Latin/CJK boundaries); no fixed or minimum box widths.

## Figures and colour

- Coined method names appear prominently at first mention, never first on a results page.
- Replace crude material (old screenshots, hand-drawn arrows, English labels, section numbers) with redrawn
  shapes and clean paper crops. Small generated assets inside a diagram are fine; a whole generated figure
  is not. Do not paint white patches over an original figure to write Japanese on it.
- Colour has one meaning each across the deck: orange for this work and its operations (dark orange for text
  on white), light red for problems and limitations, light green for merits, light grey for neutral.

## Tables and formulas

- Best result bold, second underlined.
- Name ablation rows by what was removed, in the words of the method pages, so each row points back to a
  page; avoid paper-internal labels.
- State speed-ups as multiples (「約 7,000 倍」) with raw times in the table. Numbers stay in tables; text
  gives the analysis. A main table may drop minor metrics if a backup slide has the full table.
- A formula either has every symbol explained on screen or is replaced by a qualitative explanation, with a
  hidden backup page carrying the labelled formula for questions.

## Animation mechanics

- The number of CLICK markers in the notes equals the number of click animations on the page; recount after
  every edit.
- Use native Appear animations, not duplicated slides. Multiple figures appear left to right in speaking
  order.

## Speaker script

- です・ます; 「〜させていただきます」 only at the opening and closing. Sentences of 40–60 characters, one idea
  each, 2–5 sentences per page; about 300 characters per minute.
- Point to the figure first, then state the conclusion (「左の図は〜です。〜を見ると〜」).
- Follow the slide's wording; update the script whenever the slide changes.
- Do not answer your own questions, write preview-only sentences, chain 「〜を実現しました」, use unsupported
  「非常に」「大幅に」, add sentences written only to satisfy a comment, name an example before it appears on
  screen, or read table headers one by one. Results pages give at most one representative number.
- Cover every item on the slide; trimming removes repetition, never information.
- Japanese wording and readings in the notes: see
  [slide wording](../../japanese-expression/references/slide-wording.md).

## Files, recording, presenting

- Back up before editing. Never overwrite a file someone has open; save as `_2`, `_3`, … and say so. Once
  the presenter edits the PPTX by hand, patch that file only.
- A recorded-narration deck is not re-recorded for edits: add With-Previous animations with delays from the
  recorded click timings, and verify by exporting video. Present from a copy with narration removed.
- After the last main slide: hidden backup slides, videos first, then Q&A slides labelled 「補足 n」 so main
  numbering and handouts stay unchanged. Renumber static page numbers after inserting a page and warn that
  printed handouts no longer match.
- Before the talk, prepare a quick-access folder (summary, slides, own papers, videos, Q&A notes), research
  each reviewer's field, and put the numbers and figures likely questions need on hidden Q&A slides.

## Checks before delivery

Measure the rendered pages with scripts: the gap between the message line and the first content row, the
left versus right padding of every box, and the slide-to-slide transitions after moving pages. Report the
numbers, then inspect every exported page.
