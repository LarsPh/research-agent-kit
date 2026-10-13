# Lane Prompts

Prepend the shared brief to each prompt. Each lane returns only its report.

## Lane A: Domain Bugs

> Find correctness bugs that a domain expert would catch. Check at least:
>
> 1. **Formula parity.** Compare every formula with the references in the brief: constants, eps values,
>    clamps, normalisations, sign conventions (for example stencil direction from `roll` or shifts versus
>    index offsets), and coordinate remaps; camera conventions (OpenGL versus OpenCV axes, pixel centres, the
>    up vector against the scene data); activations and background handling. When two implementations of the
>    same math exist (Python and C++, reference and realtime), compare them with each other. Matching a spec
>    is not enough.
> 2. **Numerics.** Reduction, prefix-sum, and accumulation dtypes; int32 index and offset overflow;
>    catastrophic cancellation; interpolation that mixes valid and invalid values, such as bilinear
>    downsampling of masked depth.
> 3. **Packing invariants.** Exclusive versus inclusive offsets, `sum(counts) == total`, empty segments, and
>    capacity overflow (dropped silently or counted).
> 4. **GPU and runtime handoffs.** Stream sync before interop (DLPack, PBO, CUDA-GL), device mismatches,
>    buffer lifetime, and resources released on exception paths as well as the happy path.
> 5. **Silent fallbacks.** Missing data replaced with zeros, identity transforms, or defaults, so the bug
>    stays hidden.
>
> For each finding give `file:line`; what goes wrong (input or state, then wrong output); severity; and a
> proof path: a failing test sketched in 3–8 lines, a comparison against a reference, an image or metric
> difference, or a benchmark. List findings without a proof path separately as unverified. Report each issue
> once. 600 words or fewer.

## Lane B: Generic Correctness

Run the platform's built-in code review on the target at the effort the user gave (default: high), and use
its output as-is. Without one, prompt:

> Scan the target line by line, audit removed behaviour, and check callers across files. Give each finding
> with `file:line` and a concrete failure scenario. 10 findings or fewer.

## Lane C: Design Taste

> Review design and maintainability only. Do not report bugs. Treat the repository docs as the statement of
> intent. Look at:
>
> - module boundaries and dependency direction (private access across modules, cycles);
> - doc–code drift (described but missing, and present but undescribed);
> - leftover or dead interfaces, options with a single legal value, options only tests use;
> - duplicated logic that must stay in sync, and what breaks if one copy changes;
> - names that no longer match behaviour;
> - test design: tests that grep source, mock away the unit under test, or lock in implementation details,
>   and whether the tests would fail if the code broke.
>
> Rank topics by their cost to a maintainer over the next year. Group findings into topics, not lines. For
> each give evidence (`file:line`, plus the doc line where relevant), why it matters, and the simplest fix.
> When the fix could go either way, such as changing the code or changing the doc, name both and leave the
> choice to the human. End with "If you do only three things". 600 words or fewer.

## Lane D: End-to-End Flow and Engineering Hygiene

> 1. **Walk the main command chain** from the brief, stage by stage. At each hand-off, check that the path,
>    filename pattern, and format one stage writes are exactly what the next stage reads, including
>    suffixes, ID zero-padding, and direction naming. Check that config defaults and CLI defaults agree, and
>    that each documented example config or manifest would pass its loader.
> 2. **Failure reporting.** Exceptions caught and logged as warnings, `return` on missing input, exit code 0
>    on failure, per-item errors swallowed so the run reports success. Say whether a failed stage is visible
>    to the user.
> 3. **Operations.** Checkpointing and resume, idempotent re-runs (in-place overwrites), logs or artifacts
>    rewritten in full every step, memory retained across an epoch.
> 4. **Security.** Unsafe deserialization (`torch.load(weights_only=False)`, `pickle`, `yaml.load`),
>    `eval`/`exec`, shell commands built from strings, paths read from untrusted files.
> 5. **Dependencies and process.** Unpinned or undeclared dependencies, a lockfile that is not enforced,
>    development tools in runtime dependencies, missing tests or CI for the riskiest logic, commit
>    granularity.
>
> For each finding give `file:line`, the failure scenario, and severity. Skip the brief's known absences.
> 500 words or fewer.
