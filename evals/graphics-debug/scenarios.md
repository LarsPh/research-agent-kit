# Evaluation Scenarios

Three scenarios per Anthropic's "build evaluations first" guidance. Each is run twice in a fresh context: with
the skill and without it, on the same small fixture repository. Pass means every expected behaviour appears.

## 1. Mirrored avatar that looks fine

Fixture (`fixtures/make_mirrored_motion.py`): one take exported twice; B negates X in the joints and stores
root rotations as `S @ R @ S` (det +1). Front-view stick-figure renders of both.
Prompt: "motion_a.npz 和 motion_b.npz 是同一段动作从两个 exporter 导出的，renders/ 里两段渲染出来看着差不多，但 b 用 retarget.py 重定向到角色上之后动作看着不对劲。帮我找出原因。"
Expected:
- checks handedness on a frame built from the joints, not only det of the stored rotations (the fixture stores S @ R @ S, det +1);
- names the X mirror as the cause, with the handedness or residual numbers as evidence;
- does not blame the retarget algorithm before ruling out frame and handedness.

## 2. Gaussian splatting comparison with different normalisation

Fixture (`fixtures/make_unfair_splat_compare.py`): two splat outputs of the same chair; B is scaled 2.5×,
rotated 90° about Y, shifted, and has 300 faint floaters. One shared render script with fixed bounds.
Prompt: "Method B looks much worse than method A in these side-by-side renders (renders/compare.png, made with render.py). Write up why method B is worse."
Expected:
- checks the comparison setup first and finds the frame and scale mismatch;
- normalises both (outlier filter, unit sphere) before any quality claim;
- does not report "method B is worse" from the original renders.

## 3. Colour and pose bug in a NeRF loader

Fixture (`fixtures/make_nerf_loader_bugs.py` + `nerf_loader_code/`): a loader that reads images with OpenCV
(BGR, so the trained colours are BGR) and converts OpenGL `transforms.json` cameras by flipping only the
Z axis (a mirrored camera). A held-out GT photo of the novel view.
Prompt: "新视角渲染（render_novel.py 输出的 novel_render.png）颜色发蓝，而且物体位置不对，训练 loss 正常。gt/novel_gt.png 是这个视角的真实照片。帮我找原因并修好。"
Expected:
- fixes position before colour;
- names the OpenGL vs OpenCV camera axes and confirms with reprojection or a known-pose render;
- names BGR vs RGB and confirms on a known-colour region;
- changes one thing at a time and re-renders the same views after each.
