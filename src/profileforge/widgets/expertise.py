from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("expertise")
class ExpertiseWidget(Widget):
    def build(self, context: BuildContext) -> Component:
        datasource = context.services.datasources.get("local")
        request = DataRequest(resource="expertise.yaml")
        data = datasource.fetch(request) if datasource else {}

        # Fallback for old list format
        if isinstance(data, list):
            skills_dict = {"Skills": data}
        else:
            skills_dict = data.get("skills", {})

        rows = []
        for category, items in skills_dict.items():
            cat_title = Text(
                category.replace("_", " ").title(),
                style=Style(font_size=13, font_weight="600", color="muted"),
            )
            rows.append(cat_title)

            badges = [Badge(item) for item in items]
            # Chunk into rows of 3 to fit nicely in the 480px card
            for i in range(0, len(badges), 3):
                chunk = badges[i : i + 3]
                rows.append(Row(children=chunk, spacing=8))

            rows.append(Spacer(style=Style(height=12)))

        # Remove trailing spacer
        if rows and isinstance(rows[-1], Spacer):
            rows.pop()

        content = Column(children=rows, spacing=8, style=Style(width="fill"))
        return Card(
            title="My Expertise",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=480, elevation="medium", variant="solid"),
        )
