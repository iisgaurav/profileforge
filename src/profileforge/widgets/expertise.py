from profileforge.components.layout import Column, Component, Padding, Row
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card
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

        badges = [Badge(item) for item in data]
        rows = []
        for i in range(0, len(badges), 2):
            chunk = badges[i : i + 2]
            rows.append(Row(children=chunk, spacing=8))

        content = Column(children=rows, spacing=8, style=Style(width="fill"))
        return Card(
            title="Backend Expertise",
            child=Padding(child=content, value=24, style=Style(width="fill")),
            style=Style(width=480, height=300, elevation="medium", variant="solid"),
        )
