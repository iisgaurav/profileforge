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

from .models import GitHubStats


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
