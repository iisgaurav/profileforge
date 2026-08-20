# Changelog

## [1.0.0-rc1] - 2026-08-02 — Release Candidate

> **Status: Release Candidate** — This is the first public pre-release of ProfileForge.
> Community testing feedback is being collected before the final v1.0.0 promotion.
>
> 🔗 [GitHub Pre-Release](https://github.com/iisgaurav/profileforge/releases/tag/v1.0.0-rc1) _(placeholder — publish after tagging)_

### Summary

ProfileForge v1.0.0-rc1 marks the first feature-complete release candidate of the declarative
Python framework for building beautiful, animated GitHub profile dashboards. All core subsystems
have been implemented, tested, and verified against strict quality gates.

### What's Included

| Area | Details |
|------|---------|
| **Framework** | Declarative `Component` tree engine, two-pass Flex layout, SVG rendering pipeline |
| **Themes** | 17 built-in production themes (github-dark, github-light, dracula, nord, catppuccin-*, vercel, modern, minimal, apple, showcase) |
| **Widgets** | 11 registered widgets: hero, about, skills, expertise, experience, now, focus, roadmap, social, github\_stats, github\_languages, repositories, activity\_timeline |
| **Templates** | 9 persona starter templates: backend, frontend, student, minimal, opensource, ai-engineer, indie-hacker, open-source-maintainer, security-engineer |
| **Studio** | ProfileForge Studio (`web/index.html`) — visual live preview and YAML editor |
| **Gallery** | Full gallery export pipeline (`profileforge gallery export`) generating 134 SVG assets |
| **Benchmarks** | Multi-stage performance benchmark service with `budget.yaml` gate (<15ms mean total build) |
| **Governance** | `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`, RFC Process, ADRs (5) |
| **Brand** | Full brand system: logo, wordmark, banner, favicon, icon, color palette, typography, voice guide |
| **Launch Assets** | 14 launch assets: Product Hunt, HackerNews, Reddit, Twitter thread, LinkedIn, YouTube, Instagram, FAQ, press kit |
| **Docs** | Widget Authoring Guide, Theme System, ADR index, comparison matrix, RFC Process, Release Guide, community docs (10 files) |
| **Good First Issues** | 10 curated good-first-issues for new contributors |

### Quality Gate Results (RC1 Verification Pass)

| Gate | Result |
|------|--------|
| Unit & Integration Tests (63 tests) | ✅ PASS |
| Code Linting & Formatting (ruff) | ✅ PASS |
| Public API Lock Check | ✅ PASS |
| Performance Budget Gate | ✅ PASS |
| ADR Index & Consistency | ✅ PASS |
| Documentation QA & Link Check | ✅ PASS |

### Performance (RC1 Benchmark)

- **Total Build Mean**: 10.7ms (budget: 50ms) — _well within SLA_
- **Render Pass**: 7.3ms p95
- **Throughput**: 92.9 ops/sec
- **Peak Memory**: 0.18 MB

### Fixed in RC1 Verification Pass

- Fixed broken CLI command references in `docs/community/ROADMAP.md` and `docs/community/VISION.md`
  (future planned commands cited as current — updated to descriptive prose)
- Fixed GitHub GraphQL queries failing for private repositories by scoping with `ownerAffiliations: OWNER`.
- Fixed language widget rendering bug where the last repository language was incorrectly popped from data rows.
- Fixed `SecretStore` to natively support reading `.env` files locally and fallback gracefully to `PROFILEFORGE_PAT` and `GH_TOKEN`.
- Fixed CLI orchestration bug where connectors were missing from `BuildContext` registry, forcing widgets to use mock data.



## [1.0.0] - 2026-08-02

### Highlights
- Official production release of ProfileForge v1.0.0.
- High-performance declarative component tree engine for GitHub profile SVG generation.
- Full theme token design system with 17 built-in production themes.
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
