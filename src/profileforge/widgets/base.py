from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from profileforge.components.layout import Component
from profileforge.core.context import BuildContext


class WidgetCategory:
    IDENTITY = "identity"
    STATS = "stats"
    PROJECTS = "projects"
    CAREER = "career"
    DEVELOPMENT = "development"
    CONTENT = "content"
    SOCIAL = "social"
    UTILITY = "utility"


@dataclass
class WidgetMetadata:
    id: str
    name: str
    category: str
    description: str = ""
    version: str = "1.0.0"
    author: Optional[str] = None
    license: str = "MIT"
    schema: int = 1
    tags: list[str] = field(default_factory=list)
    required_connectors: list[str] = field(default_factory=list)
    experimental: bool = False
    deprecated: bool = False


class Widget(ABC):
    """
    Abstract base class for all ProfileForge widgets.
    Defines the standard widget lifecycle and execution hooks.
    """

    @abstractmethod
    def metadata(self) -> WidgetMetadata:
        """Return the metadata definition for the widget."""
        pass

    def validate(self, context: BuildContext) -> None:
        """
        Validation hook executed before data resolution.
        Subclasses can perform pre-render validation checks here.
        """
        pass

    def resolve_connectors(self, context: BuildContext) -> dict[str, Any]:
        """
        Connector lookup hook to resolve required data connectors from context.
        """
        resolved = {}
        try:
            meta = self.metadata()
            for name in meta.required_connectors:
                if name in context.services.connectors:
                    resolved[name] = context.services.connectors[name]
        except Exception:
            pass
        return resolved

    def fetch(self, context: BuildContext) -> Any:
        """
        Data retrieval hook to fetch raw data from connectors or local sources.
        """
        return None

    def transform(self, data: Any, context: BuildContext) -> Any:
        """
        Data transformation hook to parse, aggregate, or clean fetched data.
        """
        return data

    @abstractmethod
    def build(self, data: Any, context: BuildContext) -> Component:
        """
        Pure UI building hook that transforms data into a Component layout tree.
        """
        pass

    def post_build(self, component: Component, context: BuildContext) -> Component:
        """
        Post-processing hook for layout, styling, or decoration adjustments.
        """
        return component

    def render_safe(self, context: BuildContext) -> Component:
        """
        Lifecycle orchestrator with failure isolation.
        Catches any exception and returns a graceful fallback Card component.
        """
        try:
            self.validate(context)
            self.resolve_connectors(context)
            raw_data = self.fetch(context)
            data = self.transform(raw_data, context)
            component = self.build(data, context)
            return self.post_build(component, context)
        except Exception as e:
            return self._create_fallback(context, e)

    def _create_fallback(self, context: BuildContext, error: Exception) -> Component:
        """Builds a fallback card displaying error and connector diagnostics."""
        try:
            meta = self.metadata()
            widget_name = meta.name
            req_connectors = (
                ", ".join(meta.required_connectors)
                if meta.required_connectors
                else "None"
            )
        except Exception:
            widget_name = self.__class__.__name__
            req_connectors = "Unknown"

        from profileforge.components.layout import Column, Padding, Spacer
        from profileforge.components.style import Style
        from profileforge.components.widgets import Card, Text

        err_msg = str(error) or repr(error)

        fallback_children = [
            Text(
                f"Failed to render widget: {err_msg}",
                style=Style(font_size=13, color="muted"),
            ),
            Spacer(height=8),
            Text(
                f"Required Connectors: {req_connectors}",
                style=Style(font_size=12, color="muted"),
            ),
        ]

        content = Column(
            children=fallback_children,
            spacing=0,
            style=Style(width="fill"),
        )

        return Card(
            title=f"Error: {widget_name}",
            child=Padding(child=content, value=20, style=Style(width="fill")),
            style=Style(width=820, height=140, elevation="medium", variant="solid"),
        )
