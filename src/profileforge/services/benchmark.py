from __future__ import annotations

import html
import statistics
import time
import tracemalloc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from profileforge.core.config import ConfigLoader
from profileforge.core.context import BuildContext, Services
from profileforge.core.registry import WIDGET_REGISTRY, ConnectorRegistry
from profileforge.render.layout import LayoutEngine
from profileforge.render.svg.renderer import SVGRenderer


class BenchmarkConnectorWrapper:
    """
    Wraps connectors with an in-memory cache to isolate pure CPU transformation,
    layout computation, and SVG rendering from remote network latency.
    """

    def __init__(self, target_connector: Any):
        self._target = target_connector
        self._cache: Dict[str, Any] = {}

    def fetch(self, request: Any) -> Any:
        key = getattr(request, "resource", str(request))
        if key not in self._cache:
            try:
                self._cache[key] = self._target.fetch(request)
            except Exception:
                self._cache[key] = {}
        return self._cache[key]

    def get_stats(self, username: str) -> Any:
        if "stats" not in self._cache:
            try:
                self._cache["stats"] = self._target.get_stats(username)
            except Exception:
                from profileforge.connectors.github.models import GitHubStats

                self._cache["stats"] = GitHubStats(stars=120, prs=45, commits=850)
        return self._cache["stats"]

    def get_repositories(self, username: str) -> Any:
        if "repos" not in self._cache:
            try:
                self._cache["repos"] = self._target.get_repositories(username)
            except Exception:
                from profileforge.connectors.github.models import (
                    GitHubRepository,
                )

                self._cache["repos"] = [
                    GitHubRepository(
                        name="fast-kv",
                        description="Distributed high-performance key-value store in Go",
                        primary_language="Go",
                        stars=342,
                        forks=45,
                    ),
                    GitHubRepository(
                        name="async-pipeline",
                        description="Event-driven streaming engine in Python",
                        primary_language="Python",
                        stars=189,
                        forks=23,
                    ),
                ]
        return self._cache["repos"]

    def get_languages(self, username: str) -> Any:
        if "langs" not in self._cache:
            try:
                self._cache["langs"] = self._target.get_languages(username)
            except Exception:
                from profileforge.connectors.github.models import (
                    GitHubLanguageStats,
                )

                self._cache["langs"] = [
                    GitHubLanguageStats(name="Python", bytes=45000),
                    GitHubLanguageStats(name="Go", bytes=35000),
                ]
        return self._cache["langs"]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._target, name)


@dataclass
class StageTiming:
    """Statistical summary of execution timings for an individual pipeline stage."""

    name: str
    mean_ms: float
    p95_ms: float
    min_ms: float
    max_ms: float
    samples: List[float] = field(default_factory=list, repr=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mean_ms": round(self.mean_ms, 3),
            "p95_ms": round(self.p95_ms, 3),
            "min_ms": round(self.min_ms, 3),
            "max_ms": round(self.max_ms, 3),
        }


