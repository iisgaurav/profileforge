from typing import Any

try:
    import httpx
except ImportError:
    httpx = None

from profileforge.connectors.base import Connector
from profileforge.core.exceptions import ConnectorError
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_connector
from profileforge.core.secrets import SecretStore

from .models import GitHubLanguage, GitHubStats


@register_connector("github")
class GithubConnector(Connector):
    def fetch(self, request: DataRequest) -> Any:
        # Generic fetch if needed
        return None

    def get_stats(self, username: str) -> GitHubStats:
        if httpx is None:
            raise ConnectorError(
                "The 'github' connector requires httpx. "
                "Please install it with: pip install profileforge[github]"
            )

        token = SecretStore.get("GITHUB_TOKEN")
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ProfileForge",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            with httpx.Client(headers=headers, timeout=10.0) as client:
                # We do some basic REST calls if token is missing (rate limits apply)
                # Just get basic user info for demonstration, or GraphQL if possible.
                # Since REST doesn't easily give total PRs and total commits, we can do a search query.

                # 1. Commits
                commits_resp = client.get(
                    "https://api.github.com/search/commits",
                    params={"q": f"author:{username}"},
                    headers={
                        "Accept": "application/vnd.github.cloak-preview+json",
                        **headers,
                    },
                )
                commits = (
                    commits_resp.json().get("total_count", 0)
                    if commits_resp.status_code == 200
                    else 0
                )

                # 2. PRs
                prs_resp = client.get(
                    "https://api.github.com/search/issues",
                    params={"q": f"author:{username} type:pr"},
                )
                prs = (
                    prs_resp.json().get("total_count", 0)
                    if prs_resp.status_code == 200
                    else 0
                )

                # 3. Stars (Need to iterate over repos, or just fetch first page for simplicity)
                repos_resp = client.get(
                    f"https://api.github.com/users/{username}/repos?per_page=100"
                )
                stars = 0
                if repos_resp.status_code == 200:
                    repos = repos_resp.json()
                    stars = sum(repo.get("stargazers_count", 0) for repo in repos)

                return GitHubStats(stars=stars, prs=prs, commits=commits)
        except Exception as e:
            raise ConnectorError(f"Failed to fetch GitHub stats: {e}")

    def get_languages(self, username: str) -> list[GitHubLanguage]:
        if httpx is None:
            raise ConnectorError(
                "The 'github' connector requires httpx. "
                "Please install it with: pip install profileforge[github]"
            )

        token = SecretStore.get("GITHUB_TOKEN")
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ProfileForge",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            with httpx.Client(headers=headers, timeout=10.0) as client:
                repos_resp = client.get(
                    f"https://api.github.com/users/{username}/repos?per_page=100"
                )
                if repos_resp.status_code != 200:
                    return []

                repos = repos_resp.json()
                lang_counts = {}
                total_valid_repos = 0

                for repo in repos:
                    lang = repo.get("language")
                    if lang:
                        if lang == "Jupyter Notebook":
                            lang = "Python"

                        lang_counts[lang] = lang_counts.get(lang, 0) + 1
                        total_valid_repos += 1

                if total_valid_repos == 0:
                    return []

                # Calculate percentages
                languages = []
                for lang, count in lang_counts.items():
                    pct = (count / total_valid_repos) * 100
                    languages.append(
                        GitHubLanguage(name=lang, percentage=round(pct, 1))
                    )

                # Sort by percentage descending, take top 5
                languages.sort(key=lambda x: x.percentage, reverse=True)
                return languages[:5]

        except Exception as e:
            raise ConnectorError(f"Failed to fetch GitHub languages: {e}")
