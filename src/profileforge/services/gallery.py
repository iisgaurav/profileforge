"""
ProfileForge Gallery & Ecosystem Pipeline Service.

Extracts full metadata for all registered themes, widgets, and templates,
and renders standalone SVG assets across multiple themes.
"""

from __future__ import annotations

import html as html_mod
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from profileforge.connectors.base import Connector
from profileforge.connectors.github.models import (
    GitHubLanguageStats,
    GitHubRepository,
    GitHubStats,
)
from profileforge.core.config import ConfigLoader
from profileforge.core.context import BuildContext, Services
from profileforge.core.models import (
    DashboardConfig,
    MetricsConfig,
    Outputs,
    ProfileForgeConfig,
    Theme,
    WidgetConfig,
)
from profileforge.core.registry import WIDGET_REGISTRY
from profileforge.render.layout import LayoutEngine
from profileforge.render.svg.renderer import SVGRenderer
from profileforge.templates import (
    TEMPLATES_DIR,
    get_template_info,
    list_builtin_templates,
)

TOP_THEMES: List[str] = [
    "github-dark",
    "vercel",
    "apple",
    "dracula",
    "nord",
    "modern",
    "minimal",
    "catppuccin-mocha",
]

SAMPLE_REPOSITORIES = [
    GitHubRepository(
        name="profileforge",
        stars=1420,
        primary_language="Python",
        description="Declarative, extensible developer profile card & SVG generation engine.",
        forks=184,
        languages=[
            GitHubLanguageStats(name="Python", bytes=85000),
            GitHubLanguageStats(name="HTML", bytes=12000),
        ],
    ),
    GitHubRepository(
        name="async-data-pipeline",
        stars=830,
        primary_language="Rust",
        description="High-throughput asynchronous event streamer with zero-copy deserialization.",
        forks=95,
        languages=[
            GitHubLanguageStats(name="Rust", bytes=65000),
        ],
    ),
    GitHubRepository(
        name="reactive-design-tokens",
        stars=612,
        primary_language="TypeScript",
        description="Dynamic design token management and SVG theming primitives for modern web apps.",
        forks=52,
        languages=[
            GitHubLanguageStats(name="TypeScript", bytes=45000),
        ],
    ),
    GitHubRepository(
        name="cloud-operator-kit",
        stars=425,
        primary_language="Go",
        description="Kubernetes custom controller framework with automated lifecycle reconciliation.",
        forks=38,
        languages=[
            GitHubLanguageStats(name="Go", bytes=35000),
        ],
    ),
]

