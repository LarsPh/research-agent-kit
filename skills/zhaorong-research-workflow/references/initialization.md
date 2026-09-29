# Existing-Repository Initialization

Use this sequence for a migrated or legacy research repository. Treat platform facts as unknown until
the target environment proves them.

## 1. Bootstrap Skills Before the Project Environment

1. Install `zhaorong-research-workflow` and `research-task-implementation` at user scope.
2. Check whether Matt Pocock's engineering skills are installed.
3. If they are missing, show the user the public installation command and pause for approval or manual
   installation. Do not install external packages silently.
4. Resume in a fresh agent session so skill discovery is verified separately from file presence.

The workflow skills come first because they govern how the project environment, caches, outputs, and
validation evidence will be discovered and documented. They do not depend on the project's Python or
accelerator stack.

## 2. Audit the Migrated Repository

Inspect, without deleting or rewriting:

- Git remotes, branch, recent history, status, submodules, and ignored paths.
- Existing `AGENTS.md`, `CLAUDE.md`, documentation entry points, task plans, experiment notes, and handoffs.
- Package manifests, lockfiles, containers or image definitions, launchers, cache/output paths, and data
  roots.
- Active code/config coupling to the previous platform, including absolute paths, schedulers, queue names,
  environment managers, architecture assumptions, and committed runtime outputs.
- Historical records that merely preserve provenance rather than control current execution.

Classify each old-platform item as active coupling, reusable platform-neutral code, historical provenance,
or generated residue. Block initialization while active coupling remains unresolved. Never auto-delete it.

## 3. Establish Matt's Repository Seams

Run `setup-matt-pocock-skills` after the audit and before adding research-lifecycle docs. Let it inspect the
actual remote and existing instructions, then confirm its tracker, triage labels, and single- or
multi-context domain layout with the user.

Keep responsibilities separate:

- Tracker documents define coordination operations.
- Domain documents define stable language and durable decisions.
- Research authority documents define direction, experiment state, implementation checklists, reviews,
  milestones, and deferred work.

Do not create empty `CONTEXT.md`, ADR, review, milestone, failure, or deferred files for appearance.

## 4. Build the Minimum Research Spine

Adapt existing documentation instead of imposing a second hierarchy. When no equivalent exists, draft:

- `docs/README.md`: authoritative navigation and current status.
- `docs/agents/research-workflow.md`: repository-specific lifecycle, evidence, review, and acceptance rules.
- `docs/research/active_direction.md`: current questions, established facts, open hypotheses, rejected
  assumptions, and the rolling frontier.
- A concise hard-rules block in the existing `AGENTS.md` or `CLAUDE.md`. If neither exists, ask which one
  to create, following Matt's setup rule. When both Codex and Claude Code work in the repository, use a
  shared `AGENTS.md` plus a thin `CLAUDE.md` bridge
  ([templates](https://github.com/LarsPh/research-agent-kit/tree/main/templates)). Ask the user for every
  value the templates leave as a placeholder (time thresholds, stores, language).

Show the complete draft and its relationship to existing docs before editing. Finish only after links and
authority ownership are unambiguous.

## 5. Stop Before Environment Construction

Report repository initialization as complete, then stop for user review. Mark the project environment and
compute runtime `not yet characterized`; do not fill those sections with remembered platform behavior.

The next sprint must:

1. Read company or site policies and inspect available image, job, storage, data, network, and secret
   interfaces.
2. Draft a private repository runtime-and-artifact contract, including environment manager, lock strategy,
   persistent mounts, cache identity/lifetime, output publishing, resource limits, resume, and failure
   evidence.
3. Respect a user-specified full-environment strategy such as full `uv`; never substitute a partial pip
   environment for convenience.
4. Obtain user confirmation before creating the environment or submitting compute.
5. Validate imports and entry points, then use the platform's smallest truthful accelerator job and a
   fresh-instance persistence check before research experiments.

Keep every site-specific name, command, image, mount, dataset path, and internal policy in the private
target repository. The public workflow skill contains only the discovery procedure.
