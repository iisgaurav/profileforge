from __future__ import annotations

from typing import Any

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("activity_timeline")
class ActivityTimelineWidget(Widget):
    """Activity Timeline widget displaying recent commits, PR merges, releases, and milestones."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="activity_timeline",
            name="Activity Timeline",
            category=WidgetCategory.DEVELOPMENT,
            description="Recent commit events, pull requests, releases, and development milestones in a chronological timeline.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=[
                "activity",
                "timeline",
                "milestones",
                "commits",
                "releases",
                "development",
                "events",
            ],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return []
        try:
            request = DataRequest(resource="activity_timeline.yaml")
            return connector.fetch(request) or []
        except Exception:
            return []

    def transform(self, data: Any, context: BuildContext) -> list[dict[str, Any]]:
        raw_items = []
        if isinstance(data, dict):
            if "events" in data and isinstance(data["events"], list):
                raw_items = data["events"]
            elif "timeline" in data and isinstance(data["timeline"], list):
                raw_items = data["timeline"]
            elif "activities" in data and isinstance(data["activities"], list):
                raw_items = data["activities"]
        elif isinstance(data, list):
            raw_items = data

        events = []
        for item in raw_items:
            if isinstance(item, dict):
                title = item.get("title") or item.get("event") or "Development Activity"
                event_type = item.get("type") or item.get("category") or "Update"
                repo = item.get("repo") or item.get("project") or ""
                date = item.get("date") or item.get("time") or "Recently"
                desc = item.get("description") or item.get("details") or ""
                events.append(
                    {
                        "title": title,
                        "type": event_type,
                        "repo": repo,
                        "date": date,
                        "description": desc,
                    }
                )

        if not events:
            events = [
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
            ]

        return events

    def build(self, data: Any, context: BuildContext) -> Component:
        events = data if isinstance(data, list) else []

        rows = []
        for i, ev in enumerate(events):
            type_badge = Badge(ev["type"], style=Style())
            title_text = Text(
                ev["title"],
                style=Style(font_size=13, font_weight="700", color="text"),
            )
            date_text = Text(
                ev["date"],
                style=Style(font_size=11, font_weight="600", color="primary"),
            )

            badges_and_title = Row(
                children=[type_badge, title_text],
                spacing=10,
                style=Style(align="center"),
            )

            header_row = Row(
                children=[badges_and_title, date_text],
                spacing=0,
                style=Style(width="fill", justify="space-between", align="center"),
            )
            rows.append(header_row)
            rows.append(Spacer(height=4))

            if ev.get("repo"):
                repo_text = Text(
                    f"📦 {ev['repo']}",
                    style=Style(font_size=11, font_weight="600", color="muted"),
                )
                rows.append(repo_text)
                rows.append(Spacer(height=3))

            if ev.get("description"):
                desc_text = Text(
                    f"▸ {ev['description']}",
                    style=Style(font_size=12, color="muted"),
                )
                rows.append(desc_text)
                rows.append(Spacer(height=2))

            if i < len(events) - 1:
                rows.append(Spacer(height=12))

        if rows and isinstance(rows[-1], Spacer):
            rows.pop()

        content = Column(
            children=rows,
            spacing=0,
            style=Style(width="fill"),
        )

        return Card(
            title="Recent Activity & Milestones",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, elevation="medium", variant="solid"),
        )