SAMPLE_LOCAL_DATA = {
    "about.yaml": {
        "name": "Gaurav Verma",
        "role": "Principal Systems Architect",
        "tagline": "Building resilient distributed systems and open-source developer tooling.",
        "status": "Available for opportunities",
        "location": "Mumbai, India",
    },
    "hero.yaml": {
        "name": "Gaurav Verma",
        "role": "Principal Systems Architect",
        "tagline": "Building resilient distributed systems and open-source developer tooling.",
        "status": "Available for opportunities",
        "location": "Mumbai, India",
    },
    "skills.yaml": {
        "Languages": ["Python", "TypeScript", "Rust", "Go", "C++", "SQL"],
        "Frameworks & Libraries": [
            "FastAPI",
            "React",
            "Next.js",
            "Django",
            "Node.js",
        ],
        "Cloud & DevOps": [
            "Docker",
            "Kubernetes",
            "AWS",
            "GitHub Actions",
            "Terraform",
        ],
        "Databases": ["PostgreSQL", "Redis", "MongoDB", "ClickHouse"],
        "Tools & Architecture": [
            "Git",
            "Linux",
            "GraphQL",
            "REST APIs",
            "Neovim",
        ],
    },
    "experience.yaml": [
        {
            "role": "Staff Software Engineer",
            "company": "CloudScale Infrastructure",
            "period": "2023 — Present",
            "description": "Leading architecture for distributed telemetry and real-time event ingestion pipelines.",
            "highlights": [
                "Scaled high-throughput stream processing to 1M+ req/sec.",
                "Mentored team of 12 engineers across systems engineering.",
            ],
        },
        {
            "role": "Senior Full-Stack Engineer",
            "company": "Nexus Technologies",
            "period": "2020 — 2023",
            "description": "Architected modern web micro-frontends and robust asynchronous Python backends.",
            "highlights": [
                "Reduced end-to-end latency by 45% using efficient caching.",
                "Created automated CI/CD pipeline reducing deployment time.",
            ],
        },
    ],
    "expertise.yaml": {
        "skills": {
            "Backend Systems": ["FastAPI", "gRPC", "Kafka", "PostgreSQL", "Redis"],
            "Cloud & DevOps": ["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD"],
            "Languages": ["Python", "Rust", "Go", "TypeScript"],
        }
    },
    "focus.yaml": {
        "building": [
            {
                "name": "ProfileForge — Developer Profile Engine",
                "progress": 85,
            },
            {
                "name": "Async Telemetry Streamer",
                "progress": 60,
            },
        ],
        "learning": [
            {
                "name": "Rust Systems Programming & WASM",
                "progress": 75,
            }
        ],
    },
    "now.yaml": {
        "building": "ProfileForge — Declarative GitHub profile engine with responsive SVG themes",
        "learning": "Rust systems programming, WebAssembly & high-concurrency architectures",
        "reading": "Designing Data-Intensive Applications by Martin Kleppmann",
        "focus": "Developer tooling, open-source maintainability, and declarative UI design",
        "location": "Mumbai, India",
        "updated": "August 2026",
    },
    "roadmap.yaml": [
        {
            "skill": "Distributed Stream Processing Engine",
            "progress": 90,
        },
        {
            "skill": "Custom JIT Compiler in Rust",
            "progress": 65,
        },
        {
            "skill": "Vector Database Indexing Primitives",
            "progress": 40,
        },
    ],
    "social.yaml": {
        "github": "iisgaurav",
        "twitter": "iisgaurav",
        "linkedin": "iisgaurav",
        "website": "https://iisgaurav.vercel.app",
        "instagram": "iisgaurav",
        "email": "gauravv2504@gmail.com",
    },
    "activity_timeline.yaml": [
        {
            "title": "Merged PR #142: High-throughput stream engine",
            "type": "PR Merge",
            "repo": "profileforge/core",
            "date": "2 hours ago",
            "description": "Implemented zero-copy serialization for SVG component tree layout calculation.",
        },
        {
            "title": "Tagged Release v1.0.0 (Production Launch)",
            "type": "Release",
            "repo": "profileforge/profileforge",
            "date": "Yesterday",
            "description": "Official launch of ProfileForge Studio, interactive web builder, and widget catalog.",
        },
        {
            "title": "Pushed 8 commits to main",
            "type": "Commit",
            "repo": "distributed-systems/telemetry",
            "date": "3 days ago",
            "description": "Optimized memory layout and reduced garbage collection pause times by 35%.",
        },
    ],
}


class MockGalleryLocalConnector(Connector):
    def fetch(self, request: Any) -> Any:
        resource = getattr(request, "resource", "") or str(request)
        if resource in SAMPLE_LOCAL_DATA:
            return SAMPLE_LOCAL_DATA[resource]
        stem = Path(resource).name
        if stem in SAMPLE_LOCAL_DATA:
            return SAMPLE_LOCAL_DATA[stem]
        return {}


class MockGalleryGithubConnector(Connector):
    def fetch(self, request: Any) -> Any:
        return None

    def get_stats(self, username: str) -> GitHubStats:
        return GitHubStats(stars=2480, prs=385, commits=3120)

    def get_repositories(self, username: str) -> list[GitHubRepository]:
        return SAMPLE_REPOSITORIES


