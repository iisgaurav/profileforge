"""
Unit and integration tests for ProfileForge v1.0.0 Launch Engineering services and tools.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

from profileforge.services.benchmark import (
    BenchmarkConnectorWrapper,
    BenchmarkResult,
    StageTiming,
    run_benchmark,
)
from profileforge.templates.loader import TemplateLoader
from tools.adr_index import (
    ADRMetadata,
    generate_index_markdown,
    validate_adrs,
)
from tools.docs_check import (
    validate_cli_references,
    validate_markdown_links,
    validate_yaml_blocks,
)
from tools.release import bump_version_string, get_init_version, get_pyproject_version

REPO_ROOT = Path(__file__).parent.parent


def test_benchmark_service_execution():
    backend_config = REPO_ROOT / "examples" / "backend" / "profileforge.yaml"
    result = run_benchmark(backend_config, iterations=3, warmup=1)

    assert isinstance(result, BenchmarkResult)
    assert result.iterations == 3
    assert result.total_duration_sec > 0
    assert result.ops_sec > 0
    assert result.peak_memory_mb > 0

    # Required pipeline stages
    expected_stages = [
        "config_parse",
        "theme_load",
        "connector_fetch",
        "widget_build",
        "layout_pass",
        "render_pass",
        "svg_output",
        "total_build",
    ]
    for stage in expected_stages:
        assert stage in result.stages
        timing = result.stages[stage]
        assert isinstance(timing, StageTiming)
        assert timing.mean_ms >= 0

    table = result.format_table()
    assert "Throughput:" in table
    assert "Stage" in table

    # Budget evaluation
    budget = {"total_build": 500.0, "widget_build": 50.0}
    passed, evals = result.evaluate_budget(budget)
    assert passed is True
    assert len(evals) == 2


def test_benchmark_connector_wrapper():
    class DummyTarget:
        def fetch(self, req):
            return {"fetched": True}

    wrapper = BenchmarkConnectorWrapper(DummyTarget())
    # Test fetch caching
    assert wrapper.fetch("test_res") == {"fetched": True}
    assert wrapper.fetch("test_res") == {"fetched": True}

    # Test stats & repos fallbacks
    stats = wrapper.get_stats("octocat")
    assert stats.commits > 0
    repos = wrapper.get_repositories("octocat")
    assert len(repos) > 0
    langs = wrapper.get_languages("octocat")
    assert len(langs) > 0
    assert langs[0].name == "Python"


def test_template_loader_manifests():
    template_ids = TemplateLoader.list_templates()
    assert len(template_ids) == 9

    for tid in template_ids:
        manifest = TemplateLoader.load_manifest(tid)
        assert manifest.schema == 1
        assert manifest.id == tid
        assert manifest.name
        assert manifest.description
        assert len(manifest.widgets) > 0
        assert len(manifest.themes) > 0


def test_template_loader_scaffold(tmp_path: Path):
    target = tmp_path / "new_profile"
    scaffolded_path = TemplateLoader.scaffold(
        "backend", target, project_name="Custom Architect"
    )
    assert scaffolded_path.exists()
    assert (scaffolded_path / "profileforge.yaml").exists()
    assert (scaffolded_path / "manifest.yaml").exists()

    content = (scaffolded_path / "profileforge.yaml").read_text(encoding="utf-8")
    assert "Custom Architect" in content


def test_adr_index_validation():
    adr1 = ADRMetadata(
        number=1,
        id_str="ADR-001",
        title="Component Tree",
        status="Accepted",
        date="2026-08-02",
        filename="ADR-001-component-tree.md",
        filepath=REPO_ROOT / "docs" / "adr" / "ADR-001-declarative-component-tree.md",
    )
    errors = validate_adrs([adr1])
    assert len(errors) == 0

    md = generate_index_markdown([adr1])
    assert (
        "| [ADR-001](ADR-001-component-tree.md) | Component Tree | Accepted | 2026-08-02 |"
        in md
    )


def test_docs_check_helpers(tmp_path: Path):
    test_md = tmp_path / "test.md"
    content = """
# Test Doc
```yaml
key: value
nested:
  number: 42
```
[Valid Link](test.md)
`profileforge build`
"""
    test_md.write_text(content, encoding="utf-8")

    yaml_errs = validate_yaml_blocks(test_md, content)
    assert len(yaml_errs) == 0

    link_errs = validate_markdown_links(test_md, content)
    assert len(link_errs) == 0

    cli_errs = validate_cli_references(test_md, content)
    assert len(cli_errs) == 0


def test_release_semver_bump():
    assert bump_version_string("1.0.0", "patch") == "1.0.1"
    assert bump_version_string("1.0.0", "minor") == "1.1.0"
    assert bump_version_string("1.0.0", "major") == "2.0.0"

    pyproject_ver = get_pyproject_version()
    init_ver = get_init_version()
    assert pyproject_ver == init_ver == "1.0.0"


def test_cli_benchmark_and_widgets_dispatch():
    from profileforge.cli.main import main

    with patch.object(
        sys,
        "argv",
        [
            "profileforge",
            "widgets",
            "info",
            "github_stats",
        ],
    ):
        main()

    with patch.object(
        sys,
        "argv",
        [
            "profileforge",
            "widgets",
            "list",
        ],
    ):
        main()
