from dataclasses import dataclass


@dataclass
class GitHubStats:
    stars: int
    prs: int
    commits: int
