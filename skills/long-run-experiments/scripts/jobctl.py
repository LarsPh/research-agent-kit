#!/usr/bin/env python3
"""Launch experiment jobs detached from the agent session, and tell their state from files, not guesses.

launch  start a command in tmux (or a new session when tmux is missing) so it survives the agent's
        session or sub-agent ending; record pid, token and log in <run dir>/status/<id>.json; when the
        command exits, a wrapper writes "<token> <exit code>" to <id>.done.
status  one line per job: running / stalled / done / failed / crashed.
watch   only what needs the agent: finished jobs not yet handled, crashes, stalls, idle GPUs with ready
        tasks. Exit 1 when anything is listed, 0 when nothing needs attention.
handled mark a finished job as handled after its result is recorded.

Run dir: $LONGRUN_DIR, else ./runs. A job is done only when its .done file carries its own token, so old
logs, copied logs or another job's marker never count, and no pgrep is needed.
"""

import argparse
import os
import secrets
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lrx_common as lc  # noqa: E402
from check_brief import brief_problems  # noqa: E402

FINISHED = {"done", "failed", "crashed"}


def status_dir(root):
    return root / "status"


def job_files(root, job_id):
    d = status_dir(root)
    return d / f"{job_id}.json", d / f"{job_id}.done", d / f"{job_id}.sh"


