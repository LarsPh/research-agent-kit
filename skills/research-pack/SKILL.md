---
name: research-pack
description: Pack a period of multi-branch research output (reports, code diffs, visuals) into one package for an external research LLM, and ingest the guidance it sends back. Use when the user wants to send recent results to an external planning model; when several worktrees or branches must be summarized together; or when external guidance arrives for the agent to act on. Triggers include 打包, 发给 GPT, 回传包.
---

# Research Pack

A pack is a self-explaining snapshot: an external model that has never seen the repository must be able to
discuss the work from the pack alone, and its answer must come back to a known place.

## Build the Pack

1. **Scope.** Fix the time window, the worktrees or branches in scope, and the questions the user wants the
   external model to answer. Read each line's ledger (`frontline-ledger`) and direction document first.
2. **Collect.** Run `python3 scripts/pack.py collect --out <pack-dir> --since <date>` with one
   `--worktree <path>[=<name>]` per line and one `--include <file>` per report or image to carry. It writes
   per-line commit logs, diff stats and status under `lines/`, copies included files into `docs/` and
   `images/`, writes `manifest.json`, and prints the size estimate. See `--help` for flags.
3. **Inspect visuals.** Open every image before it enters the pack. Keep the representative ones; drop
   near-duplicates.
4. **Write the digest.** Write `digest.md` at the pack root from
   [digest-template.md](references/digest-template.md). The digest is complete when every included file is
   referenced from it and every question has the evidence it needs named beside it.
5. **Budget.** Check the pack against the receiver's limits in
   [receivers.md](references/receivers.md). When it is over, cut the oldest diffs and the largest text
   first; keep representative images.
6. **Finish.** Run `python3 scripts/pack.py zip --out <pack-dir>` to produce the archive. Deliver the
   zip and a separate copy of `digest.md`, because some receivers do not open archives. Record the pack in
   the ledger's **Waiting on the user** section with where the answer should go. When a desktop agent
   pulls packs from a remote host, also publish it through the outbox in `orca-remote-bridge`.

## Ingest the Answer

1. Save the external model's guidance under the repository's inbox directory (default
   `docs/research/inbox/<YYYY-MM-DD>-<topic>.md`) with the pack name it answers.
2. Treat it as a proposal: separate recommendations from decisions, and ask the user before promoting a
   recommendation to a project decision.
3. Update the ledger: new open questions, accepted decisions, and the closed pack row.

## Optional Tools

`repomix` can replace the log/diff step for a single branch (`--include-diffs`, `--include-logs`,
`--token-count-encoding`). It does not merge branches or embed images, so keep this skill's manifest and
digest around it.
