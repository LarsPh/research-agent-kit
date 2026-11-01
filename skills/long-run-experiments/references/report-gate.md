# Report Gate

Run this before any result changes a ranking, a decision, a table, or a claim. If any item fails, report
the result as "preliminary" with what is missing.

```
Report gate:
- [ ] Opened the supervision images and the outputs; paths written in the report
- [ ] Ruled out the usual confounders: sky or background counted as holes, black-region thresholds,
      different frame formats or resolutions, different cameras or normalisation
- [ ] Gain size compared with known variation; if variation is unknown, label the result "single run,
      preliminary" instead of rerunning by default
- [ ] Before a result changes a default or a claim, reproduced on a different scene or view (cross-scene
      check), not only on another seed of the same scene
- [ ] Extra seeds only when the project's budget rules allow them and the user asked for them
- [ ] Number of scenes stated; one scene is labelled "single-scene observation"
- [ ] A wrong-looking image went through graphics-debug before any method was blamed
- [ ] Compared against the same baseline run, not a number remembered from chat
```

Repeat-run policy follows the project's rules (AGENTS.md, the user's preferences); this gate only asks that
a single, unreproduced result is labelled as such. A second seed on the same scene can confirm a result that
does not transfer: a large gain on one scene may vanish on four others.

A retracted conclusion costs more than a late one: the user may already have acted on it.
