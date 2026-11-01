"""Render the trained point model from a novel view (pinhole camera, z-buffer)."""
import numpy as np
from PIL import Image
from loader import load_dataset, load_pose

K, _, _, (W, H) = load_dataset("data")
c2w = load_pose("data/novel_view.json")
m = np.load("model.npz")
w2c = np.linalg.inv(c2w)
pc = (w2c[:3, :3] @ m["xyz"].T + w2c[:3, 3:4]).T
img = np.full((H, W, 3), 255, np.uint8); zb = np.full((H, W), np.inf)
keep = pc[:, 2] > 0.05
uv = (K @ pc[keep].T).T; uv = (uv[:, :2] / uv[:, 2:]).round().astype(int)
for (u, v), z, col in zip(uv, pc[keep, 2], m["rgb"][keep]):
    for du in (0, 1):
        for dv in (0, 1):
            x, y = u + du, v + dv
            if 0 <= x < W and 0 <= y < H and z < zb[y, x]:
                zb[y, x] = z; img[y, x] = col
Image.fromarray(img).save("novel_render.png")
print("points in front of camera:", int(keep.sum()), "/", len(keep))
