# Symptom → Candidate Causes

Candidates are listed in checking order (common and cheap first). A row gives candidates, not a verdict:
confirm with [invariants.md](invariants.md). When several symptoms appear together, fix the position rows
first.

## Position

| Symptom | Candidates, in order | Quick check |
|---|---|---|
| Image mirrored or upside down | 1. Axis convention (OpenCV vs OpenGL/Blender: y and z flipped) 2. Image flipped on load or save 3. c2w and w2c swapped 4. Mirrored input geometry (`det = -1`) | Render an asymmetric object (text, a known asset) at a GT pose; compute `det` of the transform, and the handedness of a frame built from the data |
| Whole scene shifted, rotated, or wrong scale | 1. Extrinsic convention (c2w/w2c, transpose, Euler order, quaternion wxyz vs xyzw) 2. Units (m vs cm) 3. Scene normalisation not undone | Project known 3D points (SfM points) and check they land on the image features |
| Object faces the wrong way, consistently | 1. Different forward axis between tools 2. Constant 180° yaw | Compare absolute forward with the reference at an anchor frame, not relative angles |
| Turns the opposite way, or left and right limbs swapped | 1. Whole sequence mirrored on export (rotations stored as `S @ R @ S` still have det +1) 2. Left/right joint labels swapped | Handedness of the data frame; fit both hypotheses (mirror vs label swap vs 180° yaw) and compare residuals |
| Image stretched or wrong aspect | 1. Image resized without rescaling intrinsics 2. fx/fy or width/height swapped 3. cx/cy in pixels vs normalised | Check the image size and the intrinsics refer to the same resolution |
| Motion out of sync, every frame plausible | 1. Frame rates differ, aligned by index 2. Dropped or duplicated frames | Align by real time; recompute fps = (n − 1) / (t_end − t_start) |
| Jumps or flips between frames | 1. Quaternion sign flip before interpolation 2. Euler wrap-around 3. Pose jitter | Check `dot(q_t, q_{t-1}) < 0`; plot angles over time |

## Quality

| Symptom | Candidates, in order | Quick check |
|---|---|---|
| Red and blue swapped, washed out, or overexposed | 1. BGR vs RGB 2. Gamma applied twice or not at all (sRGB vs linear) 3. Range [0,1] vs [-1,1] vs [0,255] 4. Premultiplied alpha | Look at a known colour; red-blue swap is almost always BGR |
| Training views good, novel views bad | 1. Too few views (overfitting) 2. Pose error 3. Floaters | Evaluate held-out views; check if floaters sit near training cameras |
| Close-up views blurry | 1. Resolution or downsampling 2. Little close-range supervision 3. Near plane and sampling 4. Gaussians too large, no anti-aliasing | Add a closer view or higher resolution and see if it sharpens |
| Black holes | 1. Region no view saw 2. Wrong depth 3. Alpha not accumulating to 1 4. Near/far or culling clipping | Alpha map low = nothing there; depth jump = depth problem |
| Sky or far background turns to holes or noise | 1. No sky mask or background model 2. Far plane too close | Check the mask covers the sky; raise far and compare |
| Floaters, spikes | 1. Densification thresholds 2. Pose noise 3. No depth or regularisation term | View points or Gaussians from above or far away |
| Seam in a panorama | 1. Equirect left and right edges not wrapped 2. Cube-map face orientation 3. No padding at the seam | Roll the panorama by half its width and look again |
| Stripes, grids, blocks | 1. Aliasing 2. Tile or patch-wise decoding borders 3. Interpolation mode | Check whether the spacing equals the tile or patch size |
| Flicker across video frames | 1. Per-frame random seed 2. Pose jitter 3. Frames generated independently | Fix seed and pose and regenerate |
| Mesh faces black or inside out | 1. Flipped normals or winding order 2. Back-face culling 3. Mirrored transform (`det = -1` flips winding) | Disable culling; show the normal map |
| All black, all white, or NaN | 1. NaN in the loss 2. Empty mask 3. Dtype overflow (uint8) | Print value range and NaN count |
| Empty frame in a turntable or sequence | 1. Object outside the frustum after normalisation 2. Wrong camera index | Log the non-background pixel ratio per frame |
