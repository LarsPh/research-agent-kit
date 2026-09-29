# Digest Template

`digest.md` is the entry point of the pack. Write it for a strong model that knows the field but not this
repository. Follow the user's or repository's language.

```md
# <Project> research pack — <YYYY-MM-DD>

## Read This First
- Window: <start> → <end>
- Goal of this pack: <what the user wants back, one sentence>
- Contents: `manifest.json` (every file with source worktree/branch/commit/path), `lines/<name>/`
  (log + diff stat per line), `docs/`, `images/`.

## Project Context
<5–10 lines: the research goal, the current direction, and terms the reader needs. Define project terms
on first use.>

## Lines
### <line name> — branch `<branch>`, commits `<first>..<last>`
- What changed: <2–4 bullets>
- Evidence: <docs/… and images/… filenames, each with one line on what it shows>
- Status: <completed / not done / deferred / blocked items>
- Claim boundary: <what the evidence does and does not support; smoke vs real result>

## Key Diff Stats
<only the files that matter, with one line each on why>

## Questions for You
1. <question> — Evidence: <files>. Our current lean: <recommendation, or "none">.

## How to Answer
- Reply as one Markdown document titled `<YYYY-MM-DD>-<topic>`.
- For each question: answer, reasoning, and what experiment or change you propose.
- Mark anything you are unsure of; do not invent repository facts beyond this pack.
```

## Image Naming

Images are named `<branch>__<shortsha>__<original-name>` so the reader can cite them unambiguously. Describe
each one in the digest; a caption-less image invites misreading.
