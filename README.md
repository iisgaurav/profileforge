# ProfileForge

![CI](https://github.com/iisgaurav/profileforge/workflows/ProfileForge%20CI/badge.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

**ProfileForge** is an extensible Python UI framework that generates beautiful, crisp developer profile assets (like SVG dashboards for your GitHub README). Unlike typical monolithic scripts, ProfileForge uses a **declarative component system** (inspired by React/Flutter), typed design tokens, and an internal Flex-style layout engine.

## Why ProfileForge?
Most GitHub profile generators are massive scripts tied to one person's exact aesthetic. If you want to change the layout, you have to rewrite the rendering math.

ProfileForge solves this by introducing a **Flex-style layout engine** (`Row`, `Column`, `Padding`, `Badge`, `Card`) that compiles perfectly into SVG files. You write a YAML configuration, select a theme, and the engine handles the precise X/Y coordinate math, data fetching, and typography rendering.

## Built-in Themes
ProfileForge comes with native themes designed to perfectly blend into modern web apps and GitHub profiles, such as the `github-dark` theme which features a completely transparent background and system-native crisp fonts, making the SVGs look completely native to GitHub's UI.

## Installation

ProfileForge requires Python 3.9+.

```bash
pip install git+https://github.com/iisgaurav/profileforge.git
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

This generates gorgeous `.svg` files in your `assets/` directory.

## Configuration & Customization
Your project is driven by `profileforge.yaml`.

```yaml
version: 1
project:
  name: "Jane Doe"
themes:
  active: "github-dark" # Swap themes effortlessly without touching code
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

Edit the YAML data in the `config/` directory and run `profileforge build` to see the changes update instantly.

## Extensibility & Architecture
ProfileForge architecture:
1. **Widgets**: E.g. `ExpertiseWidget`, `RoadmapWidget`—they fetch data and build the layout tree.
2. **Layout Engine**: Traverses `Row`, `Column`, `Padding` and `Badge` abstractions to compute exact `x`, `y`, `width`, and `height`.
3. **Themes**: Built on first-class `ColorTokens`, `TypographyTokens`, and `SpacingTokens`.
4. **Renderer**: Transforms the computed Layout Tree into stunning, accessible SVGs.

For complete documentation on creating custom themes, building your own widgets, and continuous integration, see the [docs/](./docs/index.md) directory.
