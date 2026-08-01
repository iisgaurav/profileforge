"""
Integration tests verifying that all starter examples and gallery pipeline build cleanly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pytest

from profileforge.core.config import ConfigLoader
from profileforge.core.context import BuildContext, Services
from profileforge.core.registry import WIDGET_REGISTRY, ConnectorRegistry
from profileforge.render.layout import LayoutEngine
from profileforge.render.svg.renderer import SVGRenderer
from profileforge.services.gallery import GalleryExporter, export_gallery

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"


def get_all_example_dirs() -> List[Path]:
    """Returns all example directories that contain a profileforge.yaml config."""
    if not EXAMPLES_DIR.exists():
        return []
    return [
        d
        for d in sorted(EXAMPLES_DIR.iterdir())
        if d.is_dir() and (d / "profileforge.yaml").exists()
    ]


REQUIRED_EXAMPLES = [
    "backend",
    "frontend",
    "minimal",
    "student",
    "opensource",
    "ai-engineer",
]


def test_required_examples_exist():
    """Verify that all 6 required starter template examples exist."""
    example_names = [d.name for d in get_all_example_dirs()]
    for req in REQUIRED_EXAMPLES:
        assert req in example_names, (
            f"Missing required example '{req}' in examples/ directory."
        )


@pytest.mark.parametrize(
    "example_name",
    REQUIRED_EXAMPLES,
)
def test_example_builds_and_generates_valid_svgs(example_name: str, tmp_path: Path):
    """
    Validates that each example's profileforge.yaml loads, all connectors and widgets resolve,
    and valid SVG documents are generated for each configured widget.
    """
    example_dir = EXAMPLES_DIR / example_name
    config_file = example_dir / "profileforge.yaml"
    assert config_file.exists(), f"Missing config file in {example_dir}"

    config = ConfigLoader.load_main_config(str(config_file))
    assert config.project_name, "Project name must not be empty"
    assert len(config.widgets) > 0, "Example must define at least one widget"

    theme_dir = example_dir / "themes"
    theme = ConfigLoader.load_theme(config.active_theme, themes_dir=str(theme_dir))
    assert theme.name, "Theme must resolve cleanly"

    # Set up connectors
    connectors = {}
    for name, ds_config in config.connectors_config.items():
        if name in ConnectorRegistry:
            c_cfg = dict(ds_config)
            if "root" in c_cfg:
                c_cfg["root"] = str(example_dir / c_cfg["root"])
            connectors[name] = ConnectorRegistry[name](c_cfg)

    services = Services(connectors=connectors)
    context = BuildContext(theme=theme, config=config, services=services)
    svg_renderer = SVGRenderer(context)

    out_dir = tmp_path / f"output_{example_name}"
    out_dir.mkdir(parents=True, exist_ok=True)

    defs_block = svg_renderer.get_defs()
    generated_files = []

    for w_config in config.widgets:
        assert w_config.name in WIDGET_REGISTRY, (
            f"Widget '{w_config.name}' not in registry"
        )
        widget = WIDGET_REGISTRY[w_config.name]()
        component_tree = widget.render_safe(context)
        LayoutEngine.calculate(component_tree)

        inner_svg = svg_renderer.render(component_tree)
        total_w = component_tree.computed_width
        total_h = component_tree.computed_height

        assert total_w > 0, f"Widget '{w_config.name}' width must be > 0"
        assert total_h > 0, f"Widget '{w_config.name}' height must be > 0"

        svg_content = (
            f'<svg width="{total_w}" height="{total_h}" '
            f'viewBox="0 0 {total_w} {total_h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f"  {defs_block}\n"
            f"  {inner_svg}\n"
            f"</svg>"
        )

        out_file = out_dir / f"{w_config.name}.svg"
        out_file.write_text(svg_content, encoding="utf-8")
        generated_files.append(out_file)

    # Verify generated SVGs
    assert len(generated_files) == len(config.widgets)
    for f in generated_files:
        assert f.exists()
        content = f.read_text(encoding="utf-8")
        assert content.startswith("<svg") or "<?xml" in content or "<!--" in content
        assert "</svg>" in content


def test_gallery_export_pipeline(tmp_path: Path):
    """
    Tests the gallery export pipeline, verifying JSON metadata and SVG asset outputs.
    """
    gallery_out = tmp_path / "gallery"
    result = export_gallery(
        out_dir=str(gallery_out),
        top_themes=["github-dark", "vercel", "apple", "dracula", "modern"],
    )
    assert result["rendered_assets_count"] > 0
    assert result["themes_count"] >= 10
    assert result["widgets_count"] == len(WIDGET_REGISTRY)

    assert gallery_out.exists()
    assert (gallery_out / "themes.json").exists()
    assert (gallery_out / "widgets.json").exists()
    assert (gallery_out / "templates.json").exists()
    assert (gallery_out / "gallery.json").exists()
    assert (gallery_out / "assets").exists()

    # 1. Verify themes.json
    with open(gallery_out / "themes.json", "r", encoding="utf-8") as f:
        themes = json.load(f)
    assert isinstance(themes, list)
    assert len(themes) >= 10
    first_theme = themes[0]
    for key in [
        "id",
        "name",
        "mode",
        "tags",
        "author",
        "version",
        "license",
        "description",
        "colors",
        "typography",
        "preview_url",
    ]:
        assert key in first_theme, f"Missing key '{key}' in theme metadata"

    # 2. Verify widgets.json
    with open(gallery_out / "widgets.json", "r", encoding="utf-8") as f:
        widgets = json.load(f)
    assert isinstance(widgets, list)
    assert len(widgets) == len(WIDGET_REGISTRY)
    first_widget = widgets[0]
    for key in [
        "id",
        "name",
        "category",
        "description",
        "version",
        "author",
        "tags",
        "required_connectors",
    ]:
        assert key in first_widget, f"Missing key '{key}' in widget metadata"

    # 3. Verify templates.json
    with open(gallery_out / "templates.json", "r", encoding="utf-8") as f:
        templates = json.load(f)
    assert isinstance(templates, list)
    assert len(templates) == 9
    first_template = templates[0]
    for key in ["id", "name", "description", "active_theme", "widgets", "file_list"]:
        assert key in first_template, f"Missing key '{key}' in template metadata"

    # 4. Verify gallery.json
    with open(gallery_out / "gallery.json", "r", encoding="utf-8") as f:
        gallery_index = json.load(f)
    assert "version" in gallery_index
    assert "themes" in gallery_index
    assert "widgets" in gallery_index
    assert "templates" in gallery_index
    assert len(gallery_index["widgets"]) == len(widgets)

    # 5. Verify assets directory contains rendered SVGs
    assets = list((gallery_out / "assets").glob("*.svg"))
    assert len(assets) > 30
    for asset in assets:
        content = asset.read_text(encoding="utf-8")
        assert "<svg" in content
        assert "</svg>" in content


def test_gallery_exporter_class():
    """Unit tests on GalleryExporter helper methods."""
    exporter = GalleryExporter()
    theme_ids = exporter.get_all_theme_ids()
    assert "github-dark" in theme_ids
    assert "vercel" in theme_ids
    assert "apple" in theme_ids

    widgets_meta = exporter.extract_widgets_metadata()
    assert len(widgets_meta) == 15

    templates_meta = exporter.extract_templates_metadata()
    assert len(templates_meta) == 9
