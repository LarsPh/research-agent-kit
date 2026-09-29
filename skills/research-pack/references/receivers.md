# Receivers

Upload limits change often; confirm against the receiver's current help pages before relying on a number.
The figures below were gathered from vendor help pages and third-party summaries in 2026 and are only a
starting point.

| Receiver | What matters | Implication for the pack |
|---|---|---|
| Chat conversation with attachments | Per-message file count and per-image size caps; code execution may unpack a zip, plain reading may not | Attach `digest.md` plus a handful of key images directly; attach the zip only when the model can run code |
| Project knowledge (ChatGPT / Claude Projects) | File-count cap per project by plan; archives may be stored without their contents being indexed | Upload `digest.md` and selected docs as separate files; treat the zip as an archive, not as knowledge |
| Cloud agent workspace (a remote "work" or code environment) | Can usually unpack and run code | The zip is the primary artifact; `digest.md` is the entry point inside it |
| Gemini-style apps | Per-prompt file-count cap even after unpacking | Keep the pack small; lead with the digest |

## Budget Heuristics

- Text: estimate tokens as characters / 4 for English and characters / 1.5 for CJK. Stay well under the
  receiver's window to leave room for the answer.
- Images: prefer a few representative, captioned images over many similar ones; downscale very large
  renders before packing.
- Cut order when over budget: oldest diffs → largest text reports → duplicate images. Keep the digest and
  the representative visuals.
