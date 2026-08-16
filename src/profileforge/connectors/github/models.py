from __future__ import annotations

__layer__ = "Layer 6 — Connectors"

from dataclasses import dataclass, field

from profileforge.connectors.models import MetricSeries, ProfileMetadata


@dataclass
class GitHubStats:
    stars: int
    prs: int
    commits: int
    repos: int = 0
    stars_series: MetricSeries | None = None
    prs_series: MetricSeries | None = None
    commits_series: MetricSeries | None = None
    repos_series: MetricSeries | None = None
    profile_metadata: ProfileMetadata | None = None


@dataclass
class GitHubLanguage:
    name: str
    percentage: float


@dataclass
class GitHubLanguageStats:
    name: str
    bytes: int


@dataclass
class GitHubRepository:
    name: str
    stars: int
    primary_language: str | None
    languages: list[GitHubLanguageStats] = field(default_factory=list)
    description: str = ""
    forks: int = 0
