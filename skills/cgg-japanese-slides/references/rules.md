# Rules

Source codes: `S1`, `S2`, `S3`, `S5` = written comments on review rounds 1, 2, 3, and 5 of one deck, with the
page (`S2-p54`); `M` = the reviewer's message sent with round 1; `O` = an oral comment relayed by the
presenter. A rule marked "(also …)" was repeated on other pages. Japanese in quotes is the reviewer's
wording or the corrected wording.

## A. Text size and amount

- Every character is at least 20pt, page numbers included; older reviewers cannot read 9pt. Raise all text
  by the same amount as the smallest, and grade sizes by importance. `S1-p1`
- Small text leads to too much per page. A page is explained in a few seconds: a three-line sentence will
  not be read, and even two lines should be avoided. `S1-p1`, `S1-p18`, `S2-p75`
- Break lines at meaningful positions, in English as well as Japanese; random breaks look careless. Do not
  break inside a phrase; for 「項目: 説明」 break right after the colon, the same way throughout. `S1-p1`,
  `S1-p14`, `S2-p30`
- Do not leave one item on two lines when its neighbours take one. `S2-p75`
- When a line overflows its box, tighten character spacing (about 0.5) and resize the box if needed; after
  trimming text, narrow the box and centre it again. `S3-p1`, `S3-p38`, `S3-p10`

## B. Page structure and logic

- Put one sentence at the top left saying what the page claims; a figure alone does not say it. `S1-p15`,
  `S1-p53`, `S1-p61`
- The title matches the whole page, not one corner of the figure. `S1-p37`
- The first line of the body describes the whole page. On a setup page, say which datasets, metrics, and
  baselines are used, not 「比較」. `S1-p43`
- State the subject: which method does this. `S1-p44`, `S1-p65`
- Each page follows from the previous one; say why this topic comes next. `S2-p10`
- Explain a task (who, input, output; roles such as User / Model) before details that depend on it.
  `S2-p10`, `S2-p13`, `S2-p18`
- Introduce key concepts where they are first needed, prominently; a concept first explained near the end is
  too late. `S1-p70`, `S2-p50`, `S2-p71`
- Narrow a limitation in steps to the task, without jumps (「服を変更できない」 rather than suddenly
  「他人に着せる」). Each limitation maps to a part of the task name. `S2-p9`, `S3-p9`
- A box titled 「共通の原因」 holds only the cause, not the remedy. `S3-p10`
- Listing related approaches is not enough; say how each relates to this work. State the problem of existing
  approaches before the merit of the proposed one. `S1-p27`, `S2-p53`
- Do not stress facts that invite "then why not use the other method?"; drop information the page does not
  need. `S1-p52`
- Do not show the same layout on consecutive pages with slightly changed words: the change goes unnoticed.
  `S2-p16`
- Do not split the same content into a top part and a bottom part; it makes the eyes travel. `S2-p24`
- When step numbers are used, the steps must match what the pages actually show. `S2-p37`
- A page that rests on many premises is still hard to follow; cut the premises. `S3-p62`

## C. Layout and whitespace

- Write explanations directly on the figure (call-outs, labels, leader lines). No legends, no explanation
  far from its target, no small notes in a corner, no figure-left / text-right layout. `S1-p36`, `S1-p45`,
  `S1-p56`, `S1-p57`, `S1-p62` (also `S2-p30`, `S2-p54`, `S2-p56`, `S2-p76`)
- Keep away from the slide edges. Keep the bottom band empty: in a room, the bottom of the screen is hard to
  see. `S1-p35`, `S2-p26`, `S2-p54`, `S2-p61`, `S5-p56`
- Balance margins: no unexplained gaps, no content pushed against one side; move the block until top and
  bottom margins are about equal and the left margin is not cramped. `S2-p15`, `S2-p26`, `S2-p33`,
  `S2-p57`, `S3-p1`, `S3-p57`
- Text never overlaps images, lines, or other text, and is never hidden by a figure. `S2-p10`, `S2-p27`,
  `S2-p29`, `S1-p59`
- Align by centre: an image centred in its box; an arrow at half the height of the person it points from; a
  label midway between the boxes it belongs to. `S2-p29`, `S5-p16`, `S5-p49`
- Keep figure-to-text spacing tight and the same on all pages. `S3-p45`, `S3-p46`
- Put a figure below and make it larger; put its short explanation above it, side by side for two figures.
  `S1-p20`, `S1-p25`
