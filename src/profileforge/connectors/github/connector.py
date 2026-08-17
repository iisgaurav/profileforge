__layer__ = "Layer 6 — Connectors"
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

        token = (
            SecretStore.get("GITHUB_TOKEN")
            or SecretStore.get("PROFILEFORGE_PAT")
            or SecretStore.get("GH_TOKEN")
            or SecretStore.get("PAT")
        )
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

                stars = 0
                total_repos = 0

                # 3. Stars & Repos (Prefer GraphQL if token exists to get private repos reliably)
                if token:
                    gql_query = """
                    query($username: String!) {
                        user(login: $username) {
                            repositories(ownerAffiliations: OWNER, first: 100) {
                                totalCount
                                nodes {
                                    stargazerCount
                                }
                            }
                            contributionsCollection {
                                restrictedContributionsCount
                            }
                        }
                    }
                    """
                    gql_resp = client.post(
                        "https://api.github.com/graphql",
                        json={"query": gql_query, "variables": {"username": username}},
                    )
                    if gql_resp.status_code == 200:
                        data = gql_resp.json().get("data", {}).get("user", {})
                        repos_data = data.get("repositories", {})
                        total_repos = repos_data.get("totalCount", 0)
                        stars = sum(
                            node.get("stargazerCount", 0)
                            for node in repos_data.get("nodes", [])
                        )
                        commits += data.get("contributionsCollection", {}).get(
                            "restrictedContributionsCount", 0
                        )

                # Fallback to REST if GraphQL failed or no token
                if total_repos == 0:
                    repos_list_resp = client.get(
                        f"https://api.github.com/users/{username}/repos?per_page=100"
                    )
                    if repos_list_resp.status_code == 200:
                        repos_list = repos_list_resp.json()
                        stars = sum(
                            repo.get("stargazers_count", 0) for repo in repos_list
                        )

                    repos_search_resp = client.get(
                        "https://api.github.com/search/repositories",
                        params={"q": f"owner:{username}"},
                    )
                    if repos_search_resp.status_code == 200:
                        total_repos = repos_search_resp.json().get("total_count", 0)

                return GitHubStats(
                    stars=stars, prs=prs, commits=commits, repos=total_repos
                )
        except Exception as e:
            raise ConnectorError(f"Failed to fetch GitHub stats: {e}")

    def get_repositories(self, username: str) -> list[GitHubRepository]:
        if httpx is None:
            raise ConnectorError(
                "The 'github' connector requires httpx. "
                "Please install it with: pip install profileforge[github]"
            )

        token = (
            SecretStore.get("GITHUB_TOKEN")
            or SecretStore.get("PROFILEFORGE_PAT")
            or SecretStore.get("GH_TOKEN")
            or SecretStore.get("PAT")
        )
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
                            repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: PUSHED_AT, direction: DESC}) {
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
