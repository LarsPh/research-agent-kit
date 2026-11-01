---
name: graphics-debug
description: Diagnoses wrong-looking renders and 3D results in graphics and 3D-vision code (NeRF, Gaussian splatting, meshes, cameras, avatars and motion, panoramas, video). Turns what an image shows into ranked candidate causes, then confirms each cause with a numeric invariant check. Use when a render, reconstruction, pose, or comparison looks wrong, even if the user only says it "looks off"; before comparing two methods side by side; or when an agent inspects its own renders. Triggers include 渲染不对, 画面异常, 看图找原因, 坐标系, 镜像, 朝向, 公平对比.
---

# Graphics Debug

Images show where something looks wrong; invariant checks prove why. An image alone cannot separate causes
that look the same (a mirror and a 180° turn of a symmetric object), and a passing metric can hide a render
that is plainly broken, so each conclusion needs both.

Copy this checklist and tick it off:

```
Graphics debug:
- [ ] 1. Comparison is valid (frame, camera, renderer, time)
- [ ] 2. Diagnostic sheet rendered
- [ ] 3. Symptoms described, not judged
- [ ] 4. Candidate causes ranked
- [ ] 5. Cause confirmed by an invariant check
- [ ] 6. Fixed one variable; same sheet and check pass
```

## 1. Make the Comparison Valid

Most "method A is worse" findings in 3D come from comparing unlike things. Before judging any image, check:

- same canonical frame, scale, and up axis (normalise both; for comparing methods follow
  [fair-comparison.md](references/fair-comparison.md));
- same intrinsics, resolution, pose, renderer, and shading;
- frames matched by real timestamps, not frame index, when frame rates may differ.

If the renderers must differ, label the figure so the difference is not read as a method difference.

## 2. Render One Fixed Diagnostic Sheet

Render the same fixed views every time, in one image: result, ground truth (if any), difference, depth, alpha
(opacity), and normals or an untextured clay render. Add one held-out view and, for motion, a strip of
frames. RGB alone rarely separates causes; depth and alpha usually do. Keeping the views fixed makes the
before and after sheets comparable.

## 3. Describe Before Judging

When a VLM or you read the sheet:

1. Describe first, using the symptom names in [symptom-table.md](references/symptom-table.md): where, what it
   looks like, and in which views. Asking for a verdict or a cause first invites a plausible story.
2. When comparing versions or picking among candidates, hide method names, randomise left and right, label
   candidates with letters, and place the reference beside them. VLMs favour whichever looks "newer" or sits
   in a fixed position.
3. Ask for a reason and a confidence. Hand low-confidence calls to the user rather than guessing.

## 4. Rank Candidate Causes

Look up each symptom in [symptom-table.md](references/symptom-table.md). Fix position before quality: a wrong
pose also produces blur, holes, and floaters, so quality symptoms often disappear once position is right.
Within position, suspect in this order and stop at the first proven fault:

1. the comparison setup (step 1);
2. coordinate system and axis convention ([conventions.md](references/conventions.md));
3. handedness (mirror, `det = -1`);
4. absolute orientation (constant 180° yaw, wrong forward axis);
5. the algorithm itself.

The order runs from cheap and common to expensive and rare. Within one symptom, do the same.

## 5. Confirm With an Invariant Check

Confirm each candidate with a check from [invariants.md](references/invariants.md). For time offset, global
mirror, constant yaw, and quaternion sign flips the check is required whatever the image shows, because
every single frame of these failures looks plausible.

Run `scripts/invariants.py` for the standard checks (rotation, handedness, quaternion flips, frame rate,
value range, reprojection); it needs only numpy. A mirror can hide inside valid rotations (`S @ R @ S` has
`det = +1`), so check handedness on a frame built from the data, not only on stored matrices. When two
causes fit the images (mirror vs 180° turn), fit each and compare residuals. Write the pass threshold before looking at the number.

## 6. Fix One Variable at a Time

Change one thing, re-render the same sheet, rerun the same check. To find the stage that breaks, switch
stages on and off one by one and rerun the check. After three rounds without progress, stop and report what
was ruled out; further guessing tends to change several things at once and loses the trail.

## Done When

- the same diagnostic sheet looks right in every view, and the invariant check that confirmed the cause passes;
- the record reads: symptom → confirmed cause (with the check) → change → after sheet;
- unresolved symptoms are listed as open, not reported as fixed.

Save a cause to project memory only after the fix is reproduced.
