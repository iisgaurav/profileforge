from typing import Any

from profileforge.components.layout import Component, Padding, Row
from profileforge.components.style import Style
from profileforge.components.widgets import Card, CircularMetric, Metric, MetricGroup
from profileforge.core.context import BuildContext
from profileforge.core.models import MetricsConfig
from profileforge.core.registry import register_widget
from profileforge.services.stats import ScoreCalculator
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("github_stats")
class GithubStatsWidget(Widget):
    """Widget to display GitHub statistics."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="github_stats",
            name="GitHub Stats",
            category=WidgetCategory.STATS,
            description="Summary of GitHub stars, PRs, commits, and overall developer score.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["github", "stats", "metrics", "analytics"],
            required_connectors=["github"],
        )

    def fetch(self, context: BuildContext) -> Any:
        github_connector = context.services.connectors.get("github")
        username = "iisgaurav"
        if github_connector:
            username = github_connector.config.get("username", "iisgaurav")

        stats = None
        if github_connector:
            try:
                stats = github_connector.get_stats(username)
            except Exception:
                pass

        return {"username": username, "stats": stats}

    def transform(self, data: Any, context: BuildContext) -> Any:
        stats = data.get("stats") if isinstance(data, dict) else None
        username = (
            data.get("username", "iisgaurav") if isinstance(data, dict) else "iisgaurav"
        )

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

        return {
            "username": username,
            "score": score,
            "stars": stars,
            "prs": prs,
            "commits": commits,
        }

    def build(self, data: Any, context: BuildContext) -> Component:
        username = data.get("username", "iisgaurav")
        score = data.get("score", 0)
        stars = data.get("stars", 0)
        prs = data.get("prs", 0)
        commits = data.get("commits", 0)

        circular = CircularMetric(
            value=score, max_value=1000, label="Total Score", icon="star"
        )

        metrics = [
            Metric(label="Total Stars", value=stars, icon="star"),
            Metric(label="Pull Requests", value=prs, icon="pr"),
            Metric(label="Total Commits", value=commits, icon="commit"),
            Metric(label="Repositories", value="--", icon="repo"),  # dummy for layout
        ]

        group = MetricGroup(metrics=metrics, columns=2, spacing=24)

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
