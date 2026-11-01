"""Tests for skills/long-run-experiments/scripts."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "skills/long-run-experiments/scripts"

BRIEF = """# Brief
line: L3
why: fill main table row 2, night d50
goal: train d50 for 2k steps
outputs: runs/out/L3-d50/
done_when: eval.json exists with psnr
budget: GPU 1x 3h, API $0
time_limit: 3h
"""


def run(script, *args, env=None, stdin=None, check=False):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True,
                          env=env, input=stdin, check=check)


@pytest.fixture
def env(tmp_path):
    e = dict(os.environ, LONGRUN_DIR=str(tmp_path / "runs"), LONGRUN_FAKE_GPUS="0:20000:90")
    (tmp_path / "runs").mkdir()
    (tmp_path / "brief.md").write_text(BRIEF, encoding="utf-8")
    return e


def wait_state(env, job, state, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        out = run("jobctl.py", "status", env=env).stdout
        if f"{job}: {state}" in out:
            return out
        time.sleep(0.1)
    raise AssertionError(out)


def test_brief_check(tmp_path, env):
    assert run("check_brief.py", str(tmp_path / "brief.md"), env=env).returncode == 0
    bad = tmp_path / "bad.md"
    bad.write_text(BRIEF.replace("budget: GPU 1x 3h, API $0", "budget: 1.5x last run").replace("why:", "x:"))
    out = run("check_brief.py", str(bad), env=env)
    assert out.returncode == 1 and "missing why" in out.stdout and "no number" not in out.stdout
    bad.write_text(BRIEF.replace("budget: GPU 1x 3h, API $0", "budget: same as before"))
    assert "budget has no number" in run("check_brief.py", str(bad), env=env).stdout
    (tmp_path / "runs" / "brief_fields.txt").write_text("eval_frame_format\n")
    assert "missing eval_frame_format" in run("check_brief.py", str(tmp_path / "brief.md"), env=env).stdout


def test_launch_refuses_incomplete_brief(tmp_path, env):
    bad = tmp_path / "bad.md"
    bad.write_text("line: L3\n")
    out = run("jobctl.py", "launch", "--id", "j", "--brief", str(bad), "--detach", "session", "--", "true", env=env)
    assert out.returncode != 0 and "incomplete" in out.stderr


@pytest.mark.parametrize("cmd,state", [("true", "done exit 0"), ("false", "failed exit 1")])
def test_done_marker_carries_token_and_exit_code(tmp_path, env, cmd, state):
    out = run("jobctl.py", "launch", "--id", "j", "--brief", str(tmp_path / "brief.md"), "--detach", "session",
              "--cwd", str(tmp_path), "--", "bash", "-c", f"echo hi; {cmd}", env=env, check=True)
    assert "launched j" in out.stdout
    wait_state(env, "j", state)
    assert "hi" in (tmp_path / "runs/logs/j.log").read_text()


def test_stale_done_marker_from_old_run_is_ignored(tmp_path, env):
    run("jobctl.py", "launch", "--id", "j", "--brief", str(tmp_path / "brief.md"), "--detach", "session",
        "--", "sleep", "5", env=env, check=True)
    (tmp_path / "runs/status/j.done").write_text("0000000000000000 0\n")  # e.g. copied from an old run
    assert "j: running" in run("jobctl.py", "status", env=env).stdout


def test_crash_without_done_marker(tmp_path, env):
    run("jobctl.py", "launch", "--id", "j", "--brief", str(tmp_path / "brief.md"), "--detach", "session",
        "--", "bash", "-c", "echo 'CUDA out of memory'; sleep 30", env=env, check=True)
    meta = json.loads((tmp_path / "runs/status/j.json").read_text())
    time.sleep(0.3)
    os.killpg(meta["pid"], 9)  # killed from outside: the wrapper never writes .done
    out = wait_state(env, "j", "crashed")
    assert "CUDA out of memory" in out


def test_job_survives_parent_session_ending(tmp_path, env):
    """The launcher exits immediately (like a sub-agent ending); the job keeps running in its own session."""
    run("jobctl.py", "launch", "--id", "j", "--brief", str(tmp_path / "brief.md"), "--detach", "session",
        "--", "bash", "-c", "sleep 1; echo finished", env=env, check=True)
    wait_state(env, "j", "done exit 0")
    assert "finished" in (tmp_path / "runs/logs/j.log").read_text()


def test_watch_and_handled(tmp_path, env):
    run("jobctl.py", "launch", "--id", "j", "--brief", str(tmp_path / "brief.md"), "--detach", "session",
        "--", "true", env=env, check=True)
    wait_state(env, "j", "done")
    out = run("jobctl.py", "watch", env=env)
    assert out.returncode == 1 and "j: done" in out.stdout
    run("jobctl.py", "handled", "j", env=env, check=True)
    out = run("jobctl.py", "watch", env=env)
    assert out.returncode == 0 and "nothing needs attention" in out.stdout


def stop_hook(env, **event):
    out = run("queue_check.py", env=env, stdin=json.dumps(event))
    assert out.returncode == 0
    return json.loads(out.stdout)["hookSpecificOutput"]["additionalContext"] if out.stdout.strip() else None


def test_stop_hook_only_acts_when_unattended(tmp_path, env):
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    assert stop_hook(env) is None
    (tmp_path / "runs/UNATTENDED").touch()
    assert "no ready task" in stop_hook(env)


def test_stop_hook_rules(tmp_path, env):
    runs = tmp_path / "runs"
    (runs / "UNATTENDED").touch()
    assert stop_hook(env) is None  # GPU busy
    env["LONGRUN_FAKE_GPUS"] = "0:0:0,1:20000:99"
    (runs / "queue.json").write_text(json.dumps([{"id": "pad", "status": "ready"}]))  # no line/why: not counted
    assert stop_hook(env, stop_hook_active=True) is None  # already continuing because of a stop hook
    assert "no ready task" in stop_hook(env)
    half = {"id": "t0", "line": "L3", "why": "row 2", "status": "ready"}  # no decision_if / dedup: not counted
    (runs / "queue.json").write_text(json.dumps([half, dict(half, id="t0b", decision_if="x")]))  # t0b: no dedup
    assert "no ready task" in stop_hook(env)
    (runs / "hooks.log").unlink()
    full = dict(half, id="t1", decision_if="beats d30: switch default", dedup_checked=True)
    (runs / "queue.json").write_text(json.dumps([full]))
    assert "ready task t1" in stop_hook(env)
    assert "ready task t1" in stop_hook(env)
    assert stop_hook(env) is None  # third refusal within an hour is skipped (cap 2)


def test_stop_hook_respects_blocking_question_and_soft_default(tmp_path, env):
    runs = tmp_path / "runs"
    (runs / "UNATTENDED").touch()
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    (runs / "questions.json").write_text(json.dumps(
        [{"id": "q1", "question": "add rival X?", "blocks": False, "default": "skip X", "status": "open"}]))
    assert "proceed with its default ('skip X')" in stop_hook(env)
    (runs / "questions.json").write_text(json.dumps(
        [{"id": "q2", "question": "spend $200?", "blocks": True, "default": "no", "status": "open"}]))
    assert stop_hook(env) is None


def test_stop_hook_survives_garbage_input(env):
    out = run("queue_check.py", env=env, stdin="not json")
    assert out.returncode == 0 and out.stdout == ""


def test_context_inject_is_short_and_labelled(tmp_path, env):
    runs = tmp_path / "runs"
    (runs / "decisions.md").write_text("\n".join(f"- [user-study] 10-{i:02d} PI: decision {i}" for i in range(40)))
    (runs / "questions.json").write_text(json.dumps([{"id": "q1", "question": "x" * 500, "blocks": True}]))
    out = run("context_inject.py", env=env).stdout
    assert out.startswith("[long-run state") and "decision 39" in out and "decision 30" not in out
    assert len(out) <= 1500 + 1


def test_wait_for_gpu(env):
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    out = run("wait_for_gpu.py", "--interval", "0.01", env=env)
    assert out.returncode == 0 and "idle GPUs: 0" in out.stdout
    env["LONGRUN_FAKE_GPUS"] = "0:9000:99"
    assert run("wait_for_gpu.py", "--interval", "0.01", "--timeout-min", "0.001", env=env).returncode == 3


def test_resume_check(tmp_path, env):
    runs = tmp_path / "runs"
    activity = tmp_path / "transcript.jsonl"
    activity.write_text("{}")
    args = ["--activity", str(activity), "--resume-cmd", "echo WAKE {reason}", "--quiet-min", "0"]
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    assert run("resume_check.py", *args, env=env).stdout == ""  # attended: never wakes
    (runs / "UNATTENDED").touch()
    out = run("resume_check.py", *args, env=env)
    assert "WAKE" in out.stdout and "no ready task" in out.stdout
    assert run("resume_check.py", *args, env=env).stdout == ""  # cooldown
    os.utime(activity, None)
    (runs / "resume.json").unlink()
    busy = run("resume_check.py", *args[:-2], "--quiet-min", "60", env=env)
    assert busy.stdout == ""  # agent active recently


def test_stop_hook_lets_a_question_stay_the_last_message(tmp_path, env):
    runs = tmp_path / "runs"
    (runs / "UNATTENDED").touch()
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    assert stop_hook(env, last_assistant_message="Queue refilled.") is not None
    assert stop_hook(env, last_assistant_message="Results above. ❓ Needs input: switch default to d50?") is None
    assert "asks_user" in (runs / "hooks.log").read_text()


def test_stop_hook_refusal_restates_blocking_questions(tmp_path, env):
    runs = tmp_path / "runs"
    (runs / "UNATTENDED").touch()
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    (runs / "questions.json").write_text(json.dumps(
        [{"id": "q2", "line": "L5", "question": "spend $200 on API?", "blocks": True, "status": "open"}]))
    task = {"id": "t1", "line": "L3", "why": "row 2", "decision_if": "x", "dedup_checked": True}
    (runs / "queue.json").write_text(json.dumps([task]))
    reason = stop_hook(env)
    assert "ready task t1" in reason and "restate" in reason and "spend $200" in reason


def test_padding_suspects_and_no_count_threshold(tmp_path, env):
    runs = tmp_path / "runs"
    (runs / "UNATTENDED").touch()
    env["LONGRUN_FAKE_GPUS"] = "0:0:0"
    reason = stop_hook(env)
    assert "idle_ok.json" in reason and "at least" not in reason
    block_time = (runs / "hooks.log").read_text().split("\t")[0]
    from datetime import datetime, timedelta
    t0 = datetime.fromisoformat(block_time)
    tasks = [{"id": "rushed", "line": "L3", "why": "w", "created": (t0 + timedelta(minutes=2)).isoformat()},
             {"id": "planned", "line": "L3", "why": "w", "created": (t0 - timedelta(hours=2)).isoformat()}]
    (runs / "queue.json").write_text(json.dumps(tasks))
    out = run("queue_check.py", "--suspects", env=env).stdout
    assert "rushed" in out and "planned" not in out
    assert "possible padding" in run("context_inject.py", env=env).stdout
