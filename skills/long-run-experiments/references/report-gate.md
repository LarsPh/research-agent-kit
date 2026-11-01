# Report Gate

Run this before any result changes a ranking, a decision, a table, or a claim. If any item fails, report
the result as "preliminary" with what is missing.

```
Report gate:
- [ ] Opened the supervision images and the outputs; paths written in the report
- [ ] Ruled out the usual confounders: sky or background counted as holes, black-region thresholds,
      different frame formats or resolutions, different cameras or normalisation
- [ ] Gain larger than the run-to-run noise, or confirmed on a second seed
- [ ] Number of scenes stated; one scene is labelled "single-scene observation"
- [ ] A wrong-looking image went through graphics-debug before any method was blamed
- [ ] Compared against the same baseline run, not a number remembered from chat
```

A retracted conclusion costs more than a late one: the user may already have acted on it.
