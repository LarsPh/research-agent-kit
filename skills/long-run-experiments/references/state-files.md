# Run Directory

Everything the scripts read lives in one directory: `$LONGRUN_DIR`, else `runs/` in the current working
directory. Keep it out of Git or ignore `runs/status/` and `runs/logs/`; commit the ledger, not the run
state.

| Path | Written by | Contents |
|---|---|---|
| `queue.json` | agent | tasks waiting to run |
| `questions.json` | agent | questions for the user |
| `decisions.md` | agent | the user's decisions, append-only |
| `dead_ends.md` | agent | abandoned approaches, append-only |
| `brief_fields.txt` | user or agent | extra required brief keys for this project, one per line |
| `briefs/<id>.md` | agent | one brief per job ([dispatch.md](dispatch.md)) |
| `status/<id>.json`, `.done`, `.sh` | `jobctl.py` | job metadata, done marker, wrapper |
| `logs/<id>.log` | the job | stdout and stderr |
| `UNATTENDED` | user or agent | present while nobody is watching; enables the Stop hook and cron |
| `idle_ok.json` | agent | why idling is right, and until when |
| `resume.json`, `hooks.log` | scripts | last cron wake-up; one line per hook or wake-up |

State that scripts parse is JSON, because models rewrite Markdown more freely than JSON. The two Markdown
logs are append-only: add lines, never edit old ones.

## queue.json

```json
[
  {"id": "L3-d50", "line": "L3", "why": "main table row 2, night scene d50", "status": "ready",
   "brief": "runs/briefs/L3-d50.md"}
]
```

`status` is `ready`, `blocked` or `launched` (`jobctl.py launch` sets it). A task without `line` and `why`
is not counted as ready anywhere.

## questions.json

```json
[
  {"id": "q7", "line": "L5", "question": "Add method X to the user-study comparison?",
   "blocks": false, "default": "keep the current three methods", "status": "open"}
]
```

When the user answers, set `status` to `answered`, add `answer`, and append the decision to `decisions.md`.

## decisions.md

One line per decision, tagged by topic, dated, in the user's own words:

```markdown
- [user-study] 2026-10-27 13:42 PI: recruit only lab members we know
- [user-study] 2026-10-31 09:10 PI: supersedes 10-27: also allow two outside volunteers
```

Mark a replaced decision by writing the new one with "supersedes"; never delete the old line.

## dead_ends.md

```markdown
- [L6] 2026-10-30 depth-prior weight 0.5→2.0: PSNR −0.4, floaters worse on 3/3 scenes; dropped
```

## idle_ok.json

```json
{"reason": "all L3 runs wait for the user's choice in q9; L5 needs GPU >40 GB", "until": "2026-11-02T06:00:00+09:00"}
```