- Use 「・」 for every bulleted item on every page; do not use it for two lines that are one sentence.
  `S2-p56`, `S2-p76`
- Bold or colour only with a reason. `S2-p57`

## D. Figures

- For outsiders, show background methods (NeRF, 3DGS) by their inference / rendering process only, not the
  training pipeline; too much information in a figure blocks understanding. `S1-p6`, `S1-p8`
- What is hard to picture from text gets a figure: concepts, regions, effects. `S1-p8`, `S1-p31`, `S1-p50`,
  `S1-p56`, `S2-p39`, `S2-p50`
- Draw elements as what they are: label an ellipse as a Gaussian and shade it dense at the centre and soft at
  the edge; a sparse volume should not look like a plain box; a network part should not look like a whole
  network. `S2-p8`, `S2-p37`, `S2-p39`
- Every line has a stated meaning: if it is a ray, say so or make it an arrow; remove stray lines. `S2-p36`,
  `S2-p63`, `S2-p73`
- Connect related figures visibly (a line from the cross-section to the 2D person, from a dashed frame to its
  label). `S2-p15`, `S2-p36`, `S2-p38`
- Arrows have large heads and thick enough lines, and point exactly at their target. `S1-p36`, `S2-p63`,
  `S5-p29`, `S5-p53`
- Rays must look 3D: cut the ray where it meets the person, put the intersection at the belly, and draw the
  rest behind the person. Avoid flat illustrations that make rays look drawn on top. `S1-p10`, `S1-p11`,
  `S2-p6`, `S3-p6`, `S3-p11`
- Label what a dot on a ray is (サンプル), and point the label at the dot, not at a segment. `S2-p11`, `S3-p11`
- Use one camera icon that shows direction (for example a side view) throughout. `S1-p11`, `S2-p50`
- Keep rays and figures no larger than needed; shrink wide figures toward what they explain. `S2-p50`,
  `S3-p35`
- Show 360° rotation with an elliptical orbit around the person; the back half dashed and hidden behind the
  person; the arrow must not overlap other boxes. A rotating video is more convincing. `S2-p78`, `S3-p77`,
  `S5-p17`, `S5-p77`
- Zoom insets: connect two corners of the small box to the large one with dashed lines, place the inset near
  its source, and hide unrelated parts inside it. `S2-p41`, `S3-p40`
- Dashed lines use short intervals and are thick enough to see. `S2-p52`, `S3-p69`
- Mark what to look at in result images (a frame around the region). `S1-p60`, `S1-p63`, `S3-p69`
- Do not use example people in odd poses; reviewers will wonder why. `S1-p10`, `S1-p13`, `S2-p15`
- Do not enlarge low-resolution results; their flaws show. When space is short, keep only the proposed
  method's result and enlarge it. `S2-p33`, `S2-p50`
- Separate figures that show a different point (e.g. occlusion only) with space. `S2-p41`
- Colours do not suggest a link that is not meant (a colour shared with a chapter). `S2-p16`
- Two colours that must be told apart (inside / outside) cannot both be thin lines drawn over a mesh.
  `S2-p59`
- Do not cut off parts of people in figures. `S1-p34`, `S2-p57`

## E. Tables and numbers

- Metrics carry ↑ or ↓. `S1-p48`
- Units are not metrics: 「計算時間 (ms) ↓」. `S2-p44`
- Explain what a number means to outsiders: 「高速に描画可能 (… fps)」. `S2-p17`
- Show where a derived number comes from, as one formula in one place. `S2-p11`
- The bold / underline legend sits directly above or below the numbers. `S2-p44`, `S2-p65`
- Make ○ and ✕ stand out: larger, bold, coloured. `S1-p26`
- Put explanations above the table, not below with a duplicated heading. `S3-p29`
- Put the difference into the table itself (a row such as 「正解深度マップ」 with 「なし (使用しない)」 /
  「あり (学習に使用)」) rather than in a sentence beside it. `S2-p43`, `S3-p42`
- Each highlight frame comes with on-screen text saying what it shows, not only spoken words; show each
  observation with its frame, or emphasise it when the frame appears. `S3-p43`, `S3-p47`
- Explain any notation used in a table. `S2-p49`
- Name the dataset on every result page, the same way on all of them; for figure grids, put row labels on
  the left, rotated 90°. `S2-p46`, `S2-p47`, `S2-p70`, `S3-p44`
- Give each image in a comparison a caption (which one is the ground truth). `S2-p41`, `S2-p61`

