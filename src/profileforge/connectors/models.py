from __future__ import annotations

__layer__ = "Layer 6 — Connectors"

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class MetricSeries:
    label: str
    points: tuple[float, ...]


@dataclass(frozen=True)
class ProfileMetadata:
    joined_at: date | None = None
    last_active_at: datetime | None = None
