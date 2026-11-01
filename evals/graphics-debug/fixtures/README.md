# Fixtures

Each script writes one scenario's fixture into the directory given as its argument (needs numpy, matplotlib;
the NeRF one also needs opencv-python and Pillow).

| Scenario | Command | Notes |
|---|---|---|
| 1 Mirrored motion | `python make_mirrored_motion.py <dir>` | writes motion_a/b.npz, renders, retarget.py, README.md |
| 2 Unfair splat comparison | `python make_unfair_splat_compare.py <dir>`, then `python render.py` inside `<dir>` | B is the same chair in another frame, plus faint floaters |
| 3 NeRF loader bugs | `python make_nerf_loader_bugs.py <dir>`, then copy `nerf_loader_code/*` into `<dir>` | loader reads BGR and flips only the camera Z axis |

Give each run its own copy of the fixture, and give the baseline run no access to the skill files.
