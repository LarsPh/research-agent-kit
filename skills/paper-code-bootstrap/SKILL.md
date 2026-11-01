---
name: paper-code-bootstrap
description: Sets up newly cloned research or paper code repositories as runnable uv-based inference environments. Use when an agent needs to convert README or requirements install instructions into pyproject.toml or uv workflows, install and validate dependencies including CUDA extensions, download checkpoints, models, or config assets, and smoke-test an inference or demo command on a suitable GPU machine. Triggers include 跑通, 配环境, 复现 demo, 装依赖.
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
   - Follow the platform profile (see Platform Profile below) for where to edit files, where to build, and
     where to run GPU work.
   - Do CUDA extension builds, `nvcc` checks, CUDA smoke tests, and inference on a machine with a GPU.
   - Before heavy inference, run `nvidia-smi` and choose one idle GPU.
   - For an environment shared across GPU architectures, compile CUDA extensions for every compute
     capability that will run it: read each GPU's capability with
     `nvidia-smi --query-gpu=name,compute_cap --format=csv` and set `TORCH_CUDA_ARCH_LIST` to the list.

4. Download required assets:
   - Prefer the code's native download path if it is clear.
   - Otherwise use official model hubs or README links.
   - For Hugging Face, consider a project-local cache for reproducibility:
     ```sh
     export HF_HOME=/path/to/repo/hf_cache
     ```
   - Resume interrupted downloads rather than restarting large files.

5. Validate in layers:
   - Import smoke test: `torch`, CUDA availability, CUDA extension imports, and key packages.
   - Model-load smoke test if affordable.
   - Minimal inference/demo test before full sweeps or WebUI.
   - Prefer CLI inference over WebUI for first validation because it has fewer moving parts.

6. Leave runnable commands:
   - Provide commands for setup, validation, and demo in the user's shell (from the profile; POSIX `sh`
     when unknown).
   - Include SSH forwarding instructions if a WebUI runs on a remote machine.
   - Note any deviations from upstream requirements, optional dependencies skipped/installed, and residual risks.

7. Write a repo-local memo:
   - Create a concise Markdown file such as `SETUP_DEMO_NOTES.md`, `LOCAL_DEMO.md`, or a project-specific name.
   - Include install decisions, uv commands, checkpoint/cache locations, optional acceleration dependency decisions, GPU architecture notes, demo commands, WebUI forwarding commands, and known failure modes.
   - Keep it practical for future recall; prefer copy-pasteable commands.

8. Final response requirements:
   - Report the most common demo command(s) the user should run.
   - Mention where the memo Markdown file was written.
   - Call out whether optional acceleration dependencies were installed, skipped, or still awaiting user choice.

## Platform Profile

Machines, shells, and GPU rules differ between labs, so this skill keeps none of them. Before step 3, look
for a platform profile, in this order:

1. a compute or platform section in the target repository's `AGENTS.md` or `CLAUDE.md`;
2. a profile file the user names, for example one filled in from this kit's
   [platform-profile template](https://github.com/LarsPh/research-agent-kit/blob/main/templates/platform-profile.md.template).

Follow it for: which machine edits files and which runs GPU work, the shell, GPUs per job, cache locations,
memory settings, and how to forward a WebUI port. Without a profile, discover what you can (`hostname`,
`nvidia-smi`, `$SHELL`, scheduler commands), ask only for what discovery cannot settle, and default to
`uv run python`, one GPU per job, and POSIX `sh` commands.

## Checklists

For a compact checklist and common failure modes, read `references/bootstrap-checklist.md`.
