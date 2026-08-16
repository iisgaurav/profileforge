from __future__ import annotations

__layer__ = "Layer 1 — Core"

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union


class HorizontalAlign(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlign(Enum):
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"
    BASELINE = "baseline"


class PercentageDisplay(Enum):
    NONE = "none"
    RIGHT = "right"
    TOP = "top"
    INSIDE = "inside"


class ThemeSize(Enum):
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"


@dataclass(frozen=True)
class Size:
    width: int
    height: int


class TypographyRole(Enum):
    TITLE = "title"
    HEADING = "heading"
    LABEL = "label"
    VALUE = "value"
    BODY = "body"
    CAPTION = "caption"


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
    # Semantic rendering tokens.  They are resolved by ConfigLoader for legacy
    # themes, so every rendered surface has an intentional foreground colour.
    hero_surface: str | None = None
    hero_on_surface: str | None = None
    badge_primary: str | None = None
    badge_secondary: str | None = None
    badge_success: str | None = None
    badge_info: str | None = None
    badge_warning: str | None = None
    badge_neutral: str | None = None
    progress_start: str | None = None
    progress_end: str | None = None


@dataclass
class TypographyTokens:
    font_family: str
    title: int = 24
    heading: int = 18
    label: int = 14
    value: int = 28
    body: int = 15
    caption: int = 13
    small: int = 12


@dataclass
class OpticalSpacingTokens:
    text_icon: int = 10
    label_value: int = 6
    badge_icon: int = 8


@dataclass
class SpacingTokens:
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
    card_padding: int = 24
    inline_gap: int = 10
    section_gap: int = 18
    group_gap: int = 24
    optical: OpticalSpacingTokens = field(default_factory=OpticalSpacingTokens)


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
    schema: int = 1
    id: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    extends: Optional[str] = None
    author: Optional[str] = None
    version: Optional[str] = None
    license: Optional[str] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    animations: Optional[dict[str, Any]] = None
    icons: Optional[dict[str, Any]] = None
    fonts: Optional[dict[str, Any]] = None
    assets: Optional[dict[str, Any]] = None
    variables: Optional[dict[str, Any]] = None


@dataclass
class RendererCapabilities:
    supports_gradients: bool = True
    supports_filters: bool = True
    supports_animation: bool = True
    supports_masks: bool = True
    supports_fonts: bool = True
    supports_accessibility: bool = True


@dataclass
class ResolvedTheme:
    colors: ColorTokens
    typography: TypographyTokens
    spacing: SpacingTokens
    radius: RadiusTokens
    shadows: ShadowTokens
    motion: MotionTokens
    effects: EffectsTokens


@dataclass
class RenderContext:
    theme: ResolvedTheme
    typography: TypographyTokens
    spacing: SpacingTokens
    effects: EffectsTokens
    renderer: str = "svg"
    api_version: int = 1
    capabilities: RendererCapabilities = field(default_factory=RendererCapabilities)


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
