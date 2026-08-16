import json
import os
import subprocess
import time


def run_benchmark():
    print("[*] Running ProfileForge Performance Baseline...")

    start_time = time.time()

    # Run a full gallery export to measure SVG rendering times
    result = subprocess.run(
        ["profileforge", "gallery", "export", "--out-dir", "artifacts/benchmark"],
        capture_output=True,
        text=True,
    )

    end_time = time.time()

    if result.returncode != 0:
        print(f"[!] Benchmark failed:\n{result.stderr}")
        return

    duration = end_time - start_time

    assets_dir = "artifacts/benchmark/assets"
    svg_count = (
        len([f for f in os.listdir(assets_dir) if f.endswith(".svg")])
        if os.path.exists(assets_dir)
        else 0
    )

    metrics = {
        "build_time_seconds": round(duration, 3),
        "svg_count": svg_count,
        "avg_render_time_ms": round((duration / svg_count * 1000), 2)
        if svg_count > 0
        else 0,
    }

    print("\n--- Performance Baseline ---")
    print(f"Total Build Time:   {metrics['build_time_seconds']}s")
    print(f"SVGs Generated:     {metrics['svg_count']}")
    print(f"Avg Render Time:    {metrics['avg_render_time_ms']}ms / widget")

    # Save as baseline
    os.makedirs("artifacts/reports", exist_ok=True)
    with open("artifacts/reports/benchmark_baseline.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\n[OK] Baseline saved to artifacts/reports/benchmark_baseline.json")


if __name__ == "__main__":
    run_benchmark()
