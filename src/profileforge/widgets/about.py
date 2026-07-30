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
            f"Hi, I'm {name} 👋", style=Style(font_size=32, font_weight="800", color="text")
        )
        
        # Center badge next to role
        role_text = Text(role, style=Style(font_size=15, font_weight="600", color="text"))
        status_badge = Badge(f"● {status}", style=Style())
        
        role_row = Row(
            children=[role_text, status_badge],
            spacing=12,
            style=Style(align="center")
        )
        
        tagline_text = Text(
            f'"{tagline}"',
            style=Style(font_size=14, color="muted", font_weight="normal"),
        )
        
        children = [name_text, Spacer(style=Style(height=16)), role_row, Spacer(style=Style(height=12)), tagline_text]

        if location:
            loc_text = Text(f"📍 {location}", style=Style(font_size=13, color="muted"))
            children.extend([Spacer(style=Style(height=8)), loc_text])

        content = Column(
            children=children, 
            spacing=0, 
            style=Style(width="fill", height="fill", justify="center", align="center")
        )

        return Card(
            title="",
            child=content,
            style=Style(width=820, height=250, elevation="medium", variant="hero"),
        )
