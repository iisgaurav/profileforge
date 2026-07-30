from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

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
    extends: Optional[str] = None

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
    options: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ProfileForgeConfig:
    version: int
    project_name: str
    project_title: str
    active_theme: str
    widgets: List[WidgetConfig]
    datasources_config: Dict[str, Any]
    outputs: Outputs

@dataclass
class DataRequest:
    resource: str
    options: Dict[str, Any] = field(default_factory=dict)
