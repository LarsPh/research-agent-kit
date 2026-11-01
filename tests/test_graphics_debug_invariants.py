"""Tests for skills/graphics-debug/scripts/invariants.py."""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "skills/graphics-debug/scripts/invariants.py"
spec = importlib.util.spec_from_file_location("invariants", SCRIPT)
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)

MIRROR_X = np.diag([-1.0, 1.0, 1.0])


def rot_y(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def test_rotation_passes_proper_and_flags_mirror():
    ok, _ = inv.check_rotation(np.stack([rot_y(0.3), rot_y(-1.0)]))
    assert ok
    ok, report = inv.check_rotation(np.stack([rot_y(0.3), MIRROR_X @ rot_y(0.3)]))
    assert not ok and report["mirrored_indices"] == [1]


def test_rotation_flags_scale():
    ok, report = inv.check_rotation(2.0 * rot_y(0.1))
    assert not ok and report["scaled_indices"] == [0]


def test_handedness_catches_mirror_that_rotation_check_misses():
    # A mirrored export stores rotations as S @ R @ S: still det +1.
    conj = np.stack([MIRROR_X @ rot_y(a) @ MIRROR_X for a in (0.2, 0.4)])
    assert inv.check_rotation(conj)[0]
    left, up, fwd = np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]), np.array([[0, 0, 1.0]])
    assert inv.check_handedness(left, up, fwd)[0]
    ok, report = inv.check_handedness(left @ MIRROR_X, up, fwd)
    assert not ok and report["mirrored_fraction"] == 1.0


def test_quat_flips():
    q = np.array([[1.0, 0, 0, 0], [0.99, 0.141, 0, 0], [-0.98, -0.199, 0, 0]])
    q /= np.linalg.norm(q, axis=1, keepdims=True)
    ok, report = inv.check_quat_flips(q)
    assert not ok and report["sign_flip_at"] == [2]
    with pytest.raises(ValueError):
        inv.check_quat_flips(np.zeros((1, 4)))


def test_fps():
    ok, report = inv.check_fps(np.arange(31) / 30.0)
    assert ok and report["fps"] == pytest.approx(30.0)
    ok, report = inv.check_fps(np.array([0.0, 0.1, 0.1, 0.3]))
    assert not ok and report["non_increasing_at"] == [1]


def test_stats_flags_nan_and_constant():
    assert not inv.check_stats(np.array([0.0, np.nan]))[0]
    assert not inv.check_stats(np.zeros((4, 4), np.uint8))[0]
    assert inv.check_stats(np.linspace(0, 1, 10))[0]


def test_reproject_and_behind_camera():
    k = np.array([[100.0, 0, 50], [0, 100.0, 50], [0, 0, 1]])
    x3d = np.random.default_rng(0).random((20, 3)) + [0, 0, 2]
    uv = (k @ x3d.T).T
    uv = uv[:, :2] / uv[:, 2:]
    ok, report = inv.check_reproject(k, np.eye(4), x3d, uv)
    assert ok and report["median_px"] < 1e-9
    flip = np.diag([1.0, -1.0, -1.0, 1.0])  # OpenGL axes used as OpenCV
    ok, report = inv.check_reproject(k, flip, x3d, uv)
    assert not ok and report["behind_camera"] == 20


def test_cli_exit_codes(tmp_path):
    path = tmp_path / "poses.npy"
    np.save(path, np.stack([np.eye(3), MIRROR_X]))
    assert inv.main(["invariants.py", "rotation", str(path)]) == 1
    assert inv.main(["invariants.py", "rotation", str(tmp_path / "missing.npy")]) == 2
    assert inv.main(["invariants.py", "unknown"]) == 2
