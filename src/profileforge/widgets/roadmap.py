from typing import Any

from profileforge.components.layout import Column, Component, Padding, Row
from profileforge.components.style import Style
from profileforge.components.widgets import Card, ProgressBar, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("roadmap")
class RoadmapWidget(Widget):
    """Learning and career milestones with progress bars."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="roadmap",
            name="Roadmap",
            category=WidgetCategory.DEVELOPMENT,
            description="Learning and career milestones with progress bars.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["roadmap", "milestones", "progress", "development"],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        request = DataRequest(resource="roadmap.yaml")
        return connector.fetch(request) if connector else []

    def transform(self, data: Any, context: BuildContext) -> Any:
        if not isinstance(data, list):
            return []
        return data

    def build(self, data: Any, context: BuildContext) -> Component:
        items = data if isinstance(data, list) else []

        rows = []
        for item in items:
            skill = item.get("skill", "Unknown")
            progress = item.get("progress", 0)

            label_row = Row(
                children=[
                    Text(skill, style=Style(font_weight="600", color="text")),
                    Text(f"{progress}%", style=Style(font_size=13, color="muted")),
                ],
                style=Style(width="fill", justify="space-between", align="end"),
            )

            bar = ProgressBar(
                progress, style=Style(width="fill", height=8, color="primary")
            )

            item_col = Column(
                children=[label_row, bar], spacing=6, style=Style(width="fill")
            )
            rows.append(item_col)

        content = Column(children=rows, spacing=16, style=Style(width="fill"))
        return Card(
            title="Learning Roadmap",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, height=250, elevation="medium", variant="solid"),
        )
