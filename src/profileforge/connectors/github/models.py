from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class GitHubStats:
    stars: int
    prs: int
    commits: int


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
