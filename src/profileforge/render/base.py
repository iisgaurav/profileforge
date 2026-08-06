from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from profileforge.components.layout import Component
from profileforge.core.models import RenderContext


@dataclass(frozen=True)
class RenderNode:
    """Immutable AST node representing a resolved component in the layout tree."""
    component: Component
    x: int
    y: int
    width: int
    height: int
    children: list[RenderNode] = field(default_factory=list)
    debug: dict[str, Any] = field(default_factory=dict)


class Renderer(ABC):
    def __init__(self, context: RenderContext):
        self.context = context
        self.theme = context.theme
        self.typography = context.typography
        self.spacing = context.spacing

    @abstractmethod
    def render(self, node: RenderNode) -> str:
        """Render a resolved layout tree into the final output format (e.g., SVG)."""
        pass
