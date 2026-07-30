from __future__ import annotations

from dataclasses import dataclass

from profileforge.core.models import (
    DashboardFooterConfig,
    DashboardHeaderConfig,
    GridConfig,
)
from profileforge.widgets.base import Widget


@dataclass
class DashboardItem:
    widget: Widget
    grid: GridConfig


@dataclass
class Dashboard:
    title: str
    subtitle: str | None
    items: list[DashboardItem]
    header: DashboardHeaderConfig
    footer: DashboardFooterConfig
