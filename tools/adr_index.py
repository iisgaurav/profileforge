#!/usr/bin/env python3
"""
Architecture Decision Record (ADR) Indexer and Validator for ProfileForge.

Scans `docs/adr/*.md`, validates ADR sequence numbering, required sections,
and statuses, and generates or checks `docs/adr/README.md`.

Usage:
    python tools/adr_index.py [--check] [--dir docs/adr]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ADRMetadata:
    number: int
    id_str: str
    title: str
    status: str
    date: str
    filename: str
    filepath: Path


VALID_STATUSES = {"Accepted", "Proposed", "Deprecated", "Superseded", "Rejected"}


def parse_adr_file(filepath: Path) -> Optional[ADRMetadata]:
    content = filepath.read_text(encoding="utf-8")

    # Match title: # ADR-001: Title
    title_match = re.search(r"^#\s+(ADR-(\d+)):\s*(.+)$", content, re.MULTILINE)
    if not title_match:
        # Fallback to general # Title
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if not h1_match:
            return None
        title = h1_match.group(1).strip()
        num_match = re.search(r"ADR-(\d+)", filepath.name)
        if not num_match:
            return None
        num = int(num_match.group(1))
        id_str = f"ADR-{num:03d}"
    else:
        id_str = title_match.group(1)
        num = int(title_match.group(2))
        title = title_match.group(3).strip()

    # Match status and date: **Accepted** (2026-08-02) or Status: Accepted
    status = "Proposed"
    date = "Unknown"

    status_block_match = re.search(
        r"##\s+Status\s*\n+[\*\_]*([A-Za-z]+)[\*\_]*\s*(?:\(([\d\-]+)\))?",
        content,
        re.IGNORECASE,
    )
    if status_block_match:
        raw_status = status_block_match.group(1).capitalize()
        if raw_status in VALID_STATUSES:
            status = raw_status
        if status_block_match.group(2):
            date = status_block_match.group(2)

    return ADRMetadata(
        number=num,
        id_str=id_str,
        title=title,
        status=status,
        date=date,
        filename=filepath.name,
        filepath=filepath,
    )


def validate_adrs(adrs: List[ADRMetadata]) -> List[str]:
    errors = []
    if not adrs:
        return ["No ADR files found to validate."]

    seen_numbers = set()
    for adr in adrs:
        if adr.number in seen_numbers:
            errors.append(f"Duplicate ADR number found: {adr.id_str} ({adr.filename})")
        seen_numbers.add(adr.number)

        if adr.status not in VALID_STATUSES:
            errors.append(
                f"Invalid status '{adr.status}' in {adr.filename}. Expected one of: {VALID_STATUSES}"
            )

        # Check required sections
        content = adr.filepath.read_text(encoding="utf-8")
        for section in ["Context", "Decision", "Consequences"]:
            if not re.search(rf"##\s+.*{section}", content, re.IGNORECASE):
                errors.append(
                    f"Missing required section '## {section}' in {adr.filename}"
                )

    # Check numbering sequence
    sorted_numbers = sorted(seen_numbers)
    for idx, num in enumerate(sorted_numbers, start=1):
        if num != idx:
            errors.append(
                f"Discontinuous ADR numbering: expected ADR-{idx:03d}, found ADR-{num:03d}"
            )

    return errors


def generate_index_markdown(adrs: List[ADRMetadata]) -> str:
    lines = [
        "# Architecture Decision Records (ADRs)",
        "",
        "This directory contains the formal Architecture Decision Records for the ProfileForge engine.",
        "",
        "| ADR | Title | Status | Date |",
        "|---|---|---|---|",
    ]

    for adr in sorted(adrs, key=lambda a: a.number):
        lines.append(
            f"| [{adr.id_str}]({adr.filename}) | {adr.title} | {adr.status} | {adr.date} |"
        )

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ProfileForge ADR Indexer and Validator"
    )
    parser.add_argument("--dir", default="docs/adr", help="Path to ADR directory")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: verify index and fail on diff/errors",
    )
    args = parser.parse_args()

    adr_dir = Path(args.dir)
    if not adr_dir.exists():
        print(f"[FAIL] ADR directory '{adr_dir}' not found.")
        sys.exit(1)

    adr_files = sorted(
        [f for f in adr_dir.glob("*.md") if f.name.upper() != "README.MD"]
    )

    adrs: List[ADRMetadata] = []
    for f in adr_files:
        meta = parse_adr_file(f)
        if meta:
            adrs.append(meta)

    errors = validate_adrs(adrs)
    if errors:
        print(f"[FAIL] ADR validation failed with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    generated_md = generate_index_markdown(adrs)
    readme_path = adr_dir / "README.md"

    if args.check:
        if not readme_path.exists():
            print(f"[FAIL] {readme_path} does not exist.")
            sys.exit(1)
        current_md = readme_path.read_text(encoding="utf-8")
        if current_md.strip() != generated_md.strip():
            print(
                f"[FAIL] {readme_path} is out of date. Run 'python tools/adr_index.py' to update."
            )
            sys.exit(1)
        print(f"[OK] ADR index and {len(adrs)} ADR(s) verified successfully.")
        sys.exit(0)

    readme_path.write_text(generated_md, encoding="utf-8")
    print(
        f"[OK] Successfully indexed and validated {len(adrs)} ADR(s) -> {readme_path}"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
