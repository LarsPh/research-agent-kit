---
name: frontline-ledger
description: Keep one rolling ledger per research line so chat carries only deltas. Use when a research line accumulates state across turns; when the user says things are getting lost in chat; or when the user returns and asks where a line stands.
---

# Frontline Ledger

The ledger is the durable front line of one research line: every decision, open question, pending user
action, and artifact lives there. Chat is a pointer into it. A reader who skips the chat and reads only the
ledger must lose nothing.

## Locate or Create the Ledger

1. Use the repository's existing ledger path for this line when one exists. Otherwise create
   `docs/research/<line>/ledger.md` beside the line's other authority documents.
2. Keep one ledger per research line. Split a section into its own file only after it outgrows a
   comfortable read, and link the split file from the ledger.
3. Use the four sections in [ledger-template.md](references/ledger-template.md), in that order.

## Update on Every Event

Update the ledger the moment any of these happens, before reporting it in chat:

- a result lands (experiment, probe, review, rendered visual) → add its path to **Artifacts** and any
  decision it settles to **Decisions**;
- a question needs the user → add it to **Open questions** with your recommendation;
- the user decides → move the question into **Decisions**, leave a one-line closed entry behind;
- something needs the user's hands (upload a package, run a command, grant access) → add it to
  **Waiting on the user** with what, how, where the result goes, and status;
- a package or deliverable becomes ready → update its row in **Waiting on the user**.

Commit the ledger with the work it describes when the repository tracks it in Git.

The update is complete when every section reflects the current state: no settled question still open, no
delivered task still pending, no new artifact missing its path.

## Report the Delta

Write each chat report as:

1. one sentence: what changed;
2. what the user must do now, if anything;
3. a pointer: which ledger sections or rows changed.

Give each open question its own paragraph, marked so it stands out (use the repository's marker when it
names one), with a recommendation. When the user does not answer, proceed on the recommendation and record
that in **Decisions**.

Leave detail in the ledger. When the user asks for a summary, answer from the ledger, not from the chat.
Follow the user's or repository's language.

## Ledger Versus Handoff

The ledger is continuous and owned by the line. A handoff is a snapshot for the next agent at session end;
it points to the ledger instead of copying it. Use `handoff` for the snapshot.

## Artifact Paths

Write artifact paths the user can open from where they read. Use repository-relative paths for files
inside the worktree. For files under a storage root outside it, link the root into an ignored directory of
the worktree and give the path through that link, or give absolute paths. Inside Orca, follow
`orca-remote-bridge` for paths.
