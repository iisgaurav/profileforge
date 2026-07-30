from __future__ import annotations

from abc import ABC

from profileforge.components.style import Style


class Component(ABC):
    """Base class for all layout and visual components."""

    def __init__(self, style: Style | None = None):
        self.style = style or Style()

    # These will be computed by the layout engine
    computed_x: int = 0
    computed_y: int = 0
    computed_width: int = 0
    computed_height: int = 0


class Row(Component):
    def __init__(
        self, children: list[Component], spacing: int = 0, style: Style | None = None
    ):
        super().__init__(style)
        self.children = children
        self.spacing = spacing


class Column(Component):
    def __init__(
        self, children: list[Component], spacing: int = 0, style: Style | None = None
    ):
        super().__init__(style)
        self.children = children
        self.spacing = spacing


class Padding(Component):
    def __init__(self, child: Component, value: int = 0, style: Style | None = None):
        super().__init__(style)
        self.child = child
        self.value = value


class Spacer(Component):
    def __init__(self, width: int = 0, height: int = 0, style: Style | None = None):
        super().__init__(style)
        self.style.width = width
        self.style.height = height


class Wrap(Component):
    def __init__(
        self,
        children: list[Component],
        spacing: int = 0,
        run_spacing: int = 0,
        style: Style | None = None,
    ):
        super().__init__(style)
        self.children = children
        self.spacing = spacing
        self.run_spacing = run_spacing
