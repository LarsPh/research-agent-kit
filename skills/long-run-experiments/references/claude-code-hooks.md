# Optional Claude Code Hooks

The skill works without hooks. These two cover what the agent tends to forget, and stay silent otherwise.

| Hook | Event | Effect |
|---|---|---|
| `scripts/queue_check.py` | Stop | While `runs/UNATTENDED` exists: refuses to stop when a finished job is unhandled, or a GPU is idle with a ready task, or idle with no recorded reason. Allows the stop when the final message asks the user something, or the only open work waits on a `blocks: true` question. Never asks for a number of queued tasks |
| `scripts/context_inject.py` | SessionStart, matcher `compact\|resume` | Prints the run state from disk (jobs, ready tasks, open questions, latest decisions, dead-end count) under 1500 characters, labelled as background |

## Install for the experiment session only

Save as `long-run-hooks.json`, replace `SKILL_DIR` with the installed skill path, and start the session with
`claude --settings long-run-hooks.json --disallowedTools AskUserQuestion`:

```json
{
  "hooks": {
    "Stop": [
      {"hooks": [{"type": "command", "command": "python3 SKILL_DIR/scripts/queue_check.py"}]}
    ],
    "SessionStart": [
      {"matcher": "compact|resume",
       "hooks": [{"type": "command", "command": "python3 SKILL_DIR/scripts/context_inject.py"}]}
    ]
  }
}
```

The hooks read `$LONGRUN_DIR` or `./runs`, so start the session from the experiment repository.

## Why only two

Each check was weighed against how often it fires and what it costs:

| Check | Where it lives instead |
|---|---|
| brief completeness | `jobctl.py launch` refuses incomplete briefs; a hook would duplicate it |
| dialogs that wait for a click | `--disallowedTools` and permission rules, built in |
| dangerous commands, credential files | permission deny rules first; a PreToolUse hook only for rules they cannot express, such as a cumulative budget |
| conclusions without images | the report gate in the skill; a keyword hook misfires and nags |
| decisions on every message | not in v1; a UserPromptSubmit hook would fire on every message |
| waking up | cron and `wait_for_gpu.py`, not hooks |

## Side effects to avoid

- **Token cost and noise.** Hook output enters the context. Both hooks print nothing when nothing is
  wrong, and `context_inject.py` runs only after compaction or resume.
- **Loops.** The Stop hook does nothing when `stop_hook_active` is true and refuses at most twice per hour.
  Claude Code also ends a turn after eight consecutive stop-hook continuations.
- **Interrupting the user.** Both act on state only; the Stop hook is inert unless `runs/UNATTENDED`
  exists. Delete it when you are back.
- **Errors.** Both catch every exception and exit 0. A hook that crashes must not block anything.

## When a hook seems to eat or cut a message

Mechanisms documented in the Claude Code hooks reference that look like a swallowed or truncated answer:

1. **A UserPromptSubmit hook blocked the prompt.** Exit code 2 or `decision: "block"` stops the prompt from
   reaching the model. A buggy hook that crashes with exit 2 does this to every message. Never block in a
   UserPromptSubmit hook that only adds context.
2. **Output over 10,000 characters.** Claude Code saves it to a file and shows the model only the path and
   the first 2,000 characters, without asking it to read the rest. Anything spliced in after that point is
   lost. Keep injected text short.
3. **Injected text drowns the user's words.** The model acts on a long injected to-do list instead of
   the user's message. Label injected text as background and keep it short.
4. **A Stop hook overrides a pending question.** The agent asks the user and ends its turn; a Stop hook
   tells it to continue; it answers the question itself or writes a new final message. In a client that
   shows only each turn's last message, the question is folded away and the user never sees it (seen
   about 15 times in one 15-hour run). Three guards in `queue_check.py`:
   - it lets the turn end when `last_assistant_message` contains a question marker (`needs input`, `❓`,
     `待决问题`, `需要你决定`); queue work moves to the start of the next turn;
   - when it does refuse, its reason tells the agent to restate every open `blocks: true` question in the
     new final message;
   - each log line records `asks_user` when the final message asked something, so covered questions can
     be counted afterwards.
   When the user is present, ask with AskUserQuestion instead of only in prose: a dialog waits and is not
   overwritten by a continuation.

Every hook run appends a line to `runs/hooks.log` (time, hook, allow/block/inject, `asks_user` when the final
message asked something). After a night, read it to see which hook fired, how often, and with what effect.
