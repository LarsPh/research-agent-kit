---
name: paper-code-bootstrap
description: Set up newly cloned research/paper code repositories into runnable uv-based inference environments. Use when Codex needs to convert README/requirements install instructions into pyproject.toml or uv workflows, install and validate dependencies including CUDA extensions, download checkpoints/models/config assets, and smoke-test an inference/demo command on an appropriate GPU node.
---

# Paper Code Bootstrap

Use this skill to turn a fresh research repository into a reproducible local demo/inference setup. Optimize for a working smoke test first, not perfect packaging.

## Workflow

1. Inspect before changing anything:
   - Read `README*`, `requirements*.txt`, `environment*.yml`, `pyproject.toml`, setup files, demo scripts, and examples.
   - Search for checkpoint/model download logic: `from_pretrained`, `snapshot_download`, `hf_hub_download`, `ckpt`, `model_path`, `pretrained`, `download`.
   - Identify entrypoints: CLI demo, WebUI, notebook, inference script, or example JSON.

2. Build the uv dependency plan:
   - Prefer a repo-local `.venv` and `uv run`.
   - Create or update `pyproject.toml` from the repo's pinned dependencies.
   - Preserve exact pins when possible, but fix impossible pins only when verified by the resolver.
   - Represent git dependencies explicitly with PEP 508 direct references.
   - Identify optional acceleration dependencies separately from required runtime dependencies.
   - Before installing optional acceleration packages (for example custom attention kernels, xFormers, FlashAttention, SageAttention, bitsandbytes, TensorRT, or other CUDA extensions), tell the user the expected benefit/risk and ask whether to install them.
   - Add uv build hints for undeclared native build deps, for example:
     ```toml
     [tool.uv.extra-build-dependencies]
     some_cuda_package = ["torch==<matching-version>"]
     ```

3. Install on the right machine:
   - Do filesystem edits and lightweight checks on the file server.
   - Do CUDA extension builds, `nvcc` checks, CUDA smoke tests, and inference on a GPU node.
   - Before heavy inference, run `nvidia-smi` and choose one idle GPU.
   - For shared venvs across multiple GPU architectures, compile CUDA extensions with all needed SMs, e.g. `TORCH_CUDA_ARCH_LIST="8.6;8.9"` for RTX A5000/A6000 and Ada cards.

4. Download required assets:
   - Prefer the code's native download path if it is clear.
   - Otherwise use official model hubs or README links.
   - For Hugging Face, consider a project-local cache for reproducibility:
     ```fish
     set -x HF_HOME /path/to/repo/hf_cache
     set -x HF_HUB_DISABLE_XET 1
     ```
   - Resume interrupted downloads rather than restarting large files.

5. Validate in layers:
   - Import smoke test: `torch`, CUDA availability, CUDA extension imports, and key packages.
   - Model-load smoke test if affordable.
   - Minimal inference/demo test before full sweeps or WebUI.
   - Prefer CLI inference over WebUI for first validation because it has fewer moving parts.

6. Leave runnable commands:
   - Provide fish-compatible commands for setup, validation, and demo.
   - Include GPU-node and SSH forwarding instructions if a WebUI is involved.
   - Note any deviations from upstream requirements, optional dependencies skipped/installed, and residual risks.

7. Write a repo-local memo:
   - Create a concise Markdown file such as `SETUP_DEMO_NOTES.md`, `LOCAL_DEMO.md`, or a project-specific name.
   - Include install decisions, uv commands, checkpoint/cache locations, optional acceleration dependency decisions, GPU architecture notes, demo commands, WebUI forwarding commands, and known failure modes.
   - Keep it practical for future recall; prefer copy-pasteable fish commands.

8. Final response requirements:
   - Report the most common demo command(s) the user should run.
   - Mention where the memo Markdown file was written.
   - Call out whether optional acceleration dependencies were installed, skipped, or still awaiting user choice.

## Lab Defaults

- Use `uv run python ...` instead of plain `python`.
- Use GPU nodes for CUDA builds/inference; do not run heavy GPU jobs on the file server.
- Use one GPU per job unless the user explicitly asks otherwise.
- Set memory helpers when useful:
  ```fish
  set -x PYTORCH_CUDA_ALLOC_CONF expandable_segments:True
  ```
- For WebUIs bound to `127.0.0.1` on GPU nodes, use two-hop SSH forwarding through the file server when the local PC cannot reach GPU nodes directly.

## Checklists

For a compact checklist and common failure modes, read `references/bootstrap-checklist.md`.
