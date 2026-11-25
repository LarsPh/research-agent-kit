# Rules

Japanese in quotes is the corrected wording. Examples come from a 3D human rendering talk; apply the principle
behind each one to the deck at hand. Most rules serve one reader: someone from another field who has a few
seconds per page and sits at the back of a room.

## A. Text size and amount

- Every character is at least 20pt, page numbers included; older reviewers cannot read 9pt from the back. Raise all text by the same amount as the smallest, and grade sizes by importance.
- Small text leads to too much per page. A page is explained in a few seconds: a three-line sentence will not be read, and even two lines should be avoided.
- Break lines at meaningful positions, in English as well as Japanese; random breaks look careless. Do not break inside a phrase; for 「項目: 説明」 break right after the colon, the same way throughout.
- Do not leave one item on two lines when its neighbours take one; the odd item looks like two items.
- When a line overflows its box, tighten character spacing (about 0.5) and resize the box if needed; after trimming text, narrow the box and centre it again.

## B. Page structure and logic

- Put one sentence at the top left saying what the page claims; a figure alone does not say it.
- The title matches the whole page, not one corner of the figure.
- The first line of the body describes the whole page. On a setup page, say which datasets, metrics, and baselines are used, not 「比較」.
- State the subject (which method does this); without it a result reads as belonging to the wrong method.
- Each page follows from the previous one; say why this topic comes next.
- Explain a task (who, input, output, and any roles) before details that depend on it; details about an undefined task do not land.
- Introduce key concepts where they are first needed, prominently; a concept first explained near the end is too late.
- Narrow a broad limitation to the task in steps, without jumps; a sudden narrow application looks forced (e.g. 「服を変更できない」 before 「他人に着せる」). Each limitation maps to a part of the task name.
- A box titled 「共通の原因」 holds only the cause, not the remedy.
- Listing related approaches is not enough; say how each relates to this work. State the problem of existing approaches before the merit of the proposed one.
- Do not stress facts that invite "then why not use the other method?"; drop information the page does not need.
- Do not show the same layout on consecutive pages with slightly changed words: the change goes unnoticed.
- Do not split the same content into a top part and a bottom part; it makes the eyes travel.
- When step numbers are used, they match what the pages actually show; otherwise the numbering looks arbitrary.
- A page that rests on many premises is still hard to follow; cut the premises.

## C. Layout and whitespace

- Write explanations directly on the figure (call-outs, labels, leader lines), so the eye does not travel and nobody misses them in a short talk. No legends, no explanation far from its target, no small notes in a corner, no figure-left / text-right layout.
- Keep away from the slide edges. Keep the bottom band empty: in a room, the bottom of the screen is hard to see.
- Balance margins: no unexplained gaps, no content pushed against one side; move the block until top and bottom margins are about equal and the left margin is not cramped.
- Text never overlaps images, lines, or other text, and is never hidden by a figure.
- Align by centre: an image centred in its box; an arrow at half the height of the object it points from; a label midway between the boxes it belongs to. Misalignment looks careless.
- Keep figure-to-text spacing tight and the same on all pages.
- Put a figure below and make it larger; put its short explanation above it, side by side for two figures.
- Use 「・」 for every bulleted item on every page; do not use it for two lines that are one sentence. Without the mark, readers cannot tell two items from one wrapped sentence.
- Bold or colour only with a reason; unexplained emphasis makes the reader look for a meaning that is not there.

## D. Figures

