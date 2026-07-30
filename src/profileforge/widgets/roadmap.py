from profileforge.components.layout import Column, Component, Padding, Row
from profileforge.components.style import Style
from profileforge.components.widgets import Card, ProgressBar, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("roadmap")
class RoadmapWidget(Widget):
    def build(self, context: BuildContext) -> Component:
        # Request data from Local DataSource
        datasource = context.services.datasources.get("local")
        request = DataRequest(resource="roadmap.yaml")
        data = datasource.fetch(request) if datasource else []

        # Build declarative layout tree using v0.2 layout system
        rows = []
        for item in data:
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
            style=Style(width=400, height=250, elevation="medium", variant="solid"),
        )
