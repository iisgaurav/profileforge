from profileforge.components.layout import Column, Component, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("github_stats")
class GithubStatsWidget(Widget):
    """Widget to display GitHub statistics."""

    def build(self, context: BuildContext) -> Component:
        github_connector = context.services.connectors.get("github")

        username = "octocat"
        if github_connector:
            username = github_connector.config.get("username", "octocat")

        stats = None
        if github_connector:
            try:
                stats = github_connector.get_stats(username)
            except Exception:
                pass

        stars = stats.stars if stats else 0
        prs = stats.prs if stats else 0
        commits = stats.commits if stats else 0

        def create_stat_block(label: str, value: str, icon: str) -> Component:
            return Column(
                children=[
                    Row(
                        children=[
                            Text(icon, style=Style(font_size=16)),
                            Spacer(width=8),
                            Text(
                                label.upper(),
                                style=Style(
                                    font_size=12, font_weight="bold", color="muted"
                                ),
                            ),
                        ],
                        spacing=0,
                        style=Style(align="center"),
                    ),
                    Spacer(height=12),
                    Text(
                        value,
                        style=Style(font_size=32, font_weight="bold", color="text"),
                    ),
                ],
                spacing=0,
                style=Style(align="center"),
            )

        content = Row(
            children=[
                create_stat_block("Total Stars", str(stars), "⭐"),
                create_stat_block("Pull Requests", str(prs), "🔄"),
                create_stat_block("Total Commits", str(commits), "🔥"),
            ],
            spacing=0,
            style=Style(width="fill", justify="space-between", align="center"),
        )

        from profileforge.components.layout import Padding

        return Card(
            title=f"GitHub Stats (@{username})",
            child=Padding(child=content, value=40, style=Style(width="fill")),
            style=Style(width=820, elevation="medium", variant="solid"),
        )
