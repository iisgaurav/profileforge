from profileforge.components.layout import Column, Component, Padding
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
            label = Text(item, style=Style(font_weight="600", color="text"))
            bar = ProgressBar(100, style=Style(width=350, height=8))
            item_col = Column(children=[label, bar], spacing=10)
            rows.append(item_col)

        content = Column(children=rows, spacing=25)
        return Card(
            title="Backend Expertise",
            child=Padding(child=content, value=25),
            style=Style(width=400),
        )
