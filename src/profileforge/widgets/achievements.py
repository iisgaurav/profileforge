from __future__ import annotations

from typing import Any

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("achievements")
class AchievementsWidget(Widget):
    """Achievements widget displaying developer unlock badges, accolades, and GitHub awards."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="achievements",
            name="Achievements",
            category=WidgetCategory.STATS,
            description="Developer unlock badges showcasing milestones, GitHub awards, and technical accomplishments.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=[
                "achievements",
                "badges",
                "awards",
                "stats",
                "unlocks",
                "gamification",
                "github",
            ],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return []
        try:
            request = DataRequest(resource="achievements.yaml")
            return connector.fetch(request) or []
        except Exception:
            return []

    def transform(self, data: Any, context: BuildContext) -> list[dict[str, Any]]:
        raw_items = []
        if isinstance(data, dict):
            if "achievements" in data and isinstance(data["achievements"], list):
                raw_items = data["achievements"]
            elif "badges" in data and isinstance(data["badges"], list):
                raw_items = data["badges"]
            elif "awards" in data and isinstance(data["awards"], list):
                raw_items = data["awards"]
        elif isinstance(data, list):
            raw_items = data

        achievements = []
        for item in raw_items:
            if isinstance(item, dict):
                name = item.get("name") or item.get("title") or "Developer Badge"
                tier = item.get("tier") or item.get("level") or "Unlocked"
                desc = item.get("description") or item.get("details") or ""
                achievements.append(
                    {
                        "name": name,
                        "tier": tier,
                        "description": desc,
                    }
                )

        if not achievements:
            achievements = [
                {
                    "name": "🦈 Pull Shark",
                    "tier": "Gold (x4)",
                    "description": "Merged 250+ pull requests with continuous test coverage & zero rollbacks.",
                },
                {
                    "name": "⚡ Quickdraw",
                    "tier": "Gold",
                    "description": "Reviewed and responded to incoming code reviews within 5 minutes.",
                },
                {
                    "name": "🧠 Galaxy Brain",
                    "tier": "Diamond",
                    "description": "Authored and answered 50+ technical architectural proposals & discussions.",
                },
                {
                    "name": "🔥 1,000+ Commits",
                    "tier": "Legendary",
                    "description": "Continuous code contribution across high-impact production repositories.",
                },
            ]

        return achievements

    def build(self, data: Any, context: BuildContext) -> Component:
        achievements = data if isinstance(data, list) else []

        rows = []
        # Build 2-column or grid rows
        for i in range(0, len(achievements), 2):
            col_items = []
            for j in range(i, min(i + 2, len(achievements))):
                ach = achievements[j]
                name_text = Text(
                    ach["name"],
                    style=Style(font_size=13, font_weight="700", color="text"),
                )
                tier_badge = Badge(ach["tier"], style=Style())

                header = Row(
                    children=[name_text, tier_badge],
                    spacing=8,
                    style=Style(align="center"),
                )

                card_children = [header, Spacer(height=4)]
                if ach.get("description"):
                    desc_text = Text(
                        ach["description"],
                        style=Style(font_size=11, color="muted"),
                    )
                    card_children.append(desc_text)

                box = Column(
                    children=card_children,
                    spacing=0,
                    style=Style(width=370),
                )
                col_items.append(box)

            row_layout = Row(
                children=col_items,
                spacing=24,
                style=Style(width="fill", justify="space-between"),
            )
            rows.append(row_layout)
            if i + 2 < len(achievements):
                rows.append(Spacer(height=12))

        content = Column(
            children=rows,
            spacing=0,
            style=Style(width="fill"),
        )

        return Card(
            title="Developer Achievements & Unlock Badges 🏆",
            child=content,
            style=Style(width=820, elevation="medium", variant="solid"),
        )