class GalleryExporter:
    """
    Exports full ecosystem gallery metadata and renders SVG assets across themes.
    """

    def __init__(
        self,
        themes_dir: Optional[Path] = None,
        out_dir: Optional[Path] = None,
        top_themes: Optional[List[str]] = None,
    ):
        self.themes_dir = themes_dir or Path(__file__).parent.parent / "themes"
        self.out_dir = Path(out_dir or "gallery")
        self.top_themes = top_themes or TOP_THEMES

    def get_all_theme_ids(self) -> List[str]:
        """Discovers all available theme IDs from built-in and custom theme directories."""
        theme_ids: set[str] = set()
        if self.themes_dir.exists():
            for f in self.themes_dir.glob("*.yaml"):
                theme_ids.add(f.stem)

        builtin_dir = Path(__file__).parent.parent / "themes"
        if builtin_dir.exists() and builtin_dir != self.themes_dir:
            for f in builtin_dir.glob("*.yaml"):
                theme_ids.add(f.stem)

        return sorted(list(theme_ids))

    def extract_themes_metadata(self) -> List[Dict[str, Any]]:
        """
        Extracts theme metadata for all themes matching the required schema:
        id, name, mode, tags, author, version, license, description, extends, colors, typography, preview_url.
        """
        theme_ids = self.get_all_theme_ids()
        themes_meta: List[Dict[str, Any]] = []

        for theme_id in theme_ids:
            try:
                theme = ConfigLoader.load_theme(
                    theme_id, themes_dir=str(self.themes_dir)
                )
                colors_dict = asdict(theme.colors)
                typography_dict = asdict(theme.typography)

                showcase_widget = (
                    "github_stats" if "github_stats" in WIDGET_REGISTRY else "about"
                )
                theme_obj = {
                    "id": theme.id or theme_id,
                    "name": theme.name,
                    "mode": theme.mode,
                    "tags": theme.tags or ["theme"],
                    "author": theme.author or "ProfileForge Team",
                    "version": theme.version or "1.0.0",
                    "license": theme.license or "MIT",
                    "description": theme.description
                    or f"Official {theme.name} theme for ProfileForge.",
                    "extends": theme.extends,
                    "colors": colors_dict,
                    "typography": typography_dict,
                    "preview_url": f"assets/{showcase_widget}_{theme_id}.svg",
                }
                themes_meta.append(theme_obj)
            except Exception:
                continue

        return themes_meta

    def extract_widgets_metadata(self) -> List[Dict[str, Any]]:
        """
        Extracts widget metadata for all registered widgets:
        id, name, category, description, version, author, tags, required_connectors, experimental, deprecated.
        """
        widgets_meta: List[Dict[str, Any]] = []

        for widget_id in sorted(WIDGET_REGISTRY.keys()):
            widget_cls = WIDGET_REGISTRY[widget_id]
            try:
                widget = widget_cls()
                meta = widget.metadata()
                widgets_meta.append(
                    {
                        "id": meta.id,
                        "name": meta.name,
                        "category": meta.category,
                        "description": meta.description,
                        "version": meta.version,
                        "author": meta.author or "ProfileForge Team",
                        "tags": meta.tags,
                        "required_connectors": meta.required_connectors,
                        "experimental": meta.experimental,
                        "deprecated": meta.deprecated,
                    }
                )
            except Exception:
                continue

        return widgets_meta

    def extract_templates_metadata(self) -> List[Dict[str, Any]]:
        """
        Extracts template metadata for all starter templates:
        id, name, description, active_theme, widgets, file_list.
        """
        template_ids = list_builtin_templates()
        templates_meta: List[Dict[str, Any]] = []

        for t_id in template_ids:
            info = get_template_info(t_id) or {}
            template_path = TEMPLATES_DIR / t_id

            file_list: List[str] = []
            if template_path.exists():
                for p in sorted(template_path.rglob("*")):
                    if p.is_file() and not p.name.startswith("."):
                        rel_path = p.relative_to(template_path).as_posix()
                        file_list.append(rel_path)

            if not file_list:
                file_list = [
                    "profileforge.yaml",
                    "README.md",
                    f"config/{info.get('widgets', ['hero'])[0]}.yaml",
                ]

            active_theme = (
                info.get("default_theme") or info.get("active_theme") or "github-dark"
            )

            templates_meta.append(
                {
                    "id": t_id,
                    "name": info.get("name", t_id.replace("-", " ").title()),
                    "description": info.get("description", ""),
                    "active_theme": active_theme,
                    "widgets": info.get("widgets", []),
                    "file_list": file_list,
                }
            )

        return templates_meta

    def render_widget_svg(
        self, widget_name: str, theme: Theme, config: ProfileForgeConfig
    ) -> str:
        """Renders a standalone SVG document for a given widget and theme."""
        services = Services(
            connectors={
                "local": MockGalleryLocalConnector({}),
                "github": MockGalleryGithubConnector({}),
            }
        )

        # Ensure widget config is set
        config.widgets = [WidgetConfig(name=widget_name)]
        config.active_theme = theme.name

        context = BuildContext(theme=theme, config=config, services=services)
        svg_renderer = SVGRenderer(context.get_render_context())

        widget_cls = WIDGET_REGISTRY[widget_name]
        widget = widget_cls()
        component_tree = widget.render_safe(context)
        render_node = LayoutEngine.calculate(component_tree)

        inner_svg = svg_renderer._render_node(render_node, [0])
        defs_block = svg_renderer.get_defs()
        total_w = render_node.width
        total_h = render_node.height
        escaped_title = html_mod.escape(f"{widget_name} - {theme.name}")

        svg_content = (
            f'<svg width="{total_w}" height="{total_h}" '
            f'viewBox="0 0 {total_w} {total_h}" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'role="img">\n'
            f"  <title>{escaped_title}</title>\n"
            f"  <desc>ProfileForge widget preview</desc>\n"
            f"{defs_block}\n"
            f"{inner_svg}\n"
            f"</svg>"
        )
        return svg_content

    def export(self) -> Dict[str, Any]:
        """
        Executes the full gallery export pipeline:
        - Creates gallery/assets directory
        - Writes gallery/themes.json
        - Writes gallery/widgets.json
        - Writes gallery/templates.json
        - Renders widget SVGs across top themes into gallery/assets/
        - Renders theme showcase SVGs into gallery/assets/
        - Writes gallery/gallery.json linking all assets
        """
        self.out_dir.mkdir(parents=True, exist_ok=True)
        assets_dir = self.out_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        themes_meta = self.extract_themes_metadata()
        widgets_meta = self.extract_widgets_metadata()
        templates_meta = self.extract_templates_metadata()

        # Base config for context
        base_config = ProfileForgeConfig(
            version=1,
            project_name="Gaurav Verma",
            project_title="Principal Systems Architect",
            active_theme="github-dark",
            widgets=[],
            connectors_config={},
            outputs=Outputs(),
            dashboard=DashboardConfig(),
            metrics=MetricsConfig(),
        )

        # Determine themes to render
        available_theme_ids = set(self.get_all_theme_ids())
        render_themes = sorted(list(available_theme_ids))

        loaded_themes: Dict[str, Theme] = {}
        for t_id in self.get_all_theme_ids():
            try:
                loaded_themes[t_id] = ConfigLoader.load_theme(
                    t_id, themes_dir=str(self.themes_dir)
                )
            except Exception:
                pass

        rendered_assets_count = 0
        widget_renders_map: Dict[str, Dict[str, str]] = {}

        # 1. Render all widgets across top themes
        for w_meta in widgets_meta:
            w_id = w_meta["id"]
            widget_renders_map[w_id] = {}
            for t_id in render_themes:
                if t_id not in loaded_themes:
                    continue
                theme = loaded_themes[t_id]
                svg_str = self.render_widget_svg(w_id, theme, base_config)
                out_filename = f"{w_id}_{t_id}.svg"
                out_path = assets_dir / out_filename
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(svg_str)
                widget_renders_map[w_id][t_id] = f"assets/{out_filename}"
                rendered_assets_count += 1

        # 2. Render theme preview SVGs (Skipped to avoid duplicating widget rendering)
        # The preview URL now simply points to the standard showcase widget generated above.

        # 3. Write themes.json
        themes_file = self.out_dir / "themes.json"
        with open(themes_file, "w", encoding="utf-8") as f:
            json.dump(themes_meta, f, indent=2)
            f.write("\n")

        # 4. Write widgets.json
        widgets_file = self.out_dir / "widgets.json"
        with open(widgets_file, "w", encoding="utf-8") as f:
            json.dump(widgets_meta, f, indent=2)
            f.write("\n")

        # 5. Write templates.json
        templates_file = self.out_dir / "templates.json"
        with open(templates_file, "w", encoding="utf-8") as f:
            json.dump(templates_meta, f, indent=2)
            f.write("\n")

        # 6. Build and write gallery.json index
        gallery_widgets_index = []
        for w in widgets_meta:
            w_id = w["id"]
            gallery_widgets_index.append(
                {
                    **w,
                    "renders": widget_renders_map.get(w_id, {}),
                }
            )

        gallery_templates_index = []
        for t in templates_meta:
            t_theme = t["active_theme"]
            t_renders = {}
            for w_name in t.get("widgets", []):
                if w_name in widget_renders_map:
                    # Prefer template's active theme render, fallback to first available
                    if t_theme in widget_renders_map[w_name]:
                        t_renders[w_name] = widget_renders_map[w_name][t_theme]
                    elif widget_renders_map[w_name]:
                        first_theme = next(iter(widget_renders_map[w_name]))
                        t_renders[w_name] = widget_renders_map[w_name][first_theme]

            gallery_templates_index.append(
                {
                    **t,
                    "renders": t_renders,
                }
            )

        gallery_index = {
            "version": "1.0.0",
            "schema": "profileforge-gallery-v1",
            "themes": themes_meta,
            "widgets": gallery_widgets_index,
            "templates": gallery_templates_index,
        }

        gallery_file = self.out_dir / "gallery.json"
        with open(gallery_file, "w", encoding="utf-8") as f:
            json.dump(gallery_index, f, indent=2)
            f.write("\n")

        return {
            "out_dir": str(self.out_dir),
            "themes_count": len(themes_meta),
            "widgets_count": len(widgets_meta),
            "templates_count": len(templates_meta),
            "rendered_assets_count": rendered_assets_count,
        }


def export_gallery(
    out_dir: str = "gallery",
    themes_dir: Optional[str] = None,
    top_themes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Helper function to execute the gallery export pipeline."""
    exporter = GalleryExporter(
        themes_dir=Path(themes_dir) if themes_dir else None,
        out_dir=Path(out_dir),
        top_themes=top_themes,
    )
    return exporter.export()


__all__ = [
    "TOP_THEMES",
    "GalleryExporter",
    "export_gallery",
]
