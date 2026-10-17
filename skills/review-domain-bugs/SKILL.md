---
name: review-domain-bugs
description: Read-only review of research, numerical, or GPU code for bugs a domain expert would catch, each with a proof path. Checks formula parity against reference implementations, numerics, packing invariants, GPU and runtime handoffs, and silent fallbacks. Use alone to check a kernel or module against training code or a paper, or as lane A of multilane-review.
---

# Review Domain Bugs

Find correctness bugs that need domain knowledge: the ones a generic line-by-line review misses because it
does not know which implementation is the reference or which convention the data uses.

## Protect the Target

Review read-only. Never edit, commit to, or push the target repository. Take the target (ref range, branch,
directory, or files) from the user; ask when none is named.

## 1. Get the Context

If a brief from multilane-review is provided, use it and do not reread the docs. Otherwise read the README,
the docs that state formulas and conventions, and the target file list, then note in 30 lines or fewer: the
references (training code, CPU or float64 path, upstream repo, paper formulas) with paths, and the stated
conventions (coordinate systems, units, dtype rules), each with its doc file and line.

## 2. Check

1. **Formula parity.** Compare every formula with the references: constants, eps values, clamps,
   normalisations, sign conventions (for example stencil direction from `roll` or shifts versus index
   offsets), and coordinate remaps; camera conventions (OpenGL versus OpenCV axes, pixel centres, the up
   vector against the scene data); activations and background handling. When two implementations of the same
   math exist (Python and C++, reference and realtime), compare them with each other. Matching the docs is
   not enough: docs rarely state signs and offsets.
2. **Numerics.** Reduction, prefix-sum, and accumulation dtypes; int32 index and offset overflow;
   catastrophic cancellation; interpolation that mixes valid and invalid values, such as bilinear
   downsampling of masked depth.
3. **Packing invariants.** Exclusive versus inclusive offsets, `sum(counts) == total`, empty segments, and
   capacity overflow (dropped silently or counted).
4. **GPU and runtime handoffs.** Stream sync before interop (DLPack, PBO, CUDA-GL), device mismatches,
   buffer lifetime, and resources released on exception paths as well as the happy path.
5. **Silent fallbacks.** Missing data replaced with zeros, identity transforms, or defaults, so the bug
   stays hidden.

## 3. Report

One table, most severe first, then a separate "unverified" list for findings without a proof path. Report
each issue once. 600 words or fewer.

| # | file:line | finding (input or state, then wrong output) | kind | severity | proof path |
|---|---|---|---|---|---|

- `kind` is `bug` for every row in this lane.
- `severity` is high, medium, or low.
- A proof path is a failing test sketched in 3–8 lines, a comparison against a reference, an image or metric
  difference, or a benchmark.

When run alone, end with: "Static review; not verified by a second pass."

Done when every row has a location, a failure scenario, and either a proof path or a place in the
unverified list.
