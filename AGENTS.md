# Research Agent Kit Maintainer Rules

This public repository distributes platform-neutral agent skills. It is not a machine, lab, cluster, or
company configuration template.

## Skill Quality

- Keep every skill's `SKILL.md` concise and imperative. Move branch-specific detail into directly linked
  `references/` files.
- Keep only `name` and `description` in skill frontmatter. Keep `agents/openai.yaml` aligned and include the
  explicit `$skill-name` token in every default prompt.
- State checkable completion criteria and protect research claim boundaries. Do not turn smoke or prototype
  evidence into production or academic completion.
- Keep platform discovery procedural. Never add private hostnames, paths, images, queues, mount points,
  credentials, dataset locations, or company commands.

## Changes and Validation

- Update `README.md` when installation commands, bundled skills, or initialization order changes.
- Use the official skill initializer for new skills and the official validator for every changed skill.
- Test skill discovery/installation in a temporary repository and forward-test complex workflow skills on
  realistic read-only tasks.
- Check Markdown links, YAML parsing, `git diff --check`, and the final staged file list before committing.
- Preserve unrelated skills unless the task explicitly expands their scope.
