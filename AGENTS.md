# Research Agent Kit Maintainer Rules

This public repository distributes platform-neutral agent skills. It is not a machine, lab, cluster, or
company configuration template.

## Skill Quality

- Keep every skill's `SKILL.md` concise and imperative. Move branch-specific detail into directly linked
  `references/` files.
- Keep only `name` and `description` in skill frontmatter. Write the description in the third person
  ("Reviews …", "Keeps …"), saying what the skill does and when to use it. Keep `agents/openai.yaml`
  aligned and include the explicit `$skill-name` token in every default prompt.
- State checkable completion criteria and protect research claim boundaries. Do not turn smoke or prototype
  evidence into production or academic completion.
- Keep platform discovery procedural. Never add private hostnames, paths, images, queues, mount points,
  credentials, dataset locations, or company commands.

## Changes and Validation

- Update `README.md` when installation commands, bundled skills, or initialization order changes.
- Use the official skill initializer for new skills and the official validator for every changed skill.
- Test skill discovery/installation in a temporary repository and forward-test complex workflow skills on
  realistic read-only tasks.
- Run `python scripts/check_repo.py` (frontmatter, openai.yaml, links, README coverage, private
  information, trailing whitespace, Python syntax) and `python -m pytest tests`; CI runs both on every pull
  request. Check the final staged file list before committing.
- Keep eval scenarios under `evals/<skill>/`, not inside the skill folder, and run them by hand before a
  large change to that skill; CI does not run model-based evals.
- Preserve unrelated skills unless the task explicitly expands their scope.
