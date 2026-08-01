# ADR-004: Pluggable Connector Architecture and Data Abstraction

## Status
**Accepted** (2026-08-02)

## Context & Problem Statement
ProfileForge widgets need data from diverse external and local sources:
- GitHub GraphQL and REST APIs (user profile stats, starred repos, top languages, PR activity).
- Local configuration files (e.g. `about.yaml`, `roadmap.yaml`, custom project highlights).
- Future integrations (WakaTime, LeetCode, Spotify, Dev.to, RSS feeds).

If widgets perform direct HTTP calls (via `requests`, `httpx`, or `urllib`) directly within their rendering logic:
1. **Network Fragility in Tests**: Unit tests cannot run offline or without live API credentials.
2. **Duplicate Network Calls**: Multiple widgets requesting the same upstream API data make duplicate network requests.
3. **No Centralized Rate Limiting & Auth**: Token expiration, header injection, and rate limiting become duplicated across widgets.
4. **Tight Coupling**: Widgets become tightly bound to specific API payload structures.

## Decision
We decided to introduce a **Pluggable Connector Architecture** (Layer 6).

Key elements of this decision:
1. **Abstract Connector Interface**: A base `Connector` class with a standardized `fetch(request: DataRequest) -> Any` method.
2. **DataRequest Model**: A normalized request descriptor encapsulating resource names, query parameters, and options.
3. **Built-in Connectors**:
   - `GitHubConnector`: Encapsulates GitHub GraphQL/REST communication, personal access token resolution, in-memory caching, and rate-limit backoff.
   - `LocalConnector`: Resolves local YAML/JSON project files relative to the working directory with path safety validation.
4. **Service Container (`Services`)**: Connectors are instantiated and injected into `BuildContext.services.connectors` at CLI initialization.
5. **Declarative Connector Requirements**: Widgets declare their required connector dependencies in `WidgetMetadata.required_connectors` (e.g., `["github"]` or `["local"]`).

```python
# Example connector interaction inside widget lifecycle:
def fetch(self, context: BuildContext) -> Any:
    connector = context.services.connectors.get("github")
    if not connector:
        return None
    request = DataRequest(
        resource="user_stats", options={"username": context.config.project_name}
    )
    return connector.fetch(request)
```

## Consequences

### Positive
- **Hermetic Testing**: Tests can mock connectors cleanly in `BuildContext.services` without monkey-patching HTTP libraries.
- **Centralized Security**: API tokens and secrets (`GITHUB_TOKEN`) are resolved once in the connector layer, keeping widgets free of credential logic.
- **Shared Caching**: Connectors can cache expensive API responses across multiple widgets in the same build pass.

### Negative / Trade-offs
- **Indirection**: Widget authors interact with connectors rather than making raw HTTP calls. Clear documentation in `docs/WIDGET_AUTHORING.md` provides copy-paste examples.
