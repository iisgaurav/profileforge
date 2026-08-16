__layer__ = "Layer 7 — Widgets"
from profileforge.widgets import (  # noqa: F401
    about,
    activity_timeline,
    experience,
    focus,
    github_languages,
    github_stats,
    now,
    repositories,
    roadmap,
    skills,
    social,
)
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata

__all__ = [
    "Widget",
    "WidgetCategory",
    "WidgetMetadata",
]
