from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Theme:
    name: str
    background: str
    primary: str
    secondary: str
    text: str
    text_muted: str
    border: str
    progress_bg: str
    extends: str | None = None


@dataclass
class OutputConfig:
    enabled: bool = False
    dir: str = ""


@dataclass
class Outputs:
    svg: OutputConfig = field(default_factory=OutputConfig)
    markdown: OutputConfig = field(default_factory=OutputConfig)
    png: OutputConfig = field(default_factory=OutputConfig)


@dataclass
class WidgetConfig:
    name: str
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfileForgeConfig:
    version: int
    project_name: str
    project_title: str
    active_theme: str
    widgets: list[WidgetConfig]
    datasources_config: dict[str, Any]
    outputs: Outputs


@dataclass
class DataRequest:
    resource: str
    options: dict[str, Any] = field(default_factory=dict)
