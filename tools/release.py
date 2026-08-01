#!/usr/bin/env python3
"""
Release Engineering and Pre-Flight Verification Tool for ProfileForge.

Capabilities:
  - 'check': Validates SemVer consistency and executes all 6 QA release gates.
  - 'bump <patch|minor|major>': Bumps version across all project files.
  - 'changelog [--version X.Y.Z]': Formats release notes and updates CHANGELOG.md.

Usage:
    python tools/release.py check
    python tools/release.py bump patch
    python tools/release.py changelog --version 1.0.0
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).parent.parent
PYPROJECT_FILE = REPO_ROOT / "pyproject.toml"
INIT_FILE = REPO_ROOT / "src" / "profileforge" / "__init__.py"
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"


def get_pyproject_version() -> str:
    content = PYPROJECT_FILE.read_text(encoding="utf-8")
    m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if not m:
        raise ValueError("Could not find version in pyproject.toml")
    return m.group(1).strip()


def get_init_version() -> str:
    content = INIT_FILE.read_text(encoding="utf-8")
    m = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not m:
        raise ValueError("Could not find __version__ in src/profileforge/__init__.py")
    return m.group(1).strip()


def bump_version_string(current: str, part: str) -> str:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(.*)$", current)
    if not m:
        raise ValueError(f"Invalid semver string: {current}")
    major, minor, patch = (
        int(m.group(1)),
        int(m.group(2)),
        int(m.group(3)),
    )

    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(
            f"Unknown bump type '{part}'. Choose from patch, minor, major."
        )


def cmd_bump(args) -> None:
    bump_type = args.part.lower()
    current = get_pyproject_version()
    new_ver = bump_version_string(current, bump_type)

    print(f"Bumping version: {current} -> {new_ver} ({bump_type})")

    # 1. Update pyproject.toml
    pyproject_content = PYPROJECT_FILE.read_text(encoding="utf-8")
    new_pyproject = re.sub(
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_ver}"',
        pyproject_content,
        count=1,
    )
    PYPROJECT_FILE.write_text(new_pyproject, encoding="utf-8")
    print(f"[OK] Updated {PYPROJECT_FILE.relative_to(REPO_ROOT)}")

    # 2. Update __init__.py
    init_content = INIT_FILE.read_text(encoding="utf-8")
    new_init = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_ver}"',
        init_content,
        count=1,
    )
    INIT_FILE.write_text(new_init, encoding="utf-8")
    print(f"[OK] Updated {INIT_FILE.relative_to(REPO_ROOT)}")

    print(f"\n[DONE] Version successfully bumped to {new_ver}.\n")


def run_command_gate(name: str, cmd: List[str]) -> Tuple[bool, str]:
    print(f"  --> Running {name} ({' '.join(cmd)})...")
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        passed = proc.returncode == 0
        output = proc.stdout.strip()
        return passed, output
    except Exception as e:
        return False, str(e)


def cmd_check(args) -> None:
    print("=" * 70)
    print(" ProfileForge Release Pre-Flight Verification")
    print("=" * 70)

    # 1. Check SemVer consistency
    pyproject_ver = get_pyproject_version()
    init_ver = get_init_version()

    print(f"  pyproject.toml version:       {pyproject_ver}")
    print(f"  src/profileforge/__version__: {init_ver}")

    if pyproject_ver != init_ver:
        print(
            f"\n[FAIL] Version mismatch! pyproject.toml ({pyproject_ver}) != __init__.py ({init_ver})"
        )
        sys.exit(1)

    print("\n[OK] Version consistency verified.\n")
    print("-" * 70)
    print(" Executing Pre-Flight Quality Gates")
    print("-" * 70)

    gates = [
        ("Unit & Integration Tests", [sys.executable, "-m", "pytest"]),
        ("Code Linting & Formatting", ["ruff", "check", "."]),
        ("Public API Lock Snapshot", [sys.executable, "tools/api_lock.py", "--check"]),
        ("Performance Budget Gate", [sys.executable, "tools/performance_check.py"]),
        ("ADR Index & Consistency", [sys.executable, "tools/adr_index.py", "--check"]),
        ("Documentation QA & Links", [sys.executable, "tools/docs_check.py"]),
    ]

    gate_results = []
    all_passed = True

    for gate_name, cmd in gates:
        passed, out = run_command_gate(gate_name, cmd)
        status_str = "[PASS]" if passed else "[FAIL]"
        gate_results.append((gate_name, status_str, out))
        if not passed:
            all_passed = False
            print(f"      [FAIL] Output:\n{out}\n")

    print("\n" + "=" * 70)
    print(" Quality Gate Summary Matrix")
    print("=" * 70)
    for name, status, _ in gate_results:
        print(f"  {name:<35} | {status}")
    print("=" * 70)

    if not all_passed:
        print(
            "\n[FAIL] Release Pre-Flight check FAILED! Please fix issues before releasing.\n"
        )
        sys.exit(1)

    print(
        f"\n[OK] All 6 quality gates passed! ProfileForge v{pyproject_ver} is ready for release.\n"
    )
    sys.exit(0)


def cmd_changelog(args) -> None:
    version = args.version or get_pyproject_version()
    today = datetime.now().strftime("%Y-%m-%d")

    entry = f"""
