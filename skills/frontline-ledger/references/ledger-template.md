# Ledger Template

Copy this skeleton. Keep headings stable so agents and humans can grep them.

```md
# <Research line> ledger

Last updated: <YYYY-MM-DD HH:MM TZ> · Branch: <branch> · Authority: <link to direction/plan doc>

## Decisions

| ID | Date | Decision | Why / evidence | Source (question ID, user message, report) |
|---|---|---|---|---|

## Open questions

### Q<n>: <one-line question>
- Deciding: <what this choice controls and why it matters>
- Options: <how the options actually differ>
- Recommendation: <option + reason>
- Default if unanswered: <what the agent will do>

### Closed
- Q<n> → D<m> (<date>)

## Waiting on the user

| # | Task | Status (ready / preparing / waiting on you / done) | What to send or run | Tool or skill | Where the result goes |
|---|---|---|---|---|---|

## Artifacts

| Date | What | Path | Inspected by agent? | Note |
|---|---|---|---|---|
```

## Section Rules

- **Decisions** only grows. Supersede an entry by adding a new one that cites the old ID.
- **Open questions** each carry a recommendation and a default. A question without a recommendation is not
  ready to ask.
- **Waiting on the user** rows name exact files, the exact destination for results, and the order to do
  them in when order matters. Move finished rows to a short "done" list with the date.
- **Artifacts** record whether an agent actually opened each visual. Generated but unopened visuals are
  marked `no`.
