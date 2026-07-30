# ProfileForge

![CI](https://github.com/profileforge/profileforge/workflows/ProfileForge%20CI/badge.svg)
![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)

**ProfileForge** is an extensible Python framework that generates developer profile assets (like SVG dashboards for your GitHub README) through a declarative component system, typed models, dependency injection, and a rendering pipeline.

## Why ProfileForge?
Most GitHub profile generators are massive, monolithic scripts tied to one person's exact preferences. If you want to change the layout, you have to rewrite the rendering math.

ProfileForge solves this by introducing a **declarative component engine** (similar to React or Flutter) that compiles into SVG files. You write a YAML configuration, and the engine handles the layout math, data fetching, and theme injection.

## What does the output look like?
ProfileForge compiles your config into polished, responsive SVGs.

*(Insert example screenshot of generated dashboard here)*

## Installation

ProfileForge requires Python 3.9+.

```bash
pip install profileforge
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

This generates `.svg` files in your `assets/` directory.

## Configuration & Customization
Your project is driven by `profileforge.yaml`.

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

Edit the data in the `config/` directory and run `profileforge build` to see the changes update instantly.

## Documentation
For complete documentation on creating custom themes, building your own widgets, and continuous integration, see the [docs/](./docs/index.md) directory.
