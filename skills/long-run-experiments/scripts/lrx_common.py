"""Shared helpers for the long-run-experiments scripts: state paths, JSON files, GPUs, hook log.

State lives under the run directory: $LONGRUN_DIR, else ./runs. Every script reads facts from there,
never from the agent's memory.
"""

import datetime as dt
import json
import os
import subprocess
from pathlib import Path


def run_dir():
    return Path(os.environ.get("LONGRUN_DIR") or "runs").resolve()


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t=None):
    return (t or now()).isoformat(timespec="seconds")


def parse_iso(text):
    return dt.datetime.fromisoformat(text) if text else None


def load_json(path, default):
    path = Path(path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def queue(root=None):
    return load_json((root or run_dir()) / "queue.json", [])


def questions(root=None):
    return load_json((root or run_dir()) / "questions.json", [])


def ready_tasks(root=None):
    """Queued tasks that name their line and reason and are not blocked."""
    return [t for t in queue(root) if t.get("status", "ready") == "ready" and t.get("line") and t.get("why")]


def open_questions(root=None):
    return [q for q in questions(root) if q.get("status", "open") == "open"]


def gpus():
    """List of {index, mem_used_mb, util} from nvidia-smi; [] when unavailable.

    LONGRUN_FAKE_GPUS="0:0:0,1:20000:95" (index:mem_mb:util) overrides it, for tests and dry runs.
    """
    fake = os.environ.get("LONGRUN_FAKE_GPUS")
    if fake is not None:
        rows = [r.split(":") for r in fake.split(",") if r]
        return [{"index": int(i), "mem_used_mb": int(m), "util": int(u)} for i, m, u in rows]
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,memory.used,utilization.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=20, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    result = []
    for line in out.strip().splitlines():
        i, m, u = (int(x.strip()) for x in line.split(","))
        result.append({"index": i, "mem_used_mb": m, "util": u})
    return result


def idle_gpus(max_mem_mb=1000, max_util=5):
    return [g["index"] for g in gpus() if g["mem_used_mb"] <= max_mem_mb and g["util"] <= max_util]


def log_hook(name, action, detail="", root=None):
    """One line per hook run, so a night's hook noise can be audited afterwards."""
    try:
        path = (root or run_dir()) / "hooks.log"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{iso()}\t{name}\t{action}\t{detail}\n")
    except OSError:
        pass
