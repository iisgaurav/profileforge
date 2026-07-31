from profileforge.components.layout import Component, Padding, Row
from profileforge.components.style import Style
from profileforge.components.widgets import Card, CircularMetric, Metric, MetricGroup
from profileforge.core.context import BuildContext
from profileforge.core.models import MetricsConfig
from profileforge.core.registry import register_widget
from profileforge.services.stats import ScoreCalculator
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

        stats_dict = {
            "stars": stars,
            "prs": prs,
            "commits": commits,
        }

        metrics_config = getattr(context.config, "metrics", MetricsConfig())
        score_calc = ScoreCalculator(metrics_config)
        score = score_calc.calculate(stats_dict)

        circular = CircularMetric(
            value=score, max_value=1000, label="Total Score", icon="star"
        )

        metrics = [
            Metric(label="Total Stars", value=stars, icon="star"),
            Metric(label="Pull Requests", value=prs, icon="pr"),
            Metric(label="Total Commits", value=commits, icon="commit"),
            Metric(label="Repositories", value="--", icon="repo"),  # dummy for layout
        ]

        group = MetricGroup(metrics=metrics, columns=2, spacing=16)

        content = Row(
            children=[circular, group],
            spacing=64,
            style=Style(width="fill", justify="center", align="center"),
        )

        return Card(
            title=f"GitHub Stats (@{username})",
            child=Padding(child=content, value=40, style=Style(width="fill")),
            style=Style(width=820, elevation="medium", variant="solid"),
        )
