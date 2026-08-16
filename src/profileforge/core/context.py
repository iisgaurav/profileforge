__layer__ = "Layer 1 — Core"
from dataclasses import dataclass, field
from typing import Any

from profileforge.core.models import (
    ProfileForgeConfig,
    RenderContext,
    RendererCapabilities,
    ResolvedTheme,
    Theme,
)


@dataclass
class Services:
    connectors: dict[str, Any] = field(default_factory=dict)  # str -> Connector
    # renderer: Renderer will be injected later


@dataclass
class BuildContext:
    theme: Theme
    config: ProfileForgeConfig
    services: Services
    cache: dict[str, Any] = field(default_factory=dict)

    def get_render_context(self) -> RenderContext:
        resolved_theme = ResolvedTheme(
            colors=self.theme.colors,
            typography=self.theme.typography,
            spacing=self.theme.spacing,
            radius=self.theme.radius,
            shadows=self.theme.shadows,
            motion=self.theme.motion,
            effects=self.theme.effects,
        )
        return RenderContext(
            theme=resolved_theme,
            typography=self.theme.typography,
            spacing=self.theme.spacing,
            effects=self.theme.effects,
            renderer="svg",
            api_version=1,
            capabilities=RendererCapabilities(
                supports_gradients=True,
                supports_filters=True,
                supports_animation=True,
                supports_masks=True,
                supports_fonts=True,
                supports_accessibility=True,
            ),
        )
