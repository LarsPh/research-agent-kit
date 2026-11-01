"""Dataset loader for transforms.json scenes."""
import json, os
import numpy as np
import cv2


def load_dataset(root):
    meta = json.load(open(os.path.join(root, "transforms.json")))
    K = np.array([[meta["fl_x"], 0, meta["cx"]], [0, meta["fl_y"], meta["cy"]], [0, 0, 1]])
    images, poses = [], []
    for fr in meta["frames"]:
        img = cv2.imread(os.path.join(root, fr["file_path"]))  # uint8 HxWx3
        images.append(img.astype(np.float32) / 255.0)
        c2w = np.array(fr["transform_matrix"])            # camera-to-world
        c2w[:3, 2] *= -1  # transforms.json cameras look down -Z; we look down +Z
        poses.append(c2w)
    return K, np.stack(images), np.stack(poses), (meta["w"], meta["h"])


def load_pose(path):
    c2w = np.array(json.load(open(path))["transform_matrix"])
    c2w[:3, 2] *= -1  # transforms.json cameras look down -Z; we look down +Z
    return c2w
