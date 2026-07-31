# ProfileForge

[![CI](https://github.com/iisgaurav/profileforge/workflows/ProfileForge%20CI/badge.svg)](https://github.com/iisgaurav/profileforge/actions)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/iisgaurav/profileforge/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?logo=github)](https://github.com/sponsors/iisgaurav)

**ProfileForge** is a declarative Python framework for building beautiful, themeable GitHub profile dashboards and SVG widgets.

Inspired by modern UI frameworks, it combines reusable components, a Flex-style layout engine, design tokens, and renderer abstractions to generate animated, accessible SVG dashboards.

## Preview

<div align="center">
  <picture>
    <img src="https://raw.githubusercontent.com/iisgaurav/iisgaurav/main/engine-config/assets/about.svg" alt="ProfileForge Hero Banner" width="100%" />
  </picture>

  <br />

  <picture>
    <img src="https://raw.githubusercontent.com/iisgaurav/iisgaurav/main/engine-config/assets/roadmap.svg" alt="Roadmap" width="100%">
  </picture>

  <br />

  <picture>
    <img src="https://raw.githubusercontent.com/iisgaurav/iisgaurav/main/engine-config/assets/expertise.svg" alt="Expertise" width="100%">
  </picture>
</div>

> *The preview above is generated entirely by ProfileForge from a YAML config. No SVG written by hand. Users compose multiple SVGs in their README for maximum flexibility.*

---

## Features

| Feature | Description |
|---|---|
| 🧩 **Declarative components** | Build layouts with `Card`, `Row`, `Column`, `Badge`, `ProgressBar` — React/Flutter style |
| 📐 **Flex-style layout engine** | Justify, align, fill — same mental model as CSS Flexbox |
| 🎨 **Design token system** | Themes define colors, typography, spacing, radius, and shadows as typed tokens |
| ✨ **Visual renderer** | SVG `<defs>` with linear gradients, glow filters, SMIL animations — no CSS |
| 🖥️ **Dashboard Engine** | Compose multi-widget dashboards with pluggable layout strategies (Bento, Grid, …) |
| 🏷️ **Multi-color badges** | Tech badges auto-assigned from a curated 8-color palette |
| 🚀 **CLI-first workflow** | `profileforge build` regenerates your entire profile in milliseconds |
| ♿ **Accessibility built-in** | `<title>`, `<desc>`, ARIA roles on every component |
| 🔬 **Snapshot-tested** | Visual regression caught by pytest before any push |
| ⚙️ **GitHub Actions CI** | Multi-version matrix (Python 3.9 → 3.12) on every commit |

---

## Why ProfileForge?

Most GitHub profile generators are massive scripts tied to one person's exact aesthetic. Changing the layout means rewriting raw SVG math.

ProfileForge separates **data from presentation**:

```
You write YAML → ProfileForge handles layout math, theming, and SVG generation
```

It works the same way React/Flutter do: you declare *what* you want, not *how* to draw it.

---

## Installation

Requires Python 3.9+.

```bash
pip install git+https://github.com/iisgaurav/profileforge.git
```

For local development:

```bash
git clone https://github.com/iisgaurav/profileforge.git
cd profileforge
pip install -e .
```

---

## Quick Start

**1. Create your config directory:**

```bash
mkdir my-profile && cd my-profile
mkdir -p engine-config/config engine-config/assets
```

**2. Create `engine-config/profileforge.yaml`:**

```yaml
version: 1
project:
  name: "Your Name"
themes:
  active: "github-dark"
datasources:
  local:
    root: "./engine-config/config"
outputs:
  svg:
    enabled: true
    dir: "engine-config/assets"
widgets:
  - name: about
  - name: roadmap
  - name: expertise
```

**3. Add your data:**

`engine-config/config/roadmap.yaml`:
```yaml
- skill: Python
  progress: 95
- skill: System Design
  progress: 88
- skill: Cloud Architecture
  progress: 82
```

`engine-config/config/expertise.yaml`:
```yaml
- "Python"
- "FastAPI"
- "Docker"
- "PostgreSQL"
- "Redis"
- "AWS"
```

**4. Build:**

```bash
profileforge build --config engine-config/profileforge.yaml
```

```
  + Loaded configuration
  + Loaded theme "github-dark"
  + Registered 3 widgets
  + Generated about.svg
  + Generated roadmap.svg
  + Generated expertise.svg

Done.
```

**5. Embed in your GitHub profile README:**

```markdown
<div align="center">
  <picture>
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_USERNAME/main/engine-config/assets/about.svg" alt="ProfileForge Hero Banner" width="100%" />
  </picture>

  <br />

  <picture>
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_USERNAME/main/engine-config/assets/roadmap.svg" alt="Roadmap" width="100%">
  </picture>

  <br />

  <picture>
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_USERNAME/main/engine-config/assets/expertise.svg" alt="Expertise" width="100%">
  </picture>
</div>
```

---

## Architecture

```text
profileforge.yaml + config/*.yaml
         │
         ▼
   ConfigLoader  ──────────────────── ThemeLoader
         │                                 │
         ▼                                 ▼
   DataSources                         Theme (tokens)
         │                                 │
         ▼                                 ▼
    Widget.build()  ─────────────►  Component Tree
    (per widget)                   (Card, Row, Column…)
                                         │
                                         ▼
                                   LayoutEngine
                               (computed x, y, w, h)
                                         │
                                         ▼
                                   SVGRenderer
                             (defs, gradients, animation)
                                         │
                                         ▼
                                widget_name.svg
```

---

## Component Model

Widgets build a **declarative component tree** — no SVG written directly:

```python
from profileforge.components.layout import Column, Padding, Row
from profileforge.components.widgets import Badge, Card, ProgressBar, Text
from profileforge.components.style import Style

Card(
    title="Tech Stack",
    child=Padding(
        value=20,
        child=Column(
            children=[
                Row(children=[Badge("Python"), Badge("FastAPI")], spacing=10),
                Row(children=[Badge("Docker"), Badge("Redis")], spacing=10),
            ],
            spacing=10,
        ),
    ),
    style=Style(width=480, height=380),
)
```

The layout engine resolves all `x`, `y`, `width`, `height` values. The SVG renderer paints the result with gradients, animations, and filters — automatically.

---

## Visual System

ProfileForge's renderer uses SVG `<defs>` to deliver a rich visual output:

| Element | Implementation |
|---|---|
| Progress bar fill | `<linearGradient>` (primary → accent) + SMIL `<animate>` (fills on load) |
| Progress bar glow | `<feGaussianBlur>` filter composited over fill |
| Badge background | Per-index gradient from 8-color tech palette |
| Badge border | Matching fg color at 50% opacity |
| Card border | `<linearGradient>` from primary (top-left) → border (bottom-right) |
| Card shadow | `<feDropShadow>` filter |
| Card header | Left accent bar + title + thin separator line |

---

## Themes

Themes are YAML files with typed design tokens. The included `github-dark` theme is optimized for GitHub's dark mode:

```yaml
name: "github-dark"
mode: "dark"
colors:
  primary:    "#58A6FF"   # GitHub blue
  accent:     "#D2A8FF"   # Purple
  text:       "#C9D1D9"
  muted:      "#8B949E"
  surface:    "#0D1117"
  border:     "#30363D"
typography:
  font_family: "Inter, -apple-system, sans-serif"
  heading: 18
  body: 14
  small: 12
radius:
  card: 10
  progress: 4
```

---

## Quality & Testing

```bash
# Lint and format
ruff check src/ tests/
ruff format src/ tests/

# Tests
pytest tests/ -v

# CI matrix: Python 3.9, 3.10, 3.11, 3.12
```

- Snapshot testing catches any visual regression before push
- All SVG output validated as well-formed XML
- Accessibility roles (`aria-*`, `<title>`, `<desc>`) on every component

---

## Roadmap

- ✅ Declarative component system (`Card`, `Row`, `Column`, `Badge`, `ProgressBar`, `Wrap`)
- ✅ Flex-style layout engine with justify / align / fill
- ✅ Design token system (colors, typography, spacing, radius, shadows)
- ✅ SVG renderer with gradients, glow filters, SMIL animations
- ✅ Multi-SVG Engine (v0.2) — Individual modular widgets for maximum composition flexibility
- ✅ Multi-color badge palette (8-color tech-specific scheme)
- ✅ GitHub Camo compatible output (valid XML, proper SVG root)
- 🚧 Auto-wrapping tag flows and badge grids
- 🚧 Widget-level color overrides (`color:` in YAML)
- 🚧 Plugin API for custom widgets
- 🚧 HTML / PNG renderer
- 🚧 Theme marketplace

---

## Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Ensure `ruff check` and `pytest` pass
4. Open a pull request

Please read `CONTRIBUTING.md` before your first PR.

---

## License

MIT License — free for personal and commercial use.

---

<div align="center">
  <sub>Built with ❤️ using ProfileForge · <a href="https://github.com/sponsors/iisgaurav">Sponsor the project</a></sub>
</div>
