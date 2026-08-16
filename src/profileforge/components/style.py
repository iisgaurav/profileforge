from __future__ import annotations

__layer__ = "Layer 3 — Components"

from dataclasses import dataclass
from typing import Union

from profileforge.core.models import HorizontalAlign, TypographyRole, VerticalAlign


@dataclass
class Constraints:
    """Universal constraints for any component."""

    min_width: int | None = None
    max_width: int | None = None
    preferred_width: int | None = None
    fill: bool = False


@dataclass
class Style:
    """Standardized styling properties for any component."""

    color: str | None = None
    background_color: str | None = None
    padding: int | None = None
    margin: int | None = None
    border_radius: int | None = None
    border_color: str | None = None
    font_size: Union[TypographyRole, int, None] = None
    font_weight: str | None = None
    max_lines: int | None = None
    overflow: str | None = None  # "wrap", "ellipsis", or "clip"

    width: int | str | None = None
    height: int | str | None = None

    variant: str | None = None
    state: str | None = None
    elevation: str | None = None

    justify: Union[HorizontalAlign, str, None] = None
    align: Union[HorizontalAlign, VerticalAlign, str, None] = None
    valign: Union[VerticalAlign, str, None] = None
