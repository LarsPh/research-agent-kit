#!/usr/bin/env python3
"""Collect multi-worktree research output into a pack directory, then zip it.

collect: per-worktree commit log, diff stat and status for a time window, copies of included files,
         and manifest.json. The agent writes digest.md afterwards.
zip:     archive the pack directory (after digest.md exists).
"""

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
CJK_RANGES = ((0x3000, 0x9FFF), (0xAC00, 0xD7AF), (0xF900, 0xFAFF))


def git(repo, *args, check=True):
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed in {repo}: {result.stderr.strip()}")
    return result.stdout.strip()


def parse_worktree(spec):
    path, _, name = spec.partition("=")
    root = Path(git(Path(path).expanduser(), "rev-parse", "--show-toplevel"))
    return {"name": name or root.name, "root": root}


def window_base(root, since):
    """Last commit before the window, or the root commit's parent (empty tree) when none exists."""
    base = git(root, "rev-list", "-1", f"--before={since}", "HEAD", check=False)
    return base or git(root, "hash-object", "-t", "tree", "/dev/null")


def estimate_tokens(text):
    cjk = sum(1 for ch in text if any(lo <= ord(ch) <= hi for lo, hi in CJK_RANGES))
    return int((len(text) - cjk) / 4 + cjk / 1.5)


def owning_line(path, lines):
    matches = [line for line in lines if path.is_relative_to(line["root"])]
    return max(matches, key=lambda line: len(line["root"].parts)) if matches else None


def collect(args):
    out = Path(args.out).expanduser()
    if out.exists() and any(out.iterdir()) and not args.force:
        raise SystemExit(f"{out} is not empty; pass --force to overwrite")
    out.mkdir(parents=True, exist_ok=True)
    lines = [parse_worktree(spec) for spec in args.worktree]
    manifest = {
        "created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "since": args.since,
        "lines": [],
        "files": [],
    }

    for line in lines:
        root, name = line["root"], line["name"]
        line_dir = out / "lines" / name
        line_dir.mkdir(parents=True, exist_ok=True)
        base = window_base(root, args.since)
        head = git(root, "rev-parse", "HEAD")
        log = git(root, "log", f"--since={args.since}", "--date=iso", "--format=%h %ad %s", "HEAD")
        (line_dir / "log.txt").write_text(log + "\n", encoding="utf-8")
        (line_dir / "diffstat.txt").write_text(
            git(root, "diff", "--stat=200", base, head) + "\n", encoding="utf-8"
        )
        (line_dir / "status.txt").write_text(git(root, "status", "--short") + "\n", encoding="utf-8")
        line.update(branch=git(root, "branch", "--show-current") or "detached", head=head)
        manifest["lines"].append(
            {
                "name": name,
                "worktree": str(root),
                "branch": line["branch"],
                "base": base,
                "head": head,
                "commits_in_window": len(log.splitlines()),
            }
        )

    for spec in args.include:
        source = Path(spec).expanduser().resolve()
        if not source.is_file():
            raise SystemExit(f"include not found or not a file: {spec}")
        line = owning_line(source, lines)
        if line is None:
            raise SystemExit(f"include is outside every --worktree: {spec}")
        rel = source.relative_to(line["root"])
        commit = git(line["root"], "log", "-1", "--format=%h", "--", str(rel), check=False)
        short = commit or line["head"][:8] + "-untracked"
        if source.suffix.lower() in IMAGE_SUFFIXES:
            dest = out / "images" / f"{line['branch'].replace('/', '-')}__{short}__{source.name}"
            kind = "image"
        else:
            dest = out / "docs" / line["name"] / rel
            kind = "text"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        manifest["files"].append(
            {
                "pack_path": str(dest.relative_to(out)),
                "line": line["name"],
                "branch": line["branch"],
                "commit": commit or None,
                "source_path": str(rel),
                "kind": kind,
                "bytes": dest.stat().st_size,
            }
        )

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    report_size(out)


def report_size(out):
    text_tokens, image_count, total = 0, 0, 0
    for path in out.rglob("*"):
        if not path.is_file():
            continue
        total += path.stat().st_size
        if path.suffix.lower() in IMAGE_SUFFIXES:
            image_count += 1
        else:
            text_tokens += estimate_tokens(path.read_text(encoding="utf-8", errors="replace"))
    print(
        json.dumps(
            {"pack": str(out), "bytes": total, "images": image_count, "text_tokens_estimate": text_tokens},
            ensure_ascii=False,
        )
    )


def make_zip(args):
    out = Path(args.out).expanduser()
    if not (out / "digest.md").is_file():
        raise SystemExit(f"{out}/digest.md is missing; write the digest before zipping")
    archive = out.with_suffix(".zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(out.rglob("*")):
            if path.is_file():
                zf.write(path, Path(out.name) / path.relative_to(out))
    report_size(out)
    print(json.dumps({"zip": str(archive), "zip_bytes": archive.stat().st_size}))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_collect = sub.add_parser("collect", help="collect logs, diff stats and included files")
    p_collect.add_argument("--worktree", action="append", required=True, metavar="PATH[=NAME]",
                           help="worktree to summarize; repeat per research line")
    p_collect.add_argument("--since", required=True, help="window start, any git date (e.g. 2026-09-01)")
    p_collect.add_argument("--out", required=True, help="pack directory to create")
    p_collect.add_argument("--include", action="append", default=[], metavar="FILE",
                           help="report or image to copy; must live inside one --worktree")
    p_collect.add_argument("--force", action="store_true", help="allow a non-empty --out")
    p_collect.set_defaults(func=collect)

    p_zip = sub.add_parser("zip", help="zip the pack directory once digest.md exists")
    p_zip.add_argument("--out", required=True, help="pack directory created by collect")
    p_zip.set_defaults(func=make_zip)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
