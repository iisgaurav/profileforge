from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Style:
    """Standardized styling properties for any component."""

    color: str | None = None
    background_color: str | None = None
    padding: int | None = None
    margin: int | None = None
    border_radius: int | None = None
    border_color: str | None = None
    font_size: int | None = None
    font_weight: str | None = None
    width: int | None = None
    height: int | None = None
