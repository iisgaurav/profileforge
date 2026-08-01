from typing import Any

from profileforge.components.layout import Column, Component, Padding, Spacer, Wrap
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("social")
class SocialWidget(Widget):
    """Displays a clean wrap of social media links, handles, and developer profiles."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="social",
            name="Social Links",
            category=WidgetCategory.SOCIAL,
            description="Displays a clean row and wrap of social media links and profiles.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["social", "links", "handles", "contacts", "community"],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return {}
        try:
            request = DataRequest(resource="social.yaml")
            return connector.fetch(request) or {}
        except Exception:
            return {}

    def transform(self, data: Any, context: BuildContext) -> list[dict[str, str]]:
        items = []

        if isinstance(data, dict):
            # If nested under 'social' or 'links'
            if "social" in data and isinstance(data["social"], (dict, list)):
                data = data["social"]
            elif "links" in data and isinstance(data["links"], (dict, list)):
                data = data["links"]

        if isinstance(data, dict):
            for platform, val in data.items():
                if isinstance(val, dict):
                    handle = (
                        val.get("username") or val.get("handle") or val.get("url") or ""
                    )
                else:
                    handle = str(val) if val else ""
                if handle:
                    items.append({"platform": platform, "handle": handle})
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    platform = item.get("platform") or item.get("name") or "link"
                    handle = (
                        item.get("username")
                        or item.get("handle")
                        or item.get("url")
                        or ""
                    )
                    if handle:
                        items.append({"platform": platform, "handle": handle})
                elif isinstance(item, str):
                    items.append({"platform": "link", "handle": item})

        # Fallback default items if none provided
        if not items:
            items = [
                {"platform": "github", "handle": "octocat"},
                {"platform": "twitter", "handle": "octocat"},
                {"platform": "linkedin", "handle": "in/octocat"},
                {"platform": "website", "handle": "https://octocat.dev"},
            ]

        formatted = []
        platform_labels = {
            "github": "🐙 GitHub",
            "twitter": "𝕏 Twitter",
            "x": "𝕏 Twitter",
            "linkedin": "💼 LinkedIn",
            "website": "🌐 Website",
            "site": "🌐 Website",
            "blog": "✍️ Blog",
            "discord": "💬 Discord",
            "email": "✉️ Email",
            "mail": "✉️ Email",
            "youtube": "▶️ YouTube",
            "twitch": "🎮 Twitch",
            "mastodon": "🐘 Mastodon",
        }

        for it in items:
            raw_p = it["platform"].lower()
            p_prefix = platform_labels.get(raw_p, f"🔗 {it['platform'].title()}")
            h = it["handle"]
            if (
                not h.startswith("@")
                and not h.startswith("http")
                and not h.startswith("/")
                and not h.startswith("in/")
                and "@" not in h
                and raw_p in ("github", "twitter", "x", "mastodon")
            ):
                h = f"@{h}"
            formatted.append(
                {"label": f"{p_prefix}: {h}", "platform": raw_p, "handle": h}
            )

        return formatted

    def build(self, data: Any, context: BuildContext) -> Component:
        items = data if isinstance(data, list) else []

        subtitle = Text(
            "Let's connect and build together:",
            style=Style(font_size=13, font_weight="500", color="muted"),
        )

        badges = [Badge(item["label"], style=Style()) for item in items]
        wrap = Wrap(
            children=badges,
            spacing=10,
            run_spacing=10,
            style=Style(width="fill"),
        )

        content = Column(
            children=[
                subtitle,
                Spacer(height=12),
                wrap,
            ],
            spacing=0,
            style=Style(width="fill"),
        )

        return Card(
            title="Connect & Socials",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, elevation="medium", variant="solid"),
        )
