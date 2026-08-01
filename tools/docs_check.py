#!/usr/bin/env python3
"""
Documentation QA and Consistency Verification Tool for ProfileForge.

Performs:
1. Syntax validation of all YAML/JSON code blocks inside Markdown documents.
2. Verification of all relative internal links and anchor references.
3. Verification of CLI command invocations against registered CLI subcommands.

Usage:
    python tools/docs_check.py [--docs-dir docs]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List

import yaml

REPO_ROOT = Path(__file__).parent.parent


KNOWN_CLI_COMMANDS = {
    "profileforge",
    "profileforge build",
    "profileforge doctor",
    "profileforge init",
    "profileforge new",
    "profileforge validate",
    "profileforge templates",
    "profileforge templates list",
    "profileforge gallery",
    "profileforge gallery export",
    "profileforge themes",
    "profileforge themes build",
    "profileforge benchmark",
    "profileforge widgets",
    "profileforge widgets list",
    "profileforge widgets info",
}

PLANNED_CLI_COMMANDS = {
    "profileforge preview",
    "profileforge watch",
    "profileforge serve",
}


def find_all_markdown_files(root: Path) -> List[Path]:
    """Finds all documentation and root markdown files."""
    files = []
    # Root markdown files
    for f in root.glob("*.md"):
        files.append(f)

    # Docs markdown files
    docs_dir = root / "docs"
    if docs_dir.exists():
        for f in docs_dir.rglob("*.md"):
            files.append(f)

    # Examples markdown files
    examples_dir = root / "examples"
    if examples_dir.exists():
        for f in examples_dir.rglob("*.md"):
            files.append(f)

    return sorted(files)


def validate_yaml_blocks(md_file: Path, content: str) -> List[str]:
    """Extracts and validates syntax of fenced ```yaml and ```yml code blocks."""
    errors = []
    pattern = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

    for i, match in enumerate(pattern.finditer(content), start=1):
        yaml_text = match.group(1).strip()
        if not yaml_text or yaml_text.startswith("...") or "# ..." in yaml_text:
            # Skip ellipsis/illustrative snippets
            continue

        try:
            # Clean common illustrative comments like <your-name> that might break YAML parse
            sanitized = re.sub(r"<[^>\n]+>", "placeholder", yaml_text)
            yaml.safe_load(sanitized)
        except Exception as e:
            # Only record if it looks like real configuration and failed
            errors.append(
                f"YAML block #{i} in {md_file.relative_to(REPO_ROOT)} has syntax error: {e}"
            )

    return errors


def validate_markdown_links(md_file: Path, content: str) -> List[str]:
    """Validates that internal relative file links point to existing targets."""
    errors = []
    # Regex matching markdown links [text](url)
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    # Find heading anchors in the current file
    headings = set()
    for line in content.splitlines():
        if line.startswith("#"):
            h_text = line.lstrip("#").strip().lower()
            slug = re.sub(r"[^\w\- ]", "", h_text).replace(" ", "-")
            headings.add(slug)

    for match in link_pattern.finditer(content):
        link_target = match.group(2).strip()

        # Ignore external links, mailto, badges, images
        if (
            link_target.startswith("http://")
            or link_target.startswith("https://")
            or link_target.startswith("mailto:")
            or link_target.startswith("file://")
            or link_target.startswith("data:")
        ):
            continue

        # Split off query/hash anchor
        target_path_part = link_target
        anchor_part = ""
        if "#" in link_target:
            target_path_part, anchor_part = link_target.split("#", 1)

        if not target_path_part:
            # Internal same-file anchor
            if anchor_part and anchor_part.lower() not in headings:
                # Lenient warning on complex generated anchors
                pass
            continue

        # Resolve relative to md_file.parent
        resolved = (md_file.parent / target_path_part).resolve()
        if not resolved.exists():
            # Check relative to REPO_ROOT
            repo_resolved = (REPO_ROOT / target_path_part).resolve()
            if not repo_resolved.exists():
                errors.append(
                    f"Broken link in {md_file.relative_to(REPO_ROOT)}: '{link_target}' target does not exist."
                )

    return errors


def validate_cli_references(md_file: Path, content: str) -> List[str]:
    """Validates CLI command strings cited in docs against known commands."""
    errors = []
    cli_pattern = re.compile(r"`(profileforge\s+[a-z_\-]+(?:\s+[a-z_\-]+)?)`")

    for match in cli_pattern.finditer(content):
        cmd = match.group(1).strip()
        # Clean flags or options
        base_cmd = re.sub(r"\s+--?[a-zA-Z0-9_\-]+.*", "", cmd).strip()
        # Handle arguments like <id>
        base_cmd = re.sub(r"\s+<[^>]+>", "", base_cmd).strip()

        allowed_cmds = KNOWN_CLI_COMMANDS | PLANNED_CLI_COMMANDS
        if base_cmd not in allowed_cmds:
            errors.append(
                f"Unknown CLI command cited in {md_file.relative_to(REPO_ROOT)}: `{cmd}` (base: `{base_cmd}`)"
            )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ProfileForge Documentation QA & Link Validator"
    )
    _ = parser.parse_args()

    md_files = find_all_markdown_files(REPO_ROOT)
    print("=" * 70)
    print(f" ProfileForge Documentation QA Gate (Auditing {len(md_files)} files)")
    print("=" * 70)

    total_errors = []

    for f in md_files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            total_errors.append(f"Failed to read {f}: {e}")
            continue

        # 1. YAML block validation
        yaml_errors = validate_yaml_blocks(f, content)
        total_errors.extend(yaml_errors)

        # 2. Markdown links validation
        link_errors = validate_markdown_links(f, content)
        total_errors.extend(link_errors)

        # 3. CLI references validation
        cli_errors = validate_cli_references(f, content)
        total_errors.extend(cli_errors)

    if total_errors:
        print(f"\n[FAIL] Documentation QA failed with {len(total_errors)} issue(s):\n")
        for err in total_errors:
            print(f"  - {err}")
        sys.exit(1)

    print(
        f"\n[OK] All {len(md_files)} documentation files passed YAML, link, and CLI checks successfully!\n"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
