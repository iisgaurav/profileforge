from dataclasses import dataclass, field
from typing import Any

from profileforge.core.models import ProfileForgeConfig, Theme


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
