# Coordinate Conventions

Each row gives its source. Conventions differ between library versions and between datasets built on the same
library, so when a row matters, confirm it against the version in use, or measure it (render an asymmetric
object; check which axis the head or the up vector points along).

| System | Handedness | World up | Camera looks along | Camera up | Source / note |
|---|---|---|---|---|---|
| OpenCV / COLMAP camera | right | depends on data | +Z | −Y (image y points down) | COLMAP output format docs: X right, Y down, Z forward; `images.txt` stores world-to-camera, quaternion (w, x, y, z), Hamilton |
| 3D Gaussian Splatting (reference code) | right | from COLMAP | +Z | −Y | Uses COLMAP cameras; its NeRF-synthetic loader flips camera Y and Z ("OpenGL/Blender camera axes (Y up, Z back) to COLMAP (Y down, Z forward)") |
| OpenGL camera | right | +Y by habit | −Z | +Y | Same as three.js and glTF cameras below |
| NeRF / nerfstudio `transforms.json` | right | +Z | −Z | +Y | nerfstudio data conventions: OpenGL/Blender camera axes; matrix columns are camera axes and origin (camera-to-world); world up +Z |
| Blender | right | +Z | −Z (camera local) | +Y (camera local) | Blender manual: Z points up; Y axis is Front/Back. Camera with zero rotation looks straight down |
| three.js | right | +Y | −Z | +Y | three.js `Camera` docs: looks down its local negative z-axis |
| glTF 2.0 | right | +Y | −Z | +Y | Spec §3.4: +Y up, +Z forward, −X right, asset front faces +Z, metres; §3.10: camera lens looks toward −Z |
| PyTorch3D | right | +Y | +Z | +Y | PyTorch3D cameras docs: +X left, +Y up, +Z into the scene; NDC (+1, +1) is top left |
| Unity | left | +Y | +Z | +Y | Unity manual: left-hand coordinate system; `Vector3.forward` = (0, 0, 1) |
| Unreal Engine | left | +Z | +X | +Z | UE docs: left-handed, Z up, +X forward, +Y right; default unit is the centimetre |
| AMASS motion data | right | +Z | — | — | Z up, +Y forward (stated in NVIDIA Kimodo's SMPL-X export code, not in AMASS docs) |
| SMPL / SMPL-X template | right | usually +Y | — | — | No official statement found. The rest template is commonly Y up, facing +Z; rendered with OpenCV cameras it appears upside down until rotated 180° about X. Measure before relying on it |

## Common Conversions

- OpenCV ↔ OpenGL camera: negate the camera's Y and Z axes (`diag(1, −1, −1)` on the camera side).
- c2w ↔ w2c: matrix inverse. Transpose inverts only the rotation part.
- Quaternion order: SciPy `Rotation.from_quat` defaults to (x, y, z, w) (`scalar_first=False`); COLMAP uses
  (w, x, y, z).
- Euler angles: record the axis order and whether rotations are intrinsic or extrinsic.
- Row-major vs column-major storage reads as a transpose.
- Left-handed ↔ right-handed (Unity, Unreal ↔ the rest): negate one axis, which flips triangle winding
  (`det = -1`); re-check normals afterwards.

Sources (checked 2026-11-01): colmap.github.io/format.html, docs.nerf.studio/quickstart/data_conventions.html,
registry.khronos.org/glTF/specs/2.0/glTF-2.0.html, pytorch3d.org/docs/cameras, threejs.org/docs (Camera),
docs.blender.org/manual (3D viewport, viewpoint), Unity manual (Rotation and orientation), Unreal Engine docs
(Coordinate System and Spaces), docs.scipy.org (Rotation.from_quat).
