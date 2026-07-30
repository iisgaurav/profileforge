from dataclasses import dataclass, field
from typing import Dict, Any
from profileforge.core.models import Theme, ProfileForgeConfig

@dataclass
class Services:
    datasources: Dict[str, Any] = field(default_factory=dict) # str -> DataSource
    # renderer: Renderer will be injected later

@dataclass
class BuildContext:
    theme: Theme
    config: ProfileForgeConfig
    services: Services
    cache: Dict[str, Any] = field(default_factory=dict)
