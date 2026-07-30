# ProfileForge

![CI](https://github.com/iisgaurav/profileforge/workflows/ProfileForge%20CI/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

**ProfileForge** is a declarative Python framework for building beautiful, themeable GitHub profile dashboards and SVG widgets. 

Inspired by modern UI frameworks, it combines reusable components, a Flex-style layout engine, design tokens, and renderer abstractions to generate accessible SVG assets.

## Preview

<div align="center">
  <img src="https://raw.githubusercontent.com/iisgaurav/iisgaurav/main/engine-config/assets/dashboard.svg?v=20260731005400" alt="ProfileForge Dashboard Preview" width="100%"/>
</div>

## Features

- **Declarative component architecture** (React/Flutter style)
- **Flex-style layout engine** (`Row`, `Column`, `Padding`)
- **Theme engine with design tokens**
- **Accessible SVG rendering**
- **CLI-first workflow**
- **YAML configuration**
- **Built-in themes** (e.g., `github-dark` for native transparent blending)
- **Extensible widget system**
- **Snapshot-tested rendering**
- **GitHub Actions friendly**

## Why ProfileForge?

Most GitHub profile generators are massive scripts tied to one person's exact aesthetic. If you want to change the layout, you have to rewrite the raw SVG generation math.

ProfileForge solves this by separating data from presentation. You write a YAML configuration, select a theme, and the internal layout engine handles the precise X/Y coordinate math, data fetching, and typography rendering automatically.

## Installation

ProfileForge requires Python 3.9+.

```bash
pip install git+https://github.com/iisgaurav/profileforge.git
```

For local development and contributing:

```bash
git clone https://github.com/iisgaurav/profileforge.git
cd profileforge
pip install -e .
```

## Quick Start (Under 5 Minutes)

Scaffold your first profile using the CLI:

```bash
# 1. Create a new project directory
profileforge new my-profile
cd my-profile

# 2. Build the default configuration
profileforge build
```

This generates the profile assets:

```bash
✓ Generated roadmap.svg
✓ Generated expertise.svg
```

## Architecture

ProfileForge pipelines configuration and data into a layout tree, which is ultimately painted by the renderer.

```text
YAML Configuration
        │
        ▼
   Data Sources
        │
        ▼
     Widgets
        │
        ▼
  Component Tree
        │
        ▼
  Layout Engine
        │
        ▼
 Resolved Layout
        │
        ▼
    Renderer
        │
        ▼
   SVG Assets
```

## Component Model

Widgets don't generate SVG strings directly. Instead, they build a declarative component tree using UI primitives.

```python
Card(
    title="Learning",
    child=Column(
        children=[
            ProgressBar(progress=95),
            ProgressBar(progress=80),
        ],
        spacing=8,
    ),
)
```

The layout engine traverses this tree to compute absolute positioning, and the renderer paints the final SVG.

## Configuration

Your project is driven by `profileforge.yaml`. Edit the data in your local directory and run `profileforge build` to update your UI.

```yaml
version: 1
project:
  name: "Jane Doe"
themes:
  active: "github-dark"
datasources:
  local:
    root: "./config"
widgets:
  - roadmap
  - expertise
outputs:
  svg:
    enabled: true
    dir: "assets"
```

## Quality & Testing

ProfileForge enforces strict engineering discipline:

- Pytest test suite
- Snapshot testing for UI regression
- Ruff linting & formatting
- GitHub Actions CI pipeline
- Accessibility checks built into SVGs

## Roadmap

- ✅ Declarative component system
- ✅ SVG renderer
- ✅ Design tokens
- 🚧 Plugin API
- 🚧 HTML renderer
- 🚧 Third-party themes

## Documentation

For complete guidance, see the `/docs` directory:
- Getting Started
- Configuration
- Theme Development
- Widget Development
- Architecture
- CLI Reference

## Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` before opening a pull request.

## License

MIT License