@dataclass
class BenchmarkResult:
    """Comprehensive benchmark execution report."""

    target_config: str
    iterations: int
    stages: Dict[str, StageTiming]
    peak_memory_mb: float
    total_duration_sec: float
    ops_sec: float
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_config": self.target_config,
            "iterations": self.iterations,
            "timestamp": self.timestamp,
            "total_duration_sec": round(self.total_duration_sec, 4),
            "ops_sec": round(self.ops_sec, 2),
            "peak_memory_mb": round(self.peak_memory_mb, 4),
            "stages": {name: stage.to_dict() for name, stage in self.stages.items()},
        }

    def evaluate_budget(
        self, budget: Dict[str, float]
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Evaluates stage mean execution times against budget thresholds.
        Returns (passed, list_of_evaluations).
        """
        evaluations = []
        all_passed = True

        for stage_name, limit_ms in budget.items():
            if stage_name in self.stages:
                actual_ms = self.stages[stage_name].mean_ms
                passed = actual_ms <= limit_ms
                if not passed:
                    all_passed = False
                evaluations.append(
                    {
                        "stage": stage_name,
                        "limit_ms": limit_ms,
                        "actual_ms": actual_ms,
                        "passed": passed,
                        "delta_ms": round(actual_ms - limit_ms, 3),
                    }
                )

        return all_passed, evaluations

    def format_table(self) -> str:
        """Formats the benchmark results into a clean CLI table."""
        lines = []
        header = f"{'Stage':<20} | {'Mean (ms)':<10} | {'p95 (ms)':<10} | {'Min (ms)':<10} | {'Max (ms)':<10}"
        lines.append("-" * len(header))
        lines.append(header)
        lines.append("-" * len(header))

        for name, stage in self.stages.items():
            lines.append(
                f"{name:<20} | {stage.mean_ms:>10.3f} | {stage.p95_ms:>10.3f} | {stage.min_ms:>10.3f} | {stage.max_ms:>10.3f}"
            )

        lines.append("-" * len(header))
        lines.append(
            f"Throughput: {self.ops_sec:.1f} ops/sec  |  Peak Memory: {self.peak_memory_mb:.2f} MB  |  Iterations: {self.iterations}"
        )
        return "\n".join(lines)


def _compute_stage_timing(name: str, samples: List[float]) -> StageTiming:
    if not samples:
        return StageTiming(name=name, mean_ms=0.0, p95_ms=0.0, min_ms=0.0, max_ms=0.0)
    sorted_samples = sorted(samples)
    p95_idx = int(len(sorted_samples) * 0.95)
    p95_val = sorted_samples[min(p95_idx, len(sorted_samples) - 1)]
    return StageTiming(
        name=name,
        mean_ms=statistics.mean(samples),
        p95_ms=p95_val,
        min_ms=min(samples),
        max_ms=max(samples),
        samples=samples,
    )


def run_benchmark(
    config_path: str | Path, iterations: int = 10, warmup: int = 2
) -> BenchmarkResult:
    """
    Executes a high-precision multi-stage performance benchmark across ProfileForge pipeline layers.

    Stages measured:
    - theme_load: Loading and resolving theme tokens
    - config_parse: Reading and parsing profileforge.yaml
    - connector_fetch: Resolving connectors and fetching context data
    - widget_build: Constructing Component tree for all widgets
    - layout_pass: Running LayoutEngine flexbox calculation
    - render_pass: SVGRenderer component rendering
    - svg_output: Full SVG markup generation with defs & metadata
    - total_build: Complete end-to-end build cycle
    """
    config_file = Path(config_path).resolve()
    if not config_file.exists():
        raise FileNotFoundError(f"Benchmark config not found: {config_file}")

    # Shared cache across iterations to simulate warm engine benchmark
    shared_connector_cache: Dict[str, Any] = {}

    # Warmup runs to stabilize JIT/cache/imports
    for _ in range(warmup):
        _run_single_pass(config_file, shared_cache=shared_connector_cache)

    timings: Dict[str, List[float]] = {
        "config_parse": [],
        "theme_load": [],
        "connector_fetch": [],
        "widget_build": [],
        "layout_pass": [],
        "render_pass": [],
        "svg_output": [],
        "total_build": [],
    }

    tracemalloc.start()
    start_total_wall = time.perf_counter()

    for _ in range(iterations):
        pass_timings = _run_single_pass(
            config_file, shared_cache=shared_connector_cache
        )
        for stage, duration_ms in pass_timings.items():
            timings[stage].append(duration_ms)

    total_wall_sec = time.perf_counter() - start_total_wall
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_memory_mb = peak_bytes / (1024 * 1024)
    ops_sec = iterations / total_wall_sec if total_wall_sec > 0 else 0.0

    stages = {
        name: _compute_stage_timing(name, samples) for name, samples in timings.items()
    }

    return BenchmarkResult(
        target_config=str(config_file),
        iterations=iterations,
        stages=stages,
        peak_memory_mb=peak_memory_mb,
        total_duration_sec=total_wall_sec,
        ops_sec=ops_sec,
    )


def _run_single_pass(
    config_path: Path, shared_cache: Optional[Dict[str, Any]] = None
) -> Dict[str, float]:
    """Runs a single instrumented build pass, returning elapsed milliseconds per stage."""
    pass_timings: Dict[str, float] = {}
    pass_start = time.perf_counter()

    # 1. config_parse
    t0 = time.perf_counter()
    config = ConfigLoader.load_main_config(str(config_path))
    pass_timings["config_parse"] = (time.perf_counter() - t0) * 1000

    # 2. theme_load
    t0 = time.perf_counter()
    theme_dir = config_path.parent / "themes"
    theme = ConfigLoader.load_theme(config.active_theme, themes_dir=str(theme_dir))
    pass_timings["theme_load"] = (time.perf_counter() - t0) * 1000

    # 3. connector_fetch
    t0 = time.perf_counter()
    connectors = {}
    for name, ds_config in config.connectors_config.items():
        if name in ConnectorRegistry:
            cfg_copy = dict(ds_config)
            if "root" in cfg_copy:
                cfg_copy["root"] = str(config_path.parent / cfg_copy["root"])
            raw_connector = ConnectorRegistry[name](cfg_copy)
            wrapped = BenchmarkConnectorWrapper(raw_connector)
            if shared_cache is not None:
                wrapped._cache = shared_cache
            connectors[name] = wrapped

    services = Services(connectors=connectors)
    context = BuildContext(theme=theme, config=config, services=services)
    pass_timings["connector_fetch"] = (time.perf_counter() - t0) * 1000

    svg_renderer = SVGRenderer(context.get_render_context())
    defs_block = svg_renderer.get_defs()

    widget_build_ms = 0.0
    layout_pass_ms = 0.0
    render_pass_ms = 0.0
    svg_output_ms = 0.0

    # Instantiate and process each widget
    active_widgets = [w for w in config.widgets if w.name in WIDGET_REGISTRY]
    for w_config in active_widgets:
        widget = WIDGET_REGISTRY[w_config.name]()

        # Widget build
        tb0 = time.perf_counter()
        component_tree = widget.render_safe(context)
        widget_build_ms += (time.perf_counter() - tb0) * 1000

        # Layout pass
        tl0 = time.perf_counter()
        render_node = LayoutEngine.calculate(component_tree)
        layout_pass_ms += (time.perf_counter() - tl0) * 1000

        # Render pass
        tr0 = time.perf_counter()
        inner_svg = svg_renderer.render(render_node)
        render_pass_ms += (time.perf_counter() - tr0) * 1000

        # SVG Output formatting
        to0 = time.perf_counter()
        total_w = render_node.width
        total_h = render_node.height
        escaped_title = html.escape(w_config.name.title())
        _ = (
            f'<svg width="{total_w}" height="{total_h}" '
            f'viewBox="0 0 {total_w} {total_h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f"  <title>{escaped_title} Widget</title>\n"
            f"  <desc>ProfileForge {escaped_title} widget</desc>\n"
            f"  {defs_block}\n"
            f"  {inner_svg}\n"
            f"</svg>"
        )
        svg_output_ms += (time.perf_counter() - to0) * 1000

    pass_timings["widget_build"] = widget_build_ms
    pass_timings["layout_pass"] = layout_pass_ms
    pass_timings["render_pass"] = render_pass_ms
    pass_timings["svg_output"] = svg_output_ms
    pass_timings["total_build"] = (time.perf_counter() - pass_start) * 1000

    return pass_timings
