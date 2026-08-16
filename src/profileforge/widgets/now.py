__layer__ = "Layer 7 — Widgets"
from typing import Any

from profileforge.components.layout import Column, Component, Inline
from profileforge.components.style import Style
from profileforge.components.widgets import Card, Text
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata


@register_widget("now")
class NowWidget(Widget):
    """Derek Sivers-style 'Now' page widget: what I'm currently building, reading, learning, and focusing on."""

    def metadata(self) -> WidgetMetadata:
        return WidgetMetadata(
            id="now",
            name="Now",
            category=WidgetCategory.DEVELOPMENT,
            description="Derek Sivers-style 'Now' widget showing active building, reading, learning, and focus.",
            version="1.0.0",
            author="ProfileForge Team",
            tags=[
                "now",
                "current",
                "building",
                "reading",
                "learning",
                "development",
                "focus",
            ],
            required_connectors=["local"],
        )

    def fetch(self, context: BuildContext) -> Any:
        connector = context.services.connectors.get("local")
        if not connector:
            return {}
        try:
            request = DataRequest(resource="now.yaml")
            return connector.fetch(request) or {}
        except Exception:
            return {}

    def transform(self, data: Any, context: BuildContext) -> dict[str, Any]:
        if isinstance(data, list):
            data = data[0] if data else {}
        if not isinstance(data, dict):
            data = {}

        building = (
            data.get("building")
            or data.get("working_on")
            or "ProfileForge — An extensible, beautiful developer profile engine"
        )
        learning = (
            data.get("learning")
            or data.get("studying")
            or "Rust systems programming, WebAssembly & high-concurrency architectures"
        )
        reading = (
            data.get("reading")
            or data.get("book")
            or "Designing Data-Intensive Applications by Martin Kleppmann"
        )
        focus = (
            data.get("focus")
            or data.get("focusing_on")
            or "Developer tooling, open-source maintainability, and declarative UI design"
        )
        location = data.get("location") or ""
        updated = data.get("updated") or data.get("last_updated") or ""

        sections = [
            {"title": "🔨 Building", "content": building},
            {"title": "🧠 Learning", "content": learning},
            {"title": "📚 Reading", "content": reading},
            {"title": "🎯 Focusing On", "content": focus},
        ]

        return {
            "sections": sections,
            "location": location,
            "updated": updated,
        }

    def build(self, data: Any, context: BuildContext) -> Component:
        sections = data.get("sections", []) if isinstance(data, dict) else []
        location = data.get("location", "") if isinstance(data, dict) else ""
        updated = data.get("updated", "") if isinstance(data, dict) else ""

        rows = []
        for sec in sections:
            header = Text(
                sec["title"],
                style=Style(font_size=13, font_weight="700", color="primary"),
            )
            body = Text(
                str(sec["content"]),
                style=Style(font_size=13, font_weight="normal", color="text"),
            )
            rows.extend([header, body])

        meta_items = []
        if location:
            meta_items.append(
                Text(f"📍 {location}", style=Style(font_size=12, color="muted"))
            )
        if updated:
            meta_items.append(
                Text(f"🕒 Updated: {updated}", style=Style(font_size=12, color="muted"))
            )

        if meta_items:
            meta_row = Inline(
                children=meta_items,
                gap=16,
                style=Style(width="fill", justify="space-between", align="center"),
            )
            rows.extend([meta_row])
        content = Column(
            children=rows,
            gap=16,
            style=Style(width="fill"),
        )

        return Card(
            title="What I'm Doing Now",
            child=content,
            style=Style(width=820, elevation="medium", variant="solid"),
        )
