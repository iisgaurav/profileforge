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

from .models import GitHubLanguageStats, GitHubRepository, GitHubStats


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

    def get_repositories(self, username: str) -> list[GitHubRepository]:
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
                if token:
                    # GraphQL
                    query = """
                    query($username: String!) {
                        user(login: $username) {
                            repositories(first: 100, isFork: false, orderBy: {field: PUSHED_AT, direction: DESC}) {
                                nodes {
                                    name
                                    description
                                    stargazerCount
                                    forkCount
                                    primaryLanguage {
                                        name
                                    }
                                    languages(first: 10) {
                                        edges {
                                            size
                                            node {
                                                name
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    """
                    resp = client.post(
                        "https://api.github.com/graphql",
                        json={"query": query, "variables": {"username": username}},
                    )

                    if resp.status_code == 200 and "errors" not in resp.json():
                        data = resp.json()
                        nodes = (
                            data.get("data", {})
                            .get("user", {})
                            .get("repositories", {})
                            .get("nodes", [])
                        )

                        repos = []
                        for node in nodes:
                            name = node.get("name", "")
                            description = node.get("description") or ""
                            stars = node.get("stargazerCount", 0)
                            forks = node.get("forkCount", 0)
                            primary_lang = node.get("primaryLanguage")
                            primary_language = (
                                primary_lang.get("name") if primary_lang else None
                            )

                            lang_stats = []
                            edges = node.get("languages", {}).get("edges", [])
                            for edge in edges:
                                size = edge.get("size", 0)
                                lang_name = edge.get("node", {}).get("name", "")
                                if lang_name and size > 0:
                                    lang_stats.append(
                                        GitHubLanguageStats(name=lang_name, bytes=size)
                                    )

                            repos.append(
                                GitHubRepository(
                                    name=name,
                                    stars=stars,
                                    primary_language=primary_language,
                                    languages=lang_stats,
                                    description=description,
                                    forks=forks,
                                )
                            )
                        return repos

                # Fallback to REST
                repos_resp = client.get(
                    f"https://api.github.com/users/{username}/repos?per_page=100"
                )
                if repos_resp.status_code != 200:
                    return []

                raw_repos = repos_resp.json()
                repos = []
                for repo in raw_repos:
                    name = repo.get("name", "")
                    description = repo.get("description") or ""
                    stars = repo.get("stargazers_count", 0)
                    forks = repo.get("forks_count", 0)
                    lang = repo.get("language")

                    lang_stats = []
                    if lang:
                        lang_stats.append(GitHubLanguageStats(name=lang, bytes=1))

                    repos.append(
                        GitHubRepository(
                            name=name,
                            stars=stars,
                            primary_language=lang,
                            languages=lang_stats,
                            description=description,
                            forks=forks,
                        )
                    )
                return repos

        except Exception as e:
            raise ConnectorError(f"Failed to fetch GitHub repositories: {e}")
