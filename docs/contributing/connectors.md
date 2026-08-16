# Submit a Connector

Connectors are data source adapters that fetch external data (from APIs, RSS feeds, local files, etc.) and standardize it for widgets to consume.

## The Connector Interface

All connectors must inherit from `BaseConnector` and implement the `fetch` method.

```python
from profileforge.connectors.base import BaseConnector, DataRequest
from typing import Any

class MyApiConnector(BaseConnector):
    def fetch(self, request: DataRequest) -> Any:
        """
        Fetch data based on the request parameters.
        Must handle retries, rate limits, and timeouts.
        """
        pass
```

## Location

Place your connector in `src/profileforge/connectors/`.

## Secrets and Authentication

- **NEVER hardcode credentials.**
- Use environment variables to retrieve tokens (e.g., `os.environ.get("GITHUB_TOKEN")`).
- Clearly document required environment variables in your connector's docstring and the global documentation.

## Rate Limiting and Retries

Your connector must handle network flakiness. Use built-in retry decorators or implement exponential backoff logic.
If the API returns a rate-limit error (e.g., HTTP 429), your connector should log a warning and return cached/fallback data if possible, or raise a structured `ConnectorRateLimitException`.

## Unit Test Requirements

- You must mock all HTTP requests in your tests. **Do not make live network calls in CI.**
- Use `responses` or `unittest.mock.patch` to simulate API success, timeout, and 4xx/5xx errors.
- Verify that your connector handles bad JSON gracefully.

## PR Checklist

- [ ] Inherits `BaseConnector`.
- [ ] Implements `fetch()`.
- [ ] Uses environment variables for secrets.
- [ ] Handles timeouts and rate limits.
- [ ] 100% test coverage with mocked HTTP responses.
- [ ] Docstrings explain the data format returned.