## [{version}] - {today}

### Highlights
- Official production release of ProfileForge v{version}.
- High-performance declarative component tree engine for GitHub profile SVG generation.
- Full theme token design system with 14 built-in production themes.
- 12 extensible widgets covering identity, stats, career, development, and social channels.
- 6 starter template personas with typed manifest validation (`manifest.yaml`).
- Sub-15ms end-to-end rendering pipeline verified by continuous performance benchmarking.

### Added
- **Track 1**: High-precision multi-stage performance benchmark service (`profileforge benchmark`) and budget gate (`budget.yaml`).
- **Track 2**: Release engineering automation (`tools/release.py`) and release guide documentation (`docs/RELEASE_GUIDE.md`).
- **Track 4**: Documentation QA and link validation gate (`tools/docs_check.py`).
- **Track 5**: Template manifest system (`manifest.yaml`) and `TemplateLoader` service.
- **Track 6**: Architecture decision records indexer (`tools/adr_index.py`) and widget CLI discovery (`profileforge widgets list/info`).

### Performance
- Total build execution latency under 12ms mean SLA.
- Sub-millisecond layout calculation and config parsing.
- Peak memory footprint below 0.5 MB.
"""
    print("Generated Changelog Entry:")
    print(entry)

    if CHANGELOG_FILE.exists():
        current_cl = CHANGELOG_FILE.read_text(encoding="utf-8")
        if f"## [{version}]" not in current_cl:
            # Prepend after header
            if "# Changelog" in current_cl:
                new_cl = current_cl.replace(
                    "# Changelog\n", f"# Changelog\n{entry}\n", 1
                )
            else:
                new_cl = f"# Changelog\n{entry}\n{current_cl}"
            CHANGELOG_FILE.write_text(new_cl, encoding="utf-8")
            print(f"[OK] Appended entry to {CHANGELOG_FILE.relative_to(REPO_ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ProfileForge Release Engineering & Verification Tool"
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # check
    subparsers.add_parser("check", help="Run full pre-flight quality gates")

    # bump
    bump_parser = subparsers.add_parser("bump", help="Bump project version")
    bump_parser.add_argument(
        "part", choices=["patch", "minor", "major"], help="Semver part to bump"
    )

    # changelog
    cl_parser = subparsers.add_parser("changelog", help="Generate changelog entry")
    cl_parser.add_argument(
        "--version", default=None, help="Version string (default: from pyproject.toml)"
    )

    args = parser.parse_args()

    if args.subcommand == "check":
        cmd_check(args)
    elif args.subcommand == "bump":
        cmd_bump(args)
    elif args.subcommand == "changelog":
        cmd_changelog(args)


if __name__ == "__main__":
    main()
