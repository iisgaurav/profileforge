from typing import Any

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Card, ProgressBar, Text
from profileforge.core.context import BuildContext
from profileforge.core.registry import register_widget
from profileforge.services.languages import LanguageAggregator
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("github_languages")
class GithubLanguagesWidget(Widget):
    """Widget to display top GitHub languages."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="github_languages",
            name="GitHub Languages",
            category=WidgetCategory.STATS,
            description="Top programming languages breakdown from GitHub repositories.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["github", "languages", "code", "stats"],
            required_connectors=["github"],
        )

    def fetch(self, context: BuildContext) -> Any:
        github_connector = context.services.connectors.get("github")
        username = "iisgaurav"
        if github_connector:
            username = github_connector.config.get("username", "iisgaurav")

        repos = []
        if github_connector:
            try:
                repos = github_connector.get_repositories(username)
            except Exception:
                pass

        return {"username": username, "repos": repos}

    def transform(self, data: Any, context: BuildContext) -> Any:
        repos = data.get("repos", []) if isinstance(data, dict) else []
        ignore_list = []
        for w_cfg in context.config.widgets:
            if w_cfg.name == "github_languages":
                cfg = w_cfg.options.get("config", {})
                ignore_list = cfg.get("ignore", [])
                break

        lang_data, is_estimated = LanguageAggregator.aggregate(
            repos, ignore=ignore_list
        )
        return {
            "languages": lang_data[:5],
            "is_estimated": is_estimated,
        }

    def build(self, data: Any, context: BuildContext) -> Component:
        lang_list = data.get("languages", []) if isinstance(data, dict) else []
        is_estimated = (
            data.get("is_estimated", False) if isinstance(data, dict) else False
        )

        rows = []
        for item in lang_list:
            skill = item.name
            progress = item.percentage

            label_row = Row(
                children=[
                    Text(
                        skill,
                        style=Style(font_size=14, font_weight="bold", color="text"),
                    ),
                    Spacer(width=4),
                    Text(
                        f"{progress}% ({item.repo_count} repos)",
                        style=Style(font_size=12, color="muted"),
                    ),
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
        title = (
            "Estimated Language Distribution"
            if is_estimated
            else "Language Distribution"
        )
        return Card(
            title=title,
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, elevation="medium", variant="solid"),
        )
