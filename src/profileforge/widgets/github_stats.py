from profileforge.components.layout import Column, Component, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget


@register_widget("github_stats")
class GithubStatsWidget(Widget):
    """Widget to display GitHub statistics."""

    def build(self, context: BuildContext) -> Component:
        local_connector = context.services.connectors.get("local")
        github_connector = context.services.connectors.get("github")

        request = DataRequest(resource="about.yaml")
        data = local_connector.fetch(request) if local_connector else {}
        if isinstance(data, list):
            data = data[0] if data else {}

        username = data.get("github_username", "octocat")

        stats = None
        if github_connector:
            try:
                stats = github_connector.get_stats(username)
            except Exception:
                pass

        stars = stats.stars if stats else 0
        prs = stats.prs if stats else 0
        commits = stats.commits if stats else 0

        title_text = Text(
            f"GitHub Stats ({username})",
            style=Style(font_size=20, font_weight="bold", color="text"),
        )

        stars_text = Text(f"⭐ Stars: {stars}", style=Style(font_size=16, color="text"))
        prs_text = Text(f"🔄 PRs: {prs}", style=Style(font_size=16, color="text"))
        commits_text = Text(
            f"🔥 Commits: {commits}", style=Style(font_size=16, color="text")
        )

        content = Column(
            children=[
                title_text,
                Spacer(height=16),
                stars_text,
                Spacer(height=8),
                prs_text,
                Spacer(height=8),
                commits_text,
            ],
            spacing=0,
            style=Style(width="fill", height="fill", justify="center", align="center"),
        )

        return Card(
            title="",
            child=content,
            style=Style(width=400, height=200, elevation="medium", variant="default"),
        )
