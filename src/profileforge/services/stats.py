from profileforge.core.models import MetricsConfig


class ScoreCalculator:
    def __init__(self, config: MetricsConfig):
        self.config = config

    def calculate(self, stats: dict) -> float:
        if not self.config.enabled:
            return 0.0

        if self.config.strategy == "weighted_sum":
            weights = {
                "stars": 1.0,
                "commits": 0.5,
                "prs": 2.0,
                "issues": 1.5,
                "repos": 1.0,
                "followers": 0.5,
            }
            score = 0.0
            for key, weight in weights.items():
                if key in stats:
                    score += float(stats[key]) * weight
            return score

        return float(sum(stats.values())) if stats else 0.0
