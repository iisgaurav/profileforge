from typing import Any

from profileforge.components.layout import Column, Component, Padding, Spacer, Wrap
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("expertise")
class ExpertiseWidget(Widget):
    """Technical skills and expertise grouped by domain."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="expertise",
            name="Expertise",
            category=WidgetCategory.CAREER,
            description="Technical skills and expertise grouped by domain.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["skills", "expertise", "stack", "career"],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        request = DataRequest(resource="expertise.yaml")
        return connector.fetch(request) if connector else {}

    def transform(self, data: Any, context: BuildContext) -> Any:
        if isinstance(data, list):
            return {"Skills": data}
        if isinstance(data, dict):
            return data.get("skills", {})
        return {}

    def build(self, data: Any, context: BuildContext) -> Component:
        skills_dict = data if isinstance(data, dict) else {}

        rows = []
        for category, items in skills_dict.items():
            cat_title = Text(
                category.replace("_", " ").title(),
                style=Style(font_size=13, font_weight="600", color="muted"),
            )
            rows.append(cat_title)

            badges = [Badge(item) for item in items]

            # Use the Wrap component for dynamic badge flow
            rows.append(
                Wrap(
                    children=badges, spacing=8, run_spacing=8, style=Style(width="fill")
                )
            )
            rows.append(Spacer(style=Style(height=12)))

        # Remove trailing spacer
        if rows and isinstance(rows[-1], Spacer):
            rows.pop()

        content = Column(children=rows, spacing=8, style=Style(width="fill"))
        return Card(
            title="My Expertise",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, height=250, elevation="medium", variant="solid"),
        )
