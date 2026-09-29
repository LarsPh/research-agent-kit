# Instruction Templates

Starting points for a research repository that Codex and Claude Code both work in. Copy them into the
target repository; fill facts from what the repository contains and ask the user for every threshold or
value left as a placeholder.

- [AGENTS.md.template](AGENTS.md.template) — the shared file: project facts, authority order, evidence
  standards, and the checkpoints where Codex must stop and ask.
- [CLAUDE.md.template](CLAUDE.md.template) — a thin bridge that imports `AGENTS.md` and adds only
  Claude-specific behavior.

## Why the Two Patches Point in Opposite Directions

The default system prompts pull the two agents apart. Codex CLI is told to keep going until the task is
completely resolved and to assume the user wants code changes; Claude Code is told to make only changes
that are requested or clearly necessary and to ask when it needs to validate an assumption
([nilenso, "Codex CLI vs Claude Code on autonomy", 2026-02-12](https://blog.nilenso.com/blog/2026/02/12/codex-cli-vs-claude-code-on-autonomy/)).

In research work this shows up as two different failure modes:

- Codex runs past decisions the user should make, then reports once at the end. Its patch lives in
  `AGENTS.md`: name the checkpoints where it must stop and ask.
- Claude reports and asks too often, and chat fills with intermediate prose. Its patch lives in
  `CLAUDE.md`: report deltas against a ledger, decide engineering details itself, and ask only research
  decisions.

## Loading Rules

- Claude Code reads `CLAUDE.md`. When a `CLAUDE.md` exists, it does not read `AGENTS.md` by default, so the
  bridge imports it with `@AGENTS.md`. Check the current Claude Code memory documentation if this changes.
- Codex concatenates `AGENTS.md` files from the repository root down to the working directory, up to a
  configurable byte limit (`project_doc_max_bytes`). Keep the shared file short enough to fit with room to
  spare.
- Put multi-step procedures in skills, not in either file. Both files load on every turn.
