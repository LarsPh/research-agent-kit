# Research Development Environment Template

These instructions describe a common research-code environment for coding agents. They are a public template; replace placeholders with your own machine names, paths, and policies.

## Machine Layout And GPU Workflow

- Use `<file-server>` for code editing, file operations, dependency inspection, lightweight CPU checks, and general project setup.
- `<file-server>` may have faster shared filesystem access but no GPU.
- Use GPU nodes such as `<gpu-node-01>` through `<gpu-node-N>` for CUDA runtime checks, CUDA extension builds, `nvcc` compilation, and inference/training validation.
- GPU nodes may contain multiple GPUs. Use only one GPU per job unless the user explicitly requests multi-GPU execution.
- Before heavy GPU jobs, run `nvidia-smi` on the chosen GPU node and pick an idle GPU. Avoid GPUs already used by other people.
- CUDA-related builds should run on a GPU node so the build environment sees CUDA correctly.

## Python And Package Management

- Prefer `uv` as the default Python package manager.
- Prefer a project-local `.venv`.
- Prefer `uv run python ...` instead of plain `python ...` unless the project documents a different launcher.
- Use complete runnable commands:

```fish
uv run python train.py
uv run python scripts/eval.py
uv run python -m pytest
CUDA_VISIBLE_DEVICES=0 uv run python scripts/smoke_test.py
```

## Shell And Command Style

- Prefer fish-compatible commands in user-facing instructions when the user works in fish.
- If Bash syntax is necessary, label it clearly as Bash.
- Do not assume CUDA paths, compiler settings, aliases, shell functions, or environment variables from memory. Inspect local shell config files when they matter.
- Common local config files to inspect may include:
  - `~/.bashrc`
  - `~/.config/fish/config.fish`
  - `~/.config/shell/common_env.sh`
  - `~/.config/fish/export_bash_vars.sh`

## CUDA Extension Compatibility

- When a `.venv` is shared across GPU models, compile CUDA extensions for all GPU architectures that may run the environment.
- Example for RTX A5000/A6000 and Ada-generation cards:

```fish
set -x TORCH_CUDA_ARCH_LIST "8.6;8.9"
```

- If a cached wheel was compiled for the wrong GPU architecture, force a source rebuild:

```fish
uv pip install --no-cache --reinstall-package <pkg> --no-deps --no-binary <pkg> --no-build-isolation <specifier>
```

## Coding-Agent Expectations

- After changing code, always provide concrete commands to run or test the modified code.
- For complex changes, run or propose a minimal smoke test before full experiments.
- If GPU validation is needed, remind the user to run it on an available GPU node after checking `nvidia-smi`.
- For CUDA or compiler issues, first check active CUDA, compiler, `PATH`, `LD_LIBRARY_PATH`, and shell environment bridging before proposing large code changes.
- Do not launch heavy GPU jobs blindly.
- Keep commands practical for a normal workflow using `tmux`, fish, `uv`, and a project-local `.venv`.

## WebUI Forwarding Pattern

If the local PC can only SSH to `<file-server>`, and `<file-server>` can SSH to `<gpu-node>`, use two-hop forwarding for WebUIs bound to `127.0.0.1` on the GPU node.

On `<file-server>`:

```fish
ssh -N -L 17860:127.0.0.1:7860 <gpu-node>
```

On the local PC:

```fish
ssh -N -L 17860:127.0.0.1:17860 <file-server-alias>
```

Then open:

```text
http://localhost:17860
```
