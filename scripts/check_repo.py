#!/usr/bin/env python3
"""Repository checks for research-agent-kit, run by CI and before committing.

Each check prints one line per problem as `path: message`. Exit status is 1 when any check fails.
Checks: skill frontmatter, agents/openai.yaml, relative Markdown links, README coverage, private
information, trailing whitespace, and Python syntax.
"""
import py_compile
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Anthropic's skill rules: name <= 64 characters without reserved words; description <= 1024 characters.
NAME_MAX, DESC_MAX, SKILL_MD_MAX_LINES = 64, 1024, 500
RESERVED = ("anthropic", "claude")
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".template", ".toml", ".sh"}
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
# Private information the public repository must not carry (AGENTS.md: no private hostnames or paths).
PRIVATE_PATTERNS = [
    (re.compile(r"/home/(?!user\b|you\b|<)[a-z_][a-z0-9_-]*/"), "absolute home path"),
    (re.compile(r"/Users/(?!<)[A-Za-z][\w.-]*/"), "absolute macOS home path"),
    (re.compile(r"[A-Za-z]:\\\\?Users\\\\?[A-Za-z]"), "Windows user path"),
    (re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}(?:\.\d{1,3})?\b"), "private IP address"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com|anthropic\.com|example\.(?:com|org))[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b"), "email address"),
]

problems = []


def report(path, message):
    problems.append(f"{path.relative_to(ROOT)}: {message}")


def tracked_text_files():
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix in TEXT_SUFFIXES or path.name.endswith(".template"):
            yield path


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]) if end != -1 else None


def check_skills():
    names = []
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            report(skill_dir, "missing SKILL.md")
            continue
        try:
            meta = frontmatter(skill_md)
        except yaml.YAMLError as exc:
            report(skill_md, f"frontmatter is not valid YAML: {exc}")
            continue
        if not isinstance(meta, dict):
            report(skill_md, "missing frontmatter")
            continue
        if set(meta) != {"name", "description"}:
            report(skill_md, f"frontmatter must hold only name and description, found {sorted(meta)}")
        name, desc = str(meta.get("name", "")), str(meta.get("description", ""))
        names.append(name)
        if name != skill_dir.name:
            report(skill_md, f"name '{name}' differs from its folder '{skill_dir.name}'")
        if not NAME_RE.match(name) or len(name) > NAME_MAX or any(w in name for w in RESERVED):
            report(skill_md, f"invalid name '{name}'")
        if not desc or len(desc) > DESC_MAX or "<" in desc or ">" in desc:
            report(skill_md, f"description empty, over {DESC_MAX} characters, or contains angle brackets")
        lines = skill_md.read_text(encoding="utf-8").count("\n")
        if lines > SKILL_MD_MAX_LINES:
            report(skill_md, f"{lines} lines; move detail into references/ (limit {SKILL_MD_MAX_LINES})")

        agent_yaml = skill_dir / "agents" / "openai.yaml"
        if not agent_yaml.is_file():
            report(skill_dir, "missing agents/openai.yaml")
            continue
        try:
            interface = (yaml.safe_load(agent_yaml.read_text(encoding="utf-8")) or {}).get("interface", {})
        except yaml.YAMLError as exc:
            report(agent_yaml, f"not valid YAML: {exc}")
            continue
        for key in ("display_name", "short_description", "default_prompt"):
            if not interface.get(key):
                report(agent_yaml, f"interface.{key} is missing")
        if f"${name}" not in str(interface.get("default_prompt", "")):
            report(agent_yaml, f"default_prompt must contain ${name}")
    return names


def check_readmes(names):
    for readme in ("README.md", "README.zh-CN.md"):
        path = ROOT / readme
        text = path.read_text(encoding="utf-8")
        for name in names:
            if f"(skills/{name}/SKILL.md)" not in text:
                report(path, f"skill '{name}' is not listed")


def check_links():
    for path in tracked_text_files():
        if path.suffix != ".md":
            continue
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                report(path, f"broken link {target}")


def check_text_hygiene():
    for path in tracked_text_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line != line.rstrip():
                report(path, f"line {number}: trailing whitespace")
            for pattern, label in PRIVATE_PATTERNS:
                if pattern.search(line):
                    report(path, f"line {number}: {label}")


def check_python():
    for path in sorted(ROOT.rglob("*.py")):
        if ".git" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            report(path, f"syntax error: {exc.msg}")


def main():
    names = check_skills()
    check_readmes(names)
    check_links()
    check_text_hygiene()
    check_python()
    for line in problems:
        print(line)
    print(f"{len(names)} skills checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
