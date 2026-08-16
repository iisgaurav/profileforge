__layer__ = "Layer 8 — CLI"
from dataclasses import dataclass
from typing import Sequence

from profileforge.connectors.github.models import GitHubRepository


@dataclass
class AggregatedLanguage:
    name: str
    percentage: float
    repo_count: int


class LanguageNormalizer:
    # A simple mapping for known name variations
    MAPPING = {
        "Jupyter Notebook": "Python",
    }

    @classmethod
    def normalize(cls, name: str) -> str:
        return cls.MAPPING.get(name, name)


class LanguageAggregator:
    @staticmethod
    def aggregate(
        repos: Sequence[GitHubRepository], ignore: list[str] = None
    ) -> tuple[list[AggregatedLanguage], bool]:
        """
        Aggregates languages from repositories.
        Returns a tuple of (sorted_languages, is_estimated).
        """
        if ignore is None:
            ignore = []
        ignore_lower = {i.lower() for i in ignore}

        lang_bytes = {}
        lang_repos = {}

        is_estimated = True

        for repo in repos:
            repo_langs_seen = set()
            for lang_stat in repo.languages:
                normalized_name = LanguageNormalizer.normalize(lang_stat.name)

                if normalized_name.lower() in ignore_lower:
                    continue

                if lang_stat.bytes > 1:
                    is_estimated = False

                lang_bytes[normalized_name] = (
                    lang_bytes.get(normalized_name, 0) + lang_stat.bytes
                )
                if normalized_name not in repo_langs_seen:
                    lang_repos[normalized_name] = lang_repos.get(normalized_name, 0) + 1
                    repo_langs_seen.add(normalized_name)

        total_bytes = sum(lang_bytes.values())

        aggregated = []
        if total_bytes > 0:
            for name, bytes_count in lang_bytes.items():
                pct = (bytes_count / total_bytes) * 100
                aggregated.append(
                    AggregatedLanguage(
                        name=name,
                        percentage=round(pct, 1),
                        repo_count=lang_repos.get(name, 0),
                    )
                )

        # Sort by percentage descending
        aggregated.sort(key=lambda x: x.percentage, reverse=True)
        return aggregated, is_estimated
