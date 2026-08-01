from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class ColorTokens:
    primary: str
    secondary: str
    background: str
    surface: str
    border: str
    text: str
    muted: str
    success: str
    warning: str
    info: str
    accent: str


@dataclass
class TypographyTokens:
    font_family: str
    heading: int
    body: int
    small: int


@dataclass
class SpacingTokens:
    xs: int
    sm: int
    md: int
    lg: int
    xl: int


@dataclass
class RadiusTokens:
    card: int
    progress: int
    badge: int


@dataclass
class ShadowTokens:
    none: str
    low: str
    medium: str
    high: str


@dataclass
class MotionTokens:
    duration_fast: int
    duration_normal: int
    duration_slow: int
    easing: str


@dataclass
class EffectsTokens:
    glow: str
    shadow: str
    glass: str


@dataclass
class Theme:
    name: str
    mode: str  # "minimal", "modern", "showcase"
    colors: ColorTokens
    typography: TypographyTokens
    spacing: SpacingTokens
    radius: RadiusTokens
    shadows: ShadowTokens
    motion: MotionTokens
    effects: EffectsTokens
    extends: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    license: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None


@dataclass
class OutputConfig:
    enabled: bool = False
    dir: str = ""
    animations: bool = False
    width: Union[int, str] = 420
    height: Union[int, str] = "auto"


@dataclass
class Outputs:
    svg: OutputConfig = field(default_factory=OutputConfig)
    markdown: OutputConfig = field(default_factory=OutputConfig)
    png: OutputConfig = field(default_factory=OutputConfig)


@dataclass
class GridConfig:
    width: int = 1
    height: int = 1


@dataclass
class WidgetConfig:
    name: str
    options: dict[str, Any] = field(default_factory=dict)
    grid: GridConfig = field(default_factory=GridConfig)


@dataclass
class DashboardHeaderConfig:
    enabled: bool = True


@dataclass
class DashboardFooterConfig:
    enabled: bool = False
    text: str = "Powered by ProfileForge"


@dataclass
class DashboardConfig:
    enabled: bool = False
    layout: str = "bento"
    title: str = ""
    subtitle: Optional[str] = None
    header: DashboardHeaderConfig = field(default_factory=DashboardHeaderConfig)
    footer: DashboardFooterConfig = field(default_factory=DashboardFooterConfig)


@dataclass
class MetricsConfig:
    enabled: bool = True
    strategy: str = "weighted_sum"


@dataclass
class ProfileForgeConfig:
    version: int
    project_name: str
    project_title: str
    active_theme: str
    widgets: list[WidgetConfig]
    connectors_config: dict[str, Any]
    outputs: Outputs
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)
    metrics: MetricsConfig = field(default_factory=MetricsConfig)


@dataclass
class DataRequest:
    resource: str
    options: dict[str, Any] = field(default_factory=dict)
