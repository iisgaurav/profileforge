from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Card, ProgressBar, Text
from profileforge.core.context import BuildContext
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("github_languages")
class GithubLanguagesWidget(Widget):
    """Widget to display top GitHub languages."""

    def build(self, context: BuildContext) -> Component:
        github_connector = context.services.connectors.get("github")

        username = "octocat"
        if github_connector:
            username = github_connector.config.get("username", "octocat")

        data = []
        if github_connector:
            try:
                data = github_connector.get_languages(username)
            except Exception:
                pass

        rows = []
        for item in data:
            skill = item.name
            progress = item.percentage

            label_row = Row(
                children=[
                    Text(
                        skill,
                        style=Style(font_size=14, font_weight="bold", color="text"),
                    ),
                    Spacer(width=4),
                    Text(f"{progress}%", style=Style(font_size=12, color="muted")),
                ],
                spacing=0,
                style=Style(justify="space-between", align="center", width="fill"),
            )

            rows.append(
                Column(
                    children=[
                        label_row,
                        Spacer(height=4),
                        ProgressBar(progress=progress, style=Style(width="fill")),
                    ],
                    spacing=0,
                    style=Style(width="fill"),
                )
            )
            rows.append(Spacer(height=16))

        if rows:
            rows.pop()

        content = Column(children=rows, spacing=0, style=Style(width="fill"))
        return Card(
            title="Top Languages",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, height=250, elevation="medium", variant="solid"),
        )
