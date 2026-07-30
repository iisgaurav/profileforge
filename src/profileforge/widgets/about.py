from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("about")
class AboutWidget(Widget):
    """Hero card: name, role, status badge, tagline, and quick links."""

    def build(self, context: BuildContext) -> Component:
        datasource = context.services.datasources.get("local")
        request = DataRequest(resource="about.yaml")
        data = datasource.fetch(request) if datasource else {}

        if isinstance(data, list):
            data = data[0] if data else {}

        name = data.get("name", "Your Name")
        role = data.get("role", "Software Engineer")
        tagline = data.get("tagline", "Building things that matter.")
        status = data.get("status", "Open to collaborate")
        location = data.get("location", "")

        name_text = Text(
            name, style=Style(font_size=22, font_weight="700", color="text")
        )
        role_text = Text(role, style=Style(font_size=14, color="muted"))
        tagline_text = Text(
            f'"{tagline}"',
            style=Style(font_size=13, color="muted", font_weight="normal"),
        )
        status_badge = Badge(f"● {status}", style=Style())

        top_row = Row(
            children=[
                Column(
                    children=[name_text, Spacer(style=Style(height=4)), role_text],
                    spacing=2,
                    style=Style(width="fill"),
                ),
                status_badge,
            ],
            style=Style(width="fill", justify="space-between", align="start"),
        )

        children = [top_row, Spacer(style=Style(height=10)), tagline_text]

        if location:
            loc_text = Text(f"📍 {location}", style=Style(font_size=12, color="muted"))
            children.append(Spacer(style=Style(height=6)))
            children.append(loc_text)

        content = Column(children=children, spacing=0, style=Style(width="fill"))

        return Card(
            title="",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, height=250, elevation="medium", variant="solid"),
        )
