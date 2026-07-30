from dataclasses import dataclass
from typing import Optional

@dataclass
class Style:
    """Standardized styling properties for any component."""
    color: Optional[str] = None
    background_color: Optional[str] = None
    padding: Optional[int] = None
    margin: Optional[int] = None
    border_radius: Optional[int] = None
    border_color: Optional[str] = None
    font_size: Optional[int] = None
    font_weight: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