def write_wrapper(path, cwd, cmd, log, done, token, gpu):
    lines = ["#!/usr/bin/env bash", f"cd {shlex.quote(str(cwd))} || exit 97"]
    if gpu is not None:
        lines.append(f"export CUDA_VISIBLE_DEVICES={shlex.quote(gpu)}")
    lines += [
        f"( {shlex.join(cmd)} ) >> {shlex.quote(str(log))} 2>&1",
        "rc=$?",
        f"printf '%s %s\\n' {token} \"$rc\" > {shlex.quote(str(done))}.tmp"
        f" && mv {shlex.quote(str(done))}.tmp {shlex.quote(str(done))}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o755)


def start(method, name, wrapper):
    if method == "tmux":
        subprocess.run(["tmux", "new-session", "-d", "-s", name, "bash", str(wrapper)], check=True)
        pid = subprocess.run(["tmux", "display-message", "-p", "-t", name, "#{pane_pid}"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return int(pid)
    proc = subprocess.Popen(["bash", str(wrapper)], start_new_session=True, stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc.pid


def launch(args):
    root = lc.run_dir()
    job_id = args.id
    meta_path, done_path, wrapper = job_files(root, job_id)
    old = lc.load_json(meta_path, None)
    if old and classify(root, old)["state"] in {"running", "stalled"} and not args.force:
        raise SystemExit(f"job {job_id} is still running; pick another id or pass --force")
    brief = Path(args.brief)
    found = brief_problems(brief)
    if found:
        raise SystemExit(f"brief {brief} is incomplete: " + "; ".join(found))
    cmd = args.cmd[1:] if args.cmd and args.cmd[0] == "--" else args.cmd
    if not cmd:
        raise SystemExit("give the command after --")
    method = args.detach
    if method == "auto":
        method = "tmux" if shutil.which("tmux") else "session"
    status_dir(root).mkdir(parents=True, exist_ok=True)
    log = Path(args.log or root / "logs" / f"{job_id}.log").resolve()
    log.parent.mkdir(parents=True, exist_ok=True)
    done_path.unlink(missing_ok=True)
    token = secrets.token_hex(8)
    write_wrapper(wrapper, Path(args.cwd).resolve(), cmd, log, done_path, token, args.gpu)
    session = f"lr-{job_id}" if method == "tmux" else None
    pid = start(method, session, wrapper)
    meta = {
        "id": job_id, "token": token, "pid": pid, "method": method, "session": session,
        "started": lc.iso(), "log": str(log), "cmd": cmd, "cwd": str(Path(args.cwd).resolve()),
        "brief": str(brief.resolve()), "gpu": args.gpu, "handled": False,
    }
    lc.save_json(meta_path, meta)
    tasks = lc.queue(root)
    for task in tasks:
        if task.get("id") == job_id:
            task["status"] = "launched"
    if tasks:
        lc.save_json(root / "queue.json", tasks)
    where = f"tmux {session}" if session else "own session"
    print(f"launched {job_id} ({where}, pid {pid}) log={log}")


def pid_alive(pid, wrapper):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    cmdline = Path(f"/proc/{pid}/cmdline")
    if cmdline.exists():  # guard against pid reuse: the process must still be our wrapper
        return str(wrapper) in cmdline.read_bytes().replace(b"\0", b" ").decode(errors="replace")
    return True


def last_line(log):
    try:
        lines = Path(log).read_text(encoding="utf-8", errors="replace").strip().splitlines()
        return lines[-1][:200] if lines else ""
    except OSError:
        return ""


def classify(root, meta, stall_min=30):
    _, done_path, wrapper = job_files(root, meta["id"])
    if done_path.exists():
        parts = done_path.read_text(encoding="utf-8").split()
        if len(parts) == 2 and parts[0] == meta["token"]:
            rc = int(parts[1])
            return {"state": "done" if rc == 0 else "failed", "rc": rc}
    if pid_alive(meta["pid"], wrapper):
        log = Path(meta["log"])
        age = (lc.now().timestamp() - log.stat().st_mtime) / 60 if log.exists() else 0
        if age > stall_min:
            return {"state": "stalled", "quiet_min": int(age)}
        return {"state": "running"}
    return {"state": "crashed", "last": last_line(meta["log"])}


def jobs(root):
    d = status_dir(root)
    return [lc.load_json(p, None) for p in sorted(d.glob("*.json"))] if d.exists() else []


def describe(meta, info):
    extra = ""
    if "rc" in info:
        extra = f" exit {info['rc']}"
    elif info["state"] == "stalled":
        extra = f" log quiet {info['quiet_min']} min"
    elif info["state"] == "crashed":
        extra = f" (no .done, process gone; last log line: {info['last']!r})"
    handled = " [handled]" if meta.get("handled") and info["state"] in FINISHED else ""
    return f"{meta['id']}: {info['state']}{extra}{handled}"


def status(args):
    root = lc.run_dir()
    for meta in jobs(root):
        if meta:
            print(describe(meta, classify(root, meta, args.stall_min)))


def watch(args):
    root = lc.run_dir()
    items = []
    for meta in jobs(root):
        if not meta:
            continue
        info = classify(root, meta, args.stall_min)
        if info["state"] == "stalled" or (info["state"] in FINISHED and not meta.get("handled")):
            items.append(describe(meta, info))
    idle = lc.idle_gpus()
    ready = lc.ready_tasks(root)
    if idle and ready:
        items.append(f"idle GPUs {idle} and {len(ready)} ready task(s): {', '.join(t['id'] for t in ready[:5])}")
    print("\n".join(items) if items else "nothing needs attention")
    return 1 if items else 0


def handled(args):
    root = lc.run_dir()
    meta_path, _, _ = job_files(root, args.id)
    meta = lc.load_json(meta_path, None)
    if not meta:
        raise SystemExit(f"no job {args.id}")
    meta["handled"] = True
    lc.save_json(meta_path, meta)
    print(f"{args.id}: handled")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("launch", help="start a job detached from this session")
    p.add_argument("--id", required=True)
    p.add_argument("--brief", required=True, help="task brief; see references/dispatch.md")
    p.add_argument("--cwd", default=".")
    p.add_argument("--log")
    p.add_argument("--gpu", help="value for CUDA_VISIBLE_DEVICES")
    p.add_argument("--detach", choices=["auto", "tmux", "session"], default="auto")
    p.add_argument("--force", action="store_true")
    p.add_argument("cmd", nargs=argparse.REMAINDER)
    p.set_defaults(func=launch)
    for name, func in (("status", status), ("watch", watch)):
        s = sub.add_parser(name)
        s.add_argument("--stall-min", type=int, default=30, help="log silence that counts as stalled")
        s.set_defaults(func=func)
    h = sub.add_parser("handled")
    h.add_argument("id")
    h.set_defaults(func=handled)
    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
