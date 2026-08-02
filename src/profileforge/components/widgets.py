from __future__ import annotations

from profileforge.components.layout import Component
from profileforge.components.style import Style


class Card(Component):
    def __init__(self, title: str, child: Component, style: Style | None = None):
        super().__init__(style)
        self.title = title
        self.child = child


class Text(Component):
    def __init__(self, value: str, style: Style | None = None):
        super().__init__(style)
        self.value = value


class ProgressBar(Component):
    def __init__(self, progress: int, style: Style | None = None):
        super().__init__(style)
        self.progress = progress


class Icon(Component):
    def __init__(self, svg_path: str, style: Style | None = None):
        super().__init__(style)
        self.svg_path = svg_path


class Badge(Component):
    def __init__(self, label: str, style: Style | None = None):
        super().__init__(style)
        self.label = label


class Metric(Component):
    def __init__(
        self,
        label: str,
        value: str | int | float,
        icon: str | None = None,
        trend: int | float | None = None,
        style: Style | None = None,
    ):
        super().__init__(style)
        self.label = label
        self.value = value
        self.icon = icon
        self.trend = trend


class MetricGroup(Component):
    def __init__(
        self,
        metrics: list[Component],
        columns: int = 2,
        spacing: int = 16,
        style: Style | None = None,
    ):
        super().__init__(style)
        self.metrics = metrics
        self.columns = columns
        self.spacing = spacing


class CircularMetric(Component):
    def __init__(
        self,
        value: float,
        max_value: float,
        label: str,
        icon: str | None = None,
        style: Style | None = None,
    ):
        super().__init__(style)
        self.value = value
        self.max_value = max_value
        self.label = label
        self.icon = icon


class Divider(Component):
    def __init__(self, opacity: float = 0.4, style: Style | None = None):
        super().__init__(style)
        self.opacity = opacity
