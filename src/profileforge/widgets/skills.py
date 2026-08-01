from typing import Any

from profileforge.components.layout import Column, Component, Padding, Spacer, Wrap
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("skills")
class SkillsWidget(Widget):
    """Categorized technical skills rendered with styled badge chips."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="skills",
            name="Technical Skills",
            category=WidgetCategory.CAREER,
            description="Groups technical skills into categorized sections with badge chips.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=[
                "skills",
                "technologies",
                "languages",
                "frameworks",
                "tools",
                "career",
                "stack",
            ],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return {}
        try:
            request = DataRequest(resource="skills.yaml")
            return connector.fetch(request) or {}
        except Exception:
            return {}

    def transform(self, data: Any, context: BuildContext) -> dict[str, list[str]]:
        if isinstance(data, dict):
            if "skills" in data and isinstance(data["skills"], (dict, list)):
                data = data["skills"]
            elif "categories" in data and isinstance(data["categories"], (dict, list)):
                data = data["categories"]

        categories: dict[str, list[str]] = {}

        if isinstance(data, dict):
            for cat, items in data.items():
                cat_name = str(cat).replace("_", " ").title()
                if isinstance(items, list):
                    categories[cat_name] = [str(it) for it in items if it]
                elif isinstance(items, str):
                    categories[cat_name] = [
                        it.strip() for it in items.split(",") if it.strip()
                    ]
        elif isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict):
                    cat_name = str(
                        entry.get("category") or entry.get("name") or "General"
                    ).title()
                    items = entry.get("items") or entry.get("skills") or []
                    if isinstance(items, list):
                        categories[cat_name] = [str(it) for it in items if it]
                    elif isinstance(items, str):
                        categories[cat_name] = [
                            it.strip() for it in items.split(",") if it.strip()
                        ]
                elif isinstance(entry, str):
                    categories.setdefault("General", []).append(entry)

        # Default fallback categories if empty
        if not categories:
            categories = {
                "Languages": ["Python", "TypeScript", "Go", "Rust", "SQL"],
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
                "Databases": ["PostgreSQL", "Redis", "MongoDB", "SQLite"],
                "Tools & Architecture": [
                    "Git",
                    "Linux",
                    "GraphQL",
                    "REST APIs",
                    "Neovim",
                ],
            }

        return categories

    def build(self, data: Any, context: BuildContext) -> Component:
        categories = data if isinstance(data, dict) else {}

        rows = []
        for cat_name, skill_items in categories.items():
            cat_header = Text(
                cat_name,
                style=Style(font_size=13, font_weight="700", color="primary"),
            )
            rows.append(cat_header)
            rows.append(Spacer(height=6))

            badges = [Badge(skill, style=Style()) for skill in skill_items]
            wrap = Wrap(
                children=badges,
                spacing=8,
                run_spacing=8,
                style=Style(width="fill"),
            )
            rows.append(wrap)
            rows.append(Spacer(height=14))

        if rows and isinstance(rows[-1], Spacer):
            rows.pop()

        content = Column(
            children=rows,
            spacing=0,
            style=Style(width="fill"),
        )

        return Card(
            title="Technical Skills",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, elevation="medium", variant="solid"),
        )
