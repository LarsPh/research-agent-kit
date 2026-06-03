# Bootstrap Checklist

## Discovery

- Read install and demo docs.
- List files with `rg --files`.
- Search model and checkpoint loading code.
- Identify exact Python version assumptions if present.
- Check whether CUDA extensions are imported at module import time.

## pyproject.toml

- Include `requires-python`.
- Convert package pins from `requirements.txt`.
- Keep git dependencies as direct references:
  ```toml
  "pkg @ git+https://github.com/org/repo.git@commit"
  ```
- If uv cannot build a CUDA package because `torch` is missing during isolated build, add:
  ```toml
  [tool.uv.extra-build-dependencies]
  pkg = ["torch==X.Y.Z"]
  ```
- If an upstream pin is impossible, change only that pin and record the reason.
- Separate required dependencies from optional acceleration dependencies. Ask the user before installing optional accelerators that add CUDA build risk.

## CUDA Extension Installs

- Check active CUDA and compiler:
  ```fish
  which nvcc
  nvcc --version
  echo $CUDA_HOME
  ```
- Compile shared environments for all likely GPUs:
  ```fish
  set -x TORCH_CUDA_ARCH_LIST "8.6;8.9"
  ```
- If a cached wheel was built for the wrong architecture, force source rebuild:
  ```fish
  uv pip install --no-cache --reinstall-package <pkg> --no-deps --no-binary <pkg> --no-build-isolation <specifier>
  ```

## Model Assets

- Prefer project-local cache for large Hugging Face assets:
  ```fish
  set -x HF_HOME /path/to/repo/hf_cache
  set -x HF_HUB_DISABLE_XET 1
  ```
- Verify large downloads by loading the model or checking expected snapshot files.
- If a repo needs auth, tell the user to run `huggingface-cli login` on the GPU node.

## Validation

- Import smoke:
  ```fish
  uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
  ```
- CUDA extension smoke: call a tiny kernel if possible, not only import.
- Demo smoke: run the smallest documented CLI inference.
- For WebUI: test CLI first, then start the server and provide SSH tunnels.

## Final Handoff

- Write a repo-local Markdown memo with:
  - install commands and any pyproject deviations
  - checkpoint/model cache paths
  - optional acceleration dependencies installed or skipped
  - CUDA architecture/build notes
  - common demo commands
  - WebUI forwarding commands if applicable
  - known failure modes and fixes
- In the final user response, include the common demo command(s) and the memo file path.

## Common Failures

- `No module named torch` during CUDA package build: missing build dependency or build isolation issue.
- `no kernel image is available`: extension was compiled for the wrong SM architecture.
- OOM in renderer/export rather than model forward: reduce video rendering, FPS, resolution, or use safer camera paths.
- WebUI `Failed to fetch`: frontend is calling the wrong forwarded host/port; prefer same-origin backend URLs where possible.
