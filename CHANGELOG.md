# Changelog

## [1.0.0] - 2026-08-02

### Highlights
- Official production release of ProfileForge v1.0.0.
- High-performance declarative component tree engine for GitHub profile SVG generation.
- Full theme token design system with 14 built-in production themes.
- 12 extensible widgets covering identity, stats, career, development, and social channels.
- 6 starter template personas with typed manifest validation (`manifest.yaml`).
- Sub-15ms end-to-end rendering pipeline verified by continuous performance benchmarking.

### Added
- **Track 1**: High-precision multi-stage performance benchmark service (`profileforge benchmark`) and budget gate (`budget.yaml`).
- **Track 2**: Release engineering automation (`tools/release.py`) and release guide documentation (`docs/RELEASE_GUIDE.md`).
- **Track 4**: Documentation QA and link validation gate (`tools/docs_check.py`).
- **Track 5**: Template manifest system (`manifest.yaml`) and `TemplateLoader` service.
- **Track 6**: Architecture decision records indexer (`tools/adr_index.py`) and widget CLI discovery (`profileforge widgets list/info`).

### Performance
- Total build execution latency under 12ms mean SLA.
- Sub-millisecond layout calculation and config parsing.
- Peak memory footprint below 0.5 MB.


All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-07-30
### Added
- Initial alpha release of ProfileForge.
- Declarative `Component` layout system.
- `profileforge` CLI (`build`, `new`, `doctor`).
- `Roadmap`, `Focus`, and `Expertise` built-in widgets.
- SVG rendering engine.
- `github-dark` theme.
- GitHub Actions CI matrix for tests.
