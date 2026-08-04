from typing import Any

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Card, Text, Divider
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("hero")
class HeroWidget(Widget):
    """Developer identity hero card: name, title/role, status badge, tagline, and location."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="hero",
            name="Hero",
            category=WidgetCategory.IDENTITY,
            description="Hero banner displaying developer name, role, status badge, tagline, and location.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=["hero", "identity", "bio", "banner", "developer"],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return {}
        try:
            request = DataRequest(resource="hero.yaml")
            return connector.fetch(request) or {}
        except Exception:
            return {}

    def transform(self, data: Any, context: BuildContext) -> dict[str, Any]:
        if isinstance(data, list):
            data = data[0] if data else {}
        if not isinstance(data, dict):
            data = {}

        # Fallback to main profileforge.yaml project settings if missing
        project_name = getattr(context.config, "project_name", "") or ""
        project_title = getattr(context.config, "project_title", "") or ""

        name = data.get("name") or project_name or "Developer"
        role = (
            data.get("role")
            or data.get("title")
            or project_title
            or "Software Engineer"
        )
        tagline = (
            data.get("tagline")
            or data.get("bio")
            or "Building high-performance software with craft and care."
        )
        status = data.get("status") or "Available for opportunities"
        location = data.get("location") or ""

        return {
            "name": name,
            "role": role,
            "tagline": tagline,
            "status": status,
            "location": location,
        }

    def build(self, data: Any, context: BuildContext) -> Component:
        name = data.get("name", "Developer")
        role = data.get("role", "Software Engineer")
        tagline = data.get("tagline", "")
        status = data.get("status", "Available for opportunities")
        location = data.get("location", "")

        name_text = Text(
            f"Hi, I'm {name} 👋",
            style=Style(font_size=32, font_weight="800", color="text", align="center"),
        )

        role_text = Text(
            role,
            style=Style(font_size=16, font_weight="600", color="primary", align="center"),
        )

        badges = [Badge(f"● {status}", style=Style())]
        if location:
            badges.append(Badge(f"📍 {location}", style=Style()))

        badge_row = Row(
            children=badges,
            spacing=10,
            style=Style(justify="center", align="center"),
        )

        tagline_text = Text(
            f'"{tagline}"',
            style=Style(font_size=14, color="muted", font_weight="normal", align="center"),
        )

        children = [
            name_text,
            Spacer(height=8),
            role_text,
            Spacer(height=16),
            badge_row,
            Spacer(height=24),
            Divider(opacity=0.4, style=Style(width=600)),
            Spacer(height=16),
            tagline_text,
        ]

        content = Column(
            children=children,
            spacing=0,
            style=Style(width="fill", height="fill", justify="center", align="center"),
        )

        return Card(
            title="",
            child=content,
            style=Style(width=820, height=250, elevation="medium", variant="hero"),
        )
