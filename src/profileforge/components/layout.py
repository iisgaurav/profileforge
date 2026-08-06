from __future__ import annotations

from abc import ABC

from profileforge.components.style import Style, Constraints


class Component(ABC):
    """Base class for all components."""

    def __init__(self, constraints: Constraints | None = None, style: Style | None = None):
        self.constraints = constraints or Constraints()
        self.style = style or Style()

    # These will be computed by the layout engine and later baked into immutable RenderNodes
    computed_x: int = 0
    computed_y: int = 0
    computed_width: int = 0
    computed_height: int = 0


class LayoutComponent(Component):
    """Base class for all components that manage layout but do not render visual appearance."""
    pass


class VisualComponent(Component):
    """Base class for all components that render visual appearance but do not manage layout."""
    pass


class Row(LayoutComponent):
    def __init__(
        self, children: list[Component], gap: int = 0, spacing: int | None = None, style: Style | None = None, constraints: Constraints | None = None
    ):
        super().__init__(constraints, style)
        self.children = children
        self.gap = spacing if spacing is not None else gap
        self.spacing = self.gap  # For backward compatibility during migration


class Column(LayoutComponent):
    def __init__(
        self, children: list[Component], gap: int = 0, spacing: int | None = None, style: Style | None = None, constraints: Constraints | None = None
    ):
        super().__init__(constraints, style)
        self.children = children
        self.gap = spacing if spacing is not None else gap
        self.spacing = self.gap  # For backward compatibility


class Inline(LayoutComponent):
    def __init__(
        self, children: list[Component], gap: int = 0, style: Style | None = None, constraints: Constraints | None = None
    ):
        super().__init__(constraints, style)
        self.children = children
        self.gap = gap


class Stack(LayoutComponent):
    def __init__(
        self, children: list[Component], style: Style | None = None, constraints: Constraints | None = None
    ):
        super().__init__(constraints, style)
        self.children = children


class Grid(LayoutComponent):
    def __init__(
        self, children: list[Component], gap: int = 0, style: Style | None = None, constraints: Constraints | None = None
    ):
        super().__init__(constraints, style)
        self.children = children
        self.gap = gap


class Padding(LayoutComponent):
    def __init__(self, child: Component, value: int = 0, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.child = child
        self.value = value


class Spacer(LayoutComponent):
    def __init__(self, width: int = 0, height: int = 0, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        # Migrate width/height to constraints internally
        self.constraints.preferred_width = width
        self.style.height = height


class Wrap(LayoutComponent):
    def __init__(
        self,
        children: list[Component],
        spacing: int = 0,
        run_spacing: int = 0,
        style: Style | None = None,
        constraints: Constraints | None = None
    ):
        super().__init__(constraints, style)
        self.children = children
        self.spacing = spacing
        self.run_spacing = run_spacing