## F. Captions and citations

- Captions go below figures, throughout. `S1-p18`, `S2-p61`, `S2-p66`–`S2-p70`
- Cite others' figures as 「図の出典: …」 with the paper only, no figure number; centre it under the figure.
  `S1-p6`, `S2-p58`
- Do not cite one's own papers included in the thesis; nobody does. `S1-p8`, `S1-p44`
- Do not attach a citation to every figure by rule; it shows the slides were made by AI. `S1-p53`
- Check that a one-line citation does not read as a contradiction (a result from one paper, image from
  another). `S3-p76`

## G. Japanese notation and wording

- End items with nouns: drop the final 「する」 (体言止め). `S1-p1`; e.g. 「描画可能」「保持」「抑制」 `S1-p33`
- No full-width parentheses or colons; use half-width ones. `S1-p1`
- Put a half-width space between half-width and full-width characters. `S1-p45`
- Separate a label with a colon: 「指導教員: 」「考察 1: 」. `S1-p1`, `S5-p47`
- Do not end every item with 「…ため」. `S1-p33`
- Use the standard term: 「ボリュームレンダリング」 `S1-p6`; 「低解像度」 `S1-p20`; 「高速化」 `S1-p20`;
  「利用場面」 not bare 「場面」 `S1-p9`; 「〜視点」 for camera counts `S1-p9`; 「本研究」 throughout `S1-p30`;
  「破綻」 `S3-p28`; 「サンプリング範囲」 `S2-p34`; 「考察」 rather than colloquial headings `S2-p48`;
  「頂点の変位」 `S2-p59`; 「基盤モデル」 rather than 「大きなモデル」 `S1-p76`.
- Words must mean what is meant: 「再構成」 targets the real person, not an avatar `S1-p53`; 「写っていない」
  is wrong when nothing has been rendered yet `S1-p10`; 「同一性」 compares two people, so for one person use
  「人物同一性」 or 「Identity」 `S3-p17`; 「…の補完」 reads as fixing a deficient model, 「…の活用」 does not
  `S2-p31`; 「首を載せる」 is not said `S3-p60`.
- 「問題点」 needs the reason it is a problem; if only the item is given, call it 「課題」. `S2-p28`,
  `S3-p70`
- Avoid colloquial phrases that can be misread (e.g. for 「訓練データに含まれていない人物」). `S1-p31`
- Say what exactly is meant: what is calibrated, what is moved, what is aligned. `S1-p33`, `S2-p59`,
  `S2-p54`
- Keep paired terms aligned (if the lower text says サンプル, the upper one does too). `S2-p11`
- Write names and their explanations in one pattern: 「SeamFix (首の継ぎ目の修復)」. `S2-p55`

## H. Animation

- Use animation to match the explanation, one element at a time; show two arrows one by one when the
  script explains them one by one. `S5-p56`
- Check the reveal order and that nothing is visible before its turn. `S3-p35`, `S3-p49`, `S3-p55`
- A click that suddenly adds a lot of information outruns understanding; split it. `S3-p38`
- A strong animation (e.g. swapping heads) can hide the other things the page shows (body shape, skin
  colour); restate them in text. `S3-p10`

## I. Cover, ending, and delivery

- Cover: if the English title is the main one, put it above the Japanese title; break the English title at a
  natural point (e.g. after "And", capitalised). `S2-p1`
- Affiliation: give only what the audience needs (e.g. the degree programme). Order: affiliation and year,
  then name, then supervisor (or name first); separate with a colon. `S1-p1`
- Publication list: make one's own name stand out (bold plus a different colour from the other list text);
  call papers 「国際学術誌論文」「国際会議論文」, not 「論文誌」「会議録」. `S2-p3`, `S3-p3`
- Summary: explain carefully how the body / domain knowledge was used; this is the core of the thesis.
  `S1-p73`
- Outlook: describe what the field needs in the long term, not a personal plan or something already done;
  say why and what for. `S1-p75`, `S1-p76`
- Every chapter has a place in an overview or positioning figure, and the sizes and positions of its marks
  follow a stated basis. `S2-p76`, `S3-p75`
- Remove pages that do not add anything, such as a closing 「ご清聴ありがとうございました」 page. `S1-p78`
- Slides follow the latest written summary of the thesis; revise the slides to match it before sending.
  `O`
- Speak loudly and clearly, and look at the reviewers, not at the PC or the screen. `M`
- Printed handouts: 4 or 6 slides per page, double-sided. `O`
