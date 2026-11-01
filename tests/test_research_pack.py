"""Tests for skills/research-pack/scripts/pack.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "skills/research-pack/scripts/pack.py"


def run(*args, check=True):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=check)


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def worktree(tmp_path):
    repo = tmp_path / "line"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "exp/a")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "report.md").write_text("# Result\n\nloss 0.1\n", encoding="utf-8")
    (repo / "fig.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "first result")
    return repo


def test_collect_writes_manifest_and_copies(worktree, tmp_path):
    out = tmp_path / "pack"
    run("collect", "--worktree", f"{worktree}=lineA", "--since", "1 year ago", "--out", str(out),
        "--include", str(worktree / "report.md"), "--include", str(worktree / "fig.png"))
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["lines"][0]["name"] == "lineA"
    assert manifest["lines"][0]["commits_in_window"] == 1
    kinds = {f["source_path"]: f["kind"] for f in manifest["files"]}
    assert kinds == {"report.md": "text", "fig.png": "image"}
    assert (out / "docs/lineA/report.md").is_file()
    assert any(p.name.startswith("exp-a__") for p in (out / "images").iterdir())
    assert "first result" in (out / "lines/lineA/log.txt").read_text(encoding="utf-8")


def test_include_outside_worktree_is_rejected(worktree, tmp_path):
    stray = tmp_path / "stray.md"
    stray.write_text("x", encoding="utf-8")
    result = run("collect", "--worktree", str(worktree), "--since", "1 year ago",
                 "--out", str(tmp_path / "pack"), "--include", str(stray), check=False)
    assert result.returncode != 0 and "outside every --worktree" in result.stderr


def test_zip_requires_digest(worktree, tmp_path):
    out = tmp_path / "pack"
    run("collect", "--worktree", str(worktree), "--since", "1 year ago", "--out", str(out))
    assert run("zip", "--out", str(out), check=False).returncode != 0
    (out / "digest.md").write_text("# Digest\n", encoding="utf-8")
    run("zip", "--out", str(out))
    assert (tmp_path / "pack.zip").is_file()


def test_non_empty_out_needs_force(worktree, tmp_path):
    out = tmp_path / "pack"
    out.mkdir()
    (out / "old.txt").write_text("x", encoding="utf-8")
    result = run("collect", "--worktree", str(worktree), "--since", "1 year ago", "--out", str(out), check=False)
    assert result.returncode != 0 and "--force" in result.stderr
