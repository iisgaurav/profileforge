#!/usr/bin/env python3
"""
Performance Budget Verification Tool for ProfileForge.

Runs multi-stage benchmark on target configuration, evaluates timings against
budget.yaml limits, and enforces performance SLAs.

Usage:
    python tools/performance_check.py [--budget budget.yaml] [--config examples/backend/profileforge.yaml]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# Ensure src/ is on sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from profileforge.services.benchmark import run_benchmark  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ProfileForge Performance Budget Verification"
    )
    parser.add_argument(
        "--budget",
        "-b",
        default="budget.yaml",
        help="Path to budget.yaml (default: budget.yaml)",
    )
    parser.add_argument(
        "--config",
        "-c",
        default="examples/backend/profileforge.yaml",
        help="Path to template config to benchmark (default: examples/backend/profileforge.yaml)",
    )
    parser.add_argument(
        "--iterations",
        "-n",
        type=int,
        default=20,
        help="Number of iterations for statistical precision (default: 20)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Path to write JSON benchmark report",
    )
    args = parser.parse_args()

    budget_path = Path(args.budget)
    config_path = Path(args.config)

    if not config_path.exists():
        # Fallback to local profileforge.yaml if example path doesn't exist
        if Path("profileforge.yaml").exists():
            config_path = Path("profileforge.yaml")
        else:
            print(f"[FAIL] Target config not found: {config_path}")
            sys.exit(1)

    if not budget_path.exists():
        print(f"[FAIL] Budget file not found: {budget_path}")
        sys.exit(1)

    with open(budget_path, "r", encoding="utf-8") as f:
        budget_data = yaml.safe_load(f) or {}

    budgets = budget_data.get("budgets", {})
    if not budgets:
        print(f"[FAIL] No 'budgets' dictionary found in {budget_path}")
        sys.exit(1)

    print("=" * 70)
    print(" ProfileForge Performance & SLA Gate")
    print(f" Target Config: {config_path}")
    print(f" Budget Spec:   {budget_path}")
    print(f" Iterations:    {args.iterations}")
    print("=" * 70)

    try:
        result = run_benchmark(config_path, iterations=args.iterations)
    except Exception as e:
        print(f"\n[FAIL] Benchmark execution failed: {e}")
        sys.exit(1)

    print("\nBenchmark Execution Results:")
    print(result.format_table())
    print()

    passed, evals = result.evaluate_budget(budgets)

    print("-" * 70)
    print(f"{'Stage':<20} | {'Actual (ms)':<12} | {'Budget (ms)':<12} | {'Status':<10}")
    print("-" * 70)

    for ev in evals:
        status_str = "[PASS]" if ev["passed"] else "[FAIL]"
        print(
            f"{ev['stage']:<20} | {ev['actual_ms']:>10.3f}ms | {ev['limit_ms']:>10.3f}ms | {status_str}"
        )
    print("-" * 70)

    if args.output:
        out_file = Path(args.output)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n[OK] Benchmark report exported -> {out_file}")

    if not passed:
        print(
            "\n[FAIL] Performance budget check FAILED! One or more stages exceeded threshold."
        )
        sys.exit(1)

    print(
        f"\n[OK] Performance budget check PASSED! All stages within SLA limits ({result.ops_sec:.1f} ops/sec).\n"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
