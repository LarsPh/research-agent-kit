# /// script
# requires-python = ">=3.9"
# dependencies = ["numpy"]
# ///
"""Numeric invariant checks for graphics debugging.

Run one check per call; every check prints a JSON report and exits 1 when it fails.

  python scripts/invariants.py rotation poses.npy        # (N,4,4) or (N,3,3) or one matrix
  python scripts/invariants.py quat-flips quats.npy      # (N,4), consecutive keys
  python scripts/invariants.py fps timestamps.npy        # (N,) seconds
  python scripts/invariants.py stats array.npy           # any numeric array (image, depth, alpha)
  python scripts/invariants.py reproject K.npy w2c.npy points3d.npy points2d.npy
  python scripts/invariants.py handedness left.npy up.npy forward.npy   # (N,3) each, from the data itself

Inputs are .npy files so the script does not guess file formats; convert first.
"""
import json
import sys

import numpy as np

# Tolerances: float32 pose files usually keep about 1e-5 relative precision; 1e-3 leaves room for
# poses that went through a few multiplications without flagging real errors.
ORTHO_TOL = 1e-3
DET_TOL = 1e-3
# Reprojection: a few pixels is typical for SfM poses at full resolution.
REPROJ_PX = 3.0


def check_rotation(m):
    m = np.asarray(m, dtype=np.float64)
    if m.ndim == 2:
        m = m[None]
    r = m[:, :3, :3]
    dets = np.linalg.det(r)
    ortho = np.abs(r @ np.transpose(r, (0, 2, 1)) - np.eye(3)).max(axis=(1, 2))
    mirrored = np.where(dets < 0)[0].tolist()
    non_ortho = np.where(ortho > ORTHO_TOL)[0].tolist()
    scaled = np.where(np.abs(np.abs(dets) - 1) > DET_TOL)[0].tolist()
    ok = not (mirrored or non_ortho or scaled)
    return ok, {
        "count": int(len(r)),
        "det_min": float(dets.min()),
        "det_max": float(dets.max()),
        "mirrored_indices": mirrored[:20],
        "non_orthonormal_indices": non_ortho[:20],
        "scaled_indices": scaled[:20],
        "hint": "det<0: mirror; |det|!=1 or non-orthonormal: scale baked in or wrong matrix layout",
    }


def check_quat_flips(q):
    q = np.asarray(q, dtype=np.float64)
    if q.ndim != 2 or q.shape[1] != 4 or len(q) < 2:
        raise ValueError(f"expected (N,4) with N>=2, got {q.shape}")
    norms = np.linalg.norm(q, axis=1)
    dots = np.einsum("ij,ij->i", q[1:], q[:-1])
    flips = (np.where(dots < 0)[0] + 1).tolist()
    ok = not flips and np.allclose(norms, 1, atol=1e-3)
    return ok, {
        "count": int(len(q)),
        "sign_flip_at": flips[:20],
        "norm_min": float(norms.min()),
        "norm_max": float(norms.max()),
        "hint": "negate q_t where dot(q_t, q_{t-1}) < 0 before interpolating; order (w,x,y,z) vs (x,y,z,w) is not detected here",
    }


def check_fps(t):
    t = np.asarray(t, dtype=np.float64).ravel()
    if len(t) < 2:
        raise ValueError("need at least 2 timestamps")
    dt = np.diff(t)
    fps = (len(t) - 1) / (t[-1] - t[0])
    irregular = np.where(np.abs(dt - np.median(dt)) > 0.5 * np.median(dt))[0].tolist()
    ok = bool((dt > 0).all()) and not irregular
    return ok, {
        "fps": float(fps),
        "non_increasing_at": np.where(dt <= 0)[0].tolist()[:20],
        "irregular_gaps_at": irregular[:20],
        "hint": "compare fps between the two sequences; align by time, not frame index",
    }


def check_stats(a):
    a = np.asarray(a)
    f = a.astype(np.float64)
    finite = np.isfinite(f)
    report = {
        "dtype": str(a.dtype),
        "shape": list(a.shape),
        "nan": int(np.isnan(f).sum()),
        "inf": int(np.isinf(f).sum()),
        "min": float(f[finite].min()) if finite.any() else None,
        "max": float(f[finite].max()) if finite.any() else None,
        "mean": float(f[finite].mean()) if finite.any() else None,
        "hint": "range [0,255] vs [0,1] vs [-1,1]; all equal values often means an empty mask or a dead stage",
    }
    ok = report["nan"] == 0 and report["inf"] == 0 and report["min"] != report["max"]
    return ok, report


def check_reproject(k, w2c, x3d, x2d):
    k = np.asarray(k, dtype=np.float64)
    w2c = np.asarray(w2c, dtype=np.float64)
    x3d = np.asarray(x3d, dtype=np.float64)
    x2d = np.asarray(x2d, dtype=np.float64)
    cam = (w2c[:3, :3] @ x3d.T + w2c[:3, 3:4]).T
    behind = int((cam[:, 2] <= 0).sum())
    uv = (k @ cam.T).T
    uv = uv[:, :2] / uv[:, 2:3]
    err = np.linalg.norm(uv - x2d, axis=1)
    med = float(np.median(err))
    ok = behind == 0 and med <= REPROJ_PX
    return ok, {
        "points": int(len(x3d)),
        "behind_camera": behind,
        "median_px": med,
        "p90_px": float(np.percentile(err, 90)),
        "hint": "assumes OpenCV camera (x right, y down, z forward) and world-to-camera; "
        "many points behind the camera suggests c2w/w2c swapped or OpenGL axes",
    }


def check_handedness(left, up, forward):
    """Mirror check on data, not on rotation matrices.

    A mirrored export often stores rotations as S @ R @ S, which still has det = +1, so the rotation
    check passes. Build the frame from the data instead (for a body: left hip minus right hip, pelvis to
    head, nose direction): in a right-handed frame cross(left, up) points along forward.
    """
    l, u, f = (np.asarray(a, dtype=np.float64).reshape(-1, 3) for a in (left, up, forward))
    s = np.einsum("ij,ij->i", np.cross(l, u), f)
    bad = np.where(s <= 0)[0].tolist()
    return not bad, {
        "count": int(len(s)),
        "mirrored_indices": bad[:20],
        "mirrored_fraction": float(len(bad) / len(s)),
        "hint": "all frames mirrored: the whole export is mirrored; some frames: left/right labels swap mid-sequence. "
        "For a left-handed source (Unity, Unreal) expect all frames to fail before conversion",
    }


CHECKS = {
    "rotation": (check_rotation, 1),
    "quat-flips": (check_quat_flips, 1),
    "fps": (check_fps, 1),
    "stats": (check_stats, 1),
    "reproject": (check_reproject, 4),
    "handedness": (check_handedness, 3),
}


def main(argv):
    if len(argv) < 2 or argv[1] not in CHECKS:
        print(__doc__)
        return 2
    fn, nargs = CHECKS[argv[1]]
    paths = argv[2:]
    if len(paths) != nargs:
        print(f"{argv[1]} needs {nargs} .npy path(s), got {len(paths)}", file=sys.stderr)
        return 2
    try:
        arrays = [np.load(p, allow_pickle=False) for p in paths]
        ok, report = fn(*arrays)
    except (OSError, ValueError) as e:
        print(json.dumps({"check": argv[1], "error": str(e)}))
        return 2
    print(json.dumps({"check": argv[1], "pass": bool(ok), **report}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
