from __future__ import annotations

from profileforge.components.layout import Component, VisualComponent
from profileforge.components.style import Style, Constraints
from profileforge.core.models import PercentageDisplay


class Card(VisualComponent):
    def __init__(self, title: str, child: Component, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.title = title
        self.child = child


class Text(VisualComponent):
    def __init__(self, value: str, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.value = value


class ProgressBar(VisualComponent):
    def __init__(self, progress: int, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.progress = progress


class ProgressMetric(VisualComponent):
    def __init__(
        self,
        label: str,
        value: int,
        display: PercentageDisplay = PercentageDisplay.RIGHT,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.label = label
        self.value = value
        self.display = display


class Icon(VisualComponent):
    def __init__(self, svg_path: str, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.svg_path = svg_path


class Badge(VisualComponent):
    def __init__(self, label: str, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.label = label


class Metric(VisualComponent):
    def __init__(
        self,
        label: str,
        value: str | int | float,
        icon: str | None = None,
        trend: int | float | None = None,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.label = label
        self.value = value
        self.icon = icon
        self.trend = trend


class MetricGroup(VisualComponent):
    def __init__(
        self,
        metrics: list[Component],
        columns: int = 2,
        spacing: int = 16,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.metrics = metrics
        self.columns = columns
        self.spacing = spacing


class CircularMetric(VisualComponent):
    def __init__(
        self,
        value: float,
        max_value: float,
        label: str,
        icon: str | None = None,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.value = value
        self.max_value = max_value
        self.label = label
        self.icon = icon


class Divider(VisualComponent):
    def __init__(self, opacity: float = 0.4, style: Style | None = None, constraints: Constraints | None = None):
        super().__init__(constraints, style)
        self.opacity = opacity
