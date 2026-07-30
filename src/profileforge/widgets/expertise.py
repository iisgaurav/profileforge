from profileforge.components.layout import Column, Component, Padding, Row
from profileforge.components.style import Style
from profileforge.components.widgets import Card, ProgressBar, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("expertise")
class ExpertiseWidget(Widget):
    def build(self, context: BuildContext) -> Component:
        datasource = context.services.datasources.get("local")
        request = DataRequest(resource="expertise.yaml")
        data = datasource.fetch(request) if datasource else []

        rows = []
        for item in data:
            # Bullet point character for the list
            bullet = Text(
                "•", style=Style(font_weight="800", color="primary", font_size=18)
            )
            label = Text(
                item, style=Style(font_weight="600", color="text", font_size=16)
            )

            # Place bullet and label in a row
            item_row = Row(
                children=[bullet, label],
                spacing=12,
                style=Style(width="fill", align="center"),
            )
            rows.append(item_row)

        content = Column(children=rows, spacing=16, style=Style(width="fill"))
        return Card(
            title="Backend Expertise",
            child=Padding(child=content, value=24, style=Style(width="fill")),
            style=Style(width=420, elevation="medium", variant="solid"),
        )
