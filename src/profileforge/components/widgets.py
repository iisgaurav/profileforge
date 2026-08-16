from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from profileforge.components.layout import Component, VisualComponent
from profileforge.components.style import Constraints, Style
from profileforge.core.models import PercentageDisplay, Size

if TYPE_CHECKING:
    from profileforge.render.measurer import IntrinsicMeasurer


class Card(VisualComponent):
    def __init__(
        self,
        title: str,
        child: Component,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.title = title
        self.child = child


class Text(VisualComponent):
    def __init__(
        self,
        value: str,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.value = value

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        return measurer.measure_text(
            self.value, self.style.font_size, self.style.font_weight or "normal"
        )


class ProgressBar(VisualComponent):
    def __init__(
        self,
        progress: int,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.progress = progress

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        return Size(width=300, height=8)


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

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        return Size(width=300, height=40)


class Icon(VisualComponent):
    def __init__(
        self,
        svg_path: str,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.svg_path = svg_path

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        return Size(width=16, height=16)


class Badge(VisualComponent):
    def __init__(
        self,
        label: str,
        tone: str | None = None,
        icon: str | None = None,
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.label = label
        self.tone = tone
        self.icon = icon

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        text_size = measurer.measure_text(self.label, "caption", font_weight="600")
        tracking = math.ceil(len(self.label) * 0.3)
        icon_width = 16 + 4 if self.icon else 0
        return Size(
            width=text_size.width + tracking + 20 + icon_width,
            height=text_size.height + 12,
        )


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
        tone: str = "primary",
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.value = value
        self.max_value = max_value
        self.label = label
        self.icon = icon
        self.tone = tone

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        return Size(width=160, height=160)


class Divider(VisualComponent):
    def __init__(
        self,
        opacity: float = 0.4,
        orientation: str = "horizontal",
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.opacity = opacity
        self.orientation = orientation


class SparklineMetric(VisualComponent):
    def __init__(
        self,
        label: str,
        value: str | int | float,
        icon: str | None = None,
        series: Any | None = None,
        tone: str = "default",
        style: Style | None = None,
        constraints: Constraints | None = None,
    ):
        super().__init__(constraints, style)
        self.label = label
        self.value = value
        self.icon = icon
        self.series = series
        self.tone = tone

    def intrinsic_size(self, measurer: IntrinsicMeasurer) -> Size:
        return Size(width=230, height=88)