- For outsiders, show background methods (e.g. NeRF, 3DGS) by the process the page talks about (usually inference / rendering) only, not the training pipeline; too much information in a figure blocks understanding.
- What is hard to picture from text gets a figure: concepts, regions, effects.
- Draw elements as what they are, and label them: e.g. a Gaussian as an ellipse dense at the centre and soft at the edge; a sparse volume not as a plain box; a network component not as a whole network. A misleading shape teaches the wrong idea.
- Every line has a stated meaning (if it is a ray, say so or make it an arrow); remove stray lines, since viewers try to interpret every mark.
- Connect related figures visibly (e.g. a line from a cross-section to the view it comes from, from a dashed frame to its label).
- Arrows have large heads and thick enough lines, and point exactly at their target.
- Rays and other 3D elements must look 3D: cut a ray where it meets the object, put the intersection near the object's middle, and draw the rest behind it. Otherwise the ray looks drawn on top of a flat picture.
- Label what each mark is (e.g. a dot on a ray is a サンプル), and point the label at the mark itself, not at the segment next to it.
- Use one icon per object throughout, drawn so its direction is visible (e.g. a side-view camera).
- Keep diagram elements no larger than needed; shrink wide figures toward what they explain.
- Show 360° rotation with an elliptical orbit around the object, the back half dashed and hidden behind it, not overlapping other boxes; a plain arc does not read as rotation. A rotating video is more convincing.
- Zoom insets: connect two corners of the small box to the large one with dashed lines, place the inset near its source, and hide unrelated parts inside it.
- Dashed lines use short intervals and are thick enough to see.
- Mark what to look at in result images (a frame around the region).
- Do not use example images that raise side questions (e.g. people in odd poses); reviewers will wonder why.
- Do not enlarge low-resolution results; their flaws show. When space is short, keep only the result that matters and enlarge that.
- Separate figures that make a different point with space, so they are not read as one group.
- Colours do not suggest a link that is not meant (e.g. reusing a chapter's colour for something unrelated).
- Two colours that must be told apart cannot both be thin lines drawn over a busy image.
- Do not cut off parts of the subject (e.g. a head) in figures.

## E. Tables and numbers

- Metrics carry ↑ or ↓.
- Units are not metrics: write 「計算時間 (ms) ↓」, not 「ms ↓」.
- Say what a number means for outsiders, with the number in parentheses: 「高速に描画可能 (… fps)」.
- Show where a derived number comes from, as one formula in one place.
- The bold / underline legend sits directly above or below the numbers.
- Make ○ and ✕ stand out: larger, bold, coloured.
- Put explanations above the table, not below with a duplicated heading.
- Put a difference between settings into the table itself (e.g. a row 「正解深度マップ」 with 「なし (使用しない)」 / 「あり (学習に使用)」) rather than in a sentence beside it.
- Each highlight frame comes with on-screen text saying what it shows, not only spoken words, because the audience may miss the speech; show each observation with its frame, or emphasise it when the frame appears.
- Explain any notation used in a table.
- Name the dataset on every result page, the same way on all of them; for figure grids, put row labels on the left, rotated 90°.
- Give each image in a comparison a caption (which one is the ground truth).

## F. Captions and citations

- Captions go below figures, throughout.
- Cite others' figures as 「図の出典: …」 with the paper only, no figure number; centre it under the figure.
- Do not cite one's own papers that the talk presents; nobody does, and it clutters the page.
- Do not attach a citation to every figure by rule; mechanical citations show the slides were made by AI without checking.
- Check that a one-line citation does not read as a contradiction (a result from one paper, image from another).

## G. Japanese notation and wording

- End items with nouns: drop the final 「する」 (体言止め), e.g. 「描画可能」「保持」「抑制」.
- No full-width parentheses or colons; use half-width ones. Full-width ones leave too much space.
- Put a half-width space between half-width and full-width characters; otherwise they look jammed together.
- Separate a label with a colon: 「指導教員: 」「考察 1: 」.
- Do not end every item with 「…ため」.
- Use the standard term: 「ボリュームレンダリング」; 「低解像度」; 「高速化」; 「利用場面」 not bare 「場面」; 「〜視点」 for camera counts; 「本研究」 throughout; 「破綻」; 「サンプリング範囲」; 「考察」 rather than colloquial headings; 「基盤モデル」 rather than 「大きなモデル」.
- Words must mean what is meant: 「再構成」 targets the real person, not an avatar; 「写っていない」 is wrong when nothing has been rendered yet; 「同一性」 compares two people, so for one person use 「人物同一性」 or 「Identity」; 「…の補完」 reads as fixing a deficient model, 「…の活用」 does not. Check that a verb fits its object in Japanese (e.g. 「首を載せる」 is not said).
- 「問題点」 needs the reason it is a problem; if only the item is given, call it 「課題」.
- Avoid colloquial phrases that can be misread (e.g. for 「訓練データに含まれていない人物」).
- Say what exactly is meant: what is calibrated, what is moved, what is aligned.
- Keep paired terms aligned (if the lower text says サンプル, the upper one does too).
- Write names and their explanations in one pattern throughout, e.g. 「Name (何をするか)」.

## H. Animation

- Use animation to match the explanation, one element at a time; show two arrows one by one when the script explains them one by one.
- Check the reveal order and that nothing is visible before its turn.
- A click that suddenly adds a lot of information outruns understanding; split it.
- A strong animation can make the audience forget the other things the page shows; restate those in text.

## I. Cover, ending, and delivery

- Cover: if the English title is the main one, put it above the Japanese title; break the English title at a natural point (e.g. after "And", capitalised).
- Affiliation: give only what the audience needs (e.g. the degree programme). Order: affiliation and year, then name, then supervisor (or name first); separate with a colon.
- Publication list: make one's own name stand out (bold plus a different colour from the other list text); call papers 「国際学術誌論文」「国際会議論文」, not 「論文誌」「会議録」.
- Summary: explain carefully how the central idea was used in each part; this is the core of a thesis talk.
- Outlook: describe what the field needs in the long term, not a personal plan or something already done; say why and what for.
- Every chapter has a place in an overview or positioning figure, and the sizes and positions of its marks follow a stated basis.
- Remove pages that do not add anything, such as a closing 「ご清聴ありがとうございました」 page.
- Slides follow the latest written document they present (e.g. the thesis summary); revise the slides to match it before sending.
- Speak loudly and clearly, and look at the reviewers, not at the PC or the screen.
- Printed handouts: 4 or 6 slides per page, double-sided.
