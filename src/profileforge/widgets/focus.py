from typing import Any

from profileforge.components.layout import Column, Component, Padding
from profileforge.components.style import Style
from profileforge.components.widgets import Card, ProgressBar, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("focus")
class FocusWidget(Widget):
    """Displays current learning goals and projects with progress indicators."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="focus",
            name="Current Focus",
            category=WidgetCategory.DEVELOPMENT,
            description="Displays current learning goals and projects with progress indicators.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["focus", "learning", "development", "goals"],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        request = DataRequest(resource="focus.yaml")
        return connector.fetch(request) if connector else {}

    def transform(self, data: Any, context: BuildContext) -> Any:
        if not isinstance(data, dict):
            return {}
        return data

    def build(self, data: Any, context: BuildContext) -> Component:
        sections = []
        for category, items in data.items():
            cat_label = Text(
                category.upper(),
                style=Style(font_size=12, font_weight="700", color="primary"),
            )

            item_rows = []
            for item in items:
                name = item.get("name", "Unknown")
                progress = item.get("progress", 0)
                item_rows.append(
                    Column(
                        children=[
                            Text(name, style=Style(font_weight="500")),
                            ProgressBar(progress, style=Style(width=350, height=6)),
                        ],
                        spacing=10,
                    )
                )

            category_col = Column(children=[cat_label, *item_rows], spacing=20)
            sections.append(category_col)

        content = Column(children=sections, spacing=30)
        return Card(
            title="Currently Doing",
            child=content,
            style=Style(width=400),
        )
