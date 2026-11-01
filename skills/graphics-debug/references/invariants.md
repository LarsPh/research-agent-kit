# Invariant Checks

The checks marked `script` run with `python scripts/invariants.py <check> <files.npy>`; it prints JSON and
exits 1 on failure.

## What Images Cannot Show

These failures look plausible in every single image, so a VLM, however strong, will pass them. Run the check.

| Failure | Why images miss it | Check |
|---|---|---|
| Time offset from different frame rates | Every frame is a plausible pose | (`script: fps`) Align by real time; recompute fps = (n − 1) / (t_end − t_start) |
| Global mirror | Labels and keypoints still look right; symmetric bodies look normal | (`script: handedness`) Build left, up, forward from the data (left hip − right hip, pelvis → head, nose direction); `cross(left, up)` must point along forward. A mirrored export often stores rotations as `S @ R @ S`, which keeps `det = +1`, so `det` of the stored rotations alone does not catch it |
| Constant 180° yaw | Relative angles match exactly | Angle between absolute forward and the reference at an anchor frame |
| Quaternion sign flip | Shows only when interpolating between keys | (`script: quat-flips`) Per key, `dot(q_t, q_{t-1}) < 0` |
| Wrong colour space on a dark render | Dark images hide orientation and tone errors | Never judge orientation from one dark render; use a skeleton or clay overlay |

## Checks

| Question | Check | Pass |
|---|---|---|
| Is the transform a proper rotation? (`script: rotation`) | `det(R)`, `R @ R.T` | `det = +1`, `R @ R.T ≈ I`. Passing does not rule out a mirror; see the handedness check |
| Does a pose match the images? (`script: reproject`) | Project known 3D points (SfM, markers) | Reprojection error within a few pixels |
| Are intrinsics consistent with the image? | Compare the intrinsics' resolution with the image | Same size; cx, cy near the centre |
| Same direction as the reference? | Cosine of bone or forward vectors | Close to 1 for every segment |
| Are two shapes aligned? | Voxel IoU, then Chamfer distance, F-score, normal consistency | Above the threshold set before looking |
| Are values sane? (`script: stats`) | min, max, mean, NaN and Inf counts per stage | In the expected range, zero NaN |
| Which stage breaks? | Turn each stage on or off (A/B) and rerun the same check | The first stage that changes the result |

Write the pass threshold before running the check, not after seeing the number.
