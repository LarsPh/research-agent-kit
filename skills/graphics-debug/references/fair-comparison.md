# Fair Side-by-Side Comparison

Use when comparing outputs of different methods or representations (Gaussian splats, meshes, point clouds).

## 1. Normalise

- Gaussian splats: drop low-opacity outliers (for example opacity < 0.1) before computing the centre and the
  bounding sphere.
- glTF / GLB: bake node transforms into the vertices first.
- Scale both to a unit bounding sphere centred at the origin. Record the transform so it can be undone.

## 2. Fix the Orientation

1. Render a thumbnail for each candidate rotation, including mirrored candidates (`det = -1`). A search over
   proper rotations only will report a "best" alignment for a mirrored input instead of flagging it.
2. Put the candidates in one labelled grid beside the reference and ask which is upright and facing forward
   (the protocol in step 3 of the main skill). Low confidence goes to the user.

## 3. Align in 3D

Coarse-to-fine search on voxel occupancy IoU (for example 30³ voxels, 45° then 15° steps), then refine with
ICP. Report geometric metrics (Chamfer distance, F-score, normal consistency) as a CSV next to the images.

## 4. Render

- Same camera path, intrinsics, and resolution for both.
- Render colour plus a clay image (depth → screen-space normals → Lambert) with the same code for both
  methods, so shading differences do not pass as geometry differences.
- If the renderers must differ, say so on the figure.

## 5. QC

- Log the non-background pixel ratio per frame to catch empty frames.
- Sample frames during rotation and check both objects face the same way.

Keep object lists and paths as arguments, not constants in the script.
