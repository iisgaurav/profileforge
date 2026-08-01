<div align="center">

# 🔥 ProfileForge

**Stop copy-pasting SVG templates. Forge your GitHub profile.**

Declarative, high-performance GitHub Profile & SVG Widget Engine — compose stunning animated dashboards in YAML, not strings.

[![CI](https://github.com/iisgaurav/profileforge/workflows/ProfileForge%20CI/badge.svg)](https://github.com/iisgaurav/profileforge/actions)
[![PyPI version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://pypi.org/project/profileforge/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Performance](https://img.shields.io/badge/throughput-100%2B%20ops%2Fsec-success)](budget.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ADRs](https://img.shields.io/badge/ADRs-5%20Indexed-purple)](docs/adr/)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?logo=github)](https://github.com/sponsors/iisgaurav)

> ⭐ **Star this repo if ProfileForge saves you time!**

[See It in Action](#%EF%B8%8F-see-it-before-you-build-it) •
[30-Second Start](#-build-in-30-seconds) •
[15 Widgets](#-widget-showcase) •
[9 Templates](#-persona-templates) •
[14 Themes](#-theme-gallery) •
[Studio App](#-profileforge-studio) •
[CLI Reference](#-cli-cheat-sheet)

</div>

---

## 🖼️ See It Before You Build It

<div align="center">

**Hero Widget** — Your identity, beautifully rendered:
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/hero_github-dark.svg" alt="Hero Widget — GitHub Dark Theme" width="820" />
</picture>

<br/>

**Skills Widget** — Categorized tech stack with color-coded badges:
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/skills_dracula.svg" alt="Skills Widget — Dracula Theme" width="820" />
</picture>

<br/>

**GitHub Stats Widget** — Commit velocity, stars & developer score:
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/github_stats_modern.svg" alt="GitHub Stats Widget — Modern Theme" width="820" />
</picture>

<br/>

**Featured Repositories** — Pinned projects with stars, forks, and language tags:
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/repositories_nord.svg" alt="Repositories Widget — Nord Theme" width="820" />
</picture>

<br/>

**Contribution Streak 🔥** — Real-time streak tracking with circular progress:
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/streak_dracula.svg" alt="Streak Widget — Dracula Theme" width="820" />
</picture>

</div>

---

## ⚡ Build in 30 Seconds

```bash
# 1. Install
pip install profileforge

# 2. Scaffold your profile (pick a persona)
profileforge new my-profile --template backend
cd my-profile

# 3. Build — SVGs land in assets/widgets/
profileforge build
```

That's it. Your animated SVG profile dashboard is ready to embed in your GitHub README.

---

## 📦 Installation Methods

| Method | Command | Best For |
|---|---|---|
| **pip (stable)** | `pip install profileforge` | Production use, CI/CD |
| **Scaffold + Build** | `profileforge new my-profile --template backend` | New projects, getting started fast |
| **ProfileForge Studio** | Open `./web/index.html` locally | Zero-config visual builder, no terminal |

### Use with GitHub Actions (auto-update on schedule)

```yaml
# .github/workflows/profile.yml
- name: Rebuild Profile SVGs
  run: |
    pip install profileforge
    profileforge build
    git add assets/ && git commit -m "chore: refresh profile svgs" && git push
```

---

## 🧩 Widget Showcase

ProfileForge ships **15 production-grade widgets** across 6 categories:

| Category | Widget ID | Description | Connector |
|---|---|---|---|
| **Identity** | `hero` | Prominent name, role, status badge, and location banner | `local` |
| **Identity** | `about` | Bio overview, focal tech stacks, and profile narrative | `local` |
| **Stats** | `github_stats` | Stars, PRs, commits, and overall developer ranking score | `github` |
| **Stats** | `github_languages` | Top programming languages breakdown with colored bars | `github` |
| **Stats** | `streak` | Current Streak 🔥, Longest Streak, Total Active Days | `local` |
| **Stats** | `achievements` | Unlocked achievements as bold badges, locked as muted | `local` |
| **Career** | `skills` | Categorized tech skills with curated color badges | `local` |
| **Career** | `experience` | Chronological career timeline and roles | `local` |
| **Career** | `expertise` | Domain specialties and proficiency ratings | `local` |
| **Projects** | `repositories` | Featured repos with stars, forks, and language tags | `github` |
| **Development** | `roadmap` | Active milestones, progress percentages, and target dates | `local` |
| **Development** | `now` | Derek Sivers-style: building, reading, learning, experimenting | `local` |
| **Development** | `focus` | Immediate weekly / monthly development priorities | `local` |
| **Development** | `activity_timeline` | Colored timeline of recent dev events and contributions | `local` |
| **Social** | `social` | Interactive social links, portfolio buttons, and contacts | `local` |

```bash
# Inspect any widget
profileforge widgets info github_stats

# List all available widgets
profileforge widgets list
```

---

## 👥 Persona Templates

Start with a persona that matches your developer identity. All templates include typed `manifest.yaml`, full seed configs, and a curated widget set.

| Persona | Template ID | Theme | Who It's For | Scaffold |
|---|---|---|---|---|
| **Backend Engineer** | `backend` | `github-dark` | Go, Rust, Python, microservices & DB devs | `profileforge new dev -t backend` |
| **Frontend Engineer** | `frontend` | `modern` | React, Vue, TypeScript, UI/UX devs | `profileforge new dev -t frontend` |
| **Minimalist** | `minimal` | `minimal` | Clean monochrome typography profiles | `profileforge new dev -t minimal` |
| **Student / Learner** | `student` | `catppuccin-mocha` | CS students, bootcamp grads, self-taught devs | `profileforge new dev -t student` |
| **Open Source** | `opensource` | `dracula` | Library authors & core maintainers | `profileforge new dev -t opensource` |
| **AI / ML Engineer** | `ai-engineer` | `cyberpunk` | PyTorch, LLM agents, data scientists | `profileforge new dev -t ai-engineer` |
| **Indie Hacker** 🆕 | `indie-hacker` | `modern` / `vercel` | Founders, bootstrappers, building in public | `profileforge new dev -t indie-hacker` |
| **Security Engineer** 🆕 | `security-engineer` | `dracula` / `cyberpunk` | Pentesters, AppSec engineers, bug bounty hunters | `profileforge new dev -t security-engineer` |
| **OSS Maintainer** 🆕 | `open-source-maintainer` | `github-dark` | OSS project leads, foundation contributors | `profileforge new dev -t open-source-maintainer` |

```bash
# List all templates
profileforge templates list
```

---

## 🎨 Theme Gallery

14 production-grade themes. Zero configuration required — just set `active` in your `profileforge.yaml`.

<div align="center">

<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/dracula.svg" alt="Dracula Theme Preview" width="400" />
</picture>
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/github-dark.svg" alt="GitHub Dark Theme Preview" width="400" />
</picture>

<br/>

<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/modern.svg" alt="Modern Theme Preview" width="400" />
</picture>
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/nord.svg" alt="Nord Theme Preview" width="400" />
</picture>

<br/>

<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/vercel.svg" alt="Vercel Theme Preview" width="400" />
</picture>
<picture>
  <img src="https://raw.githubusercontent.com/iisgaurav/profileforge/main/gallery/assets/minimal.svg" alt="Minimal Theme Preview" width="400" />
</picture>

</div>

| Theme ID | Mode | Tags | Primary Color |
|---|---|---|---|
| `github-dark` | 🌑 Dark | `core`, `official` | `#58A6FF` |
| `github-light` | ☀️ Light | `core`, `official` | `#0969DA` |
| `dracula` | 🌑 Dark | `official` | `#FF79C6` |
| `nord` | 🌑 Dark | `official` | `#88C0D0` |
| `modern` | 🌑 Dark | `core`, `official` | `#3B82F6` |
| `vercel` | 🌑 Dark | `official` | `#FFFFFF` |
| `minimal` | 🌕 Minimal | `core`, `official` | `#000000` |
| `apple` | ☀️ Light | `official` | `#0071E3` |
| `catppuccin-mocha` | 🌑 Dark | `official` | `#89B4FA` |
| `catppuccin-frappe` | 🌑 Dark | `official` | `#8CAAEE` |
| `catppuccin-macchiato` | 🌑 Dark | `official` | `#8AADF4` |
| `catppuccin-latte` | ☀️ Light | `official` | `#1E66F5` |
| `catppuccin-base` | 🌑 Dark | `official` | `#58A6FF` |
| `showcase` | ✨ Showcase | `core`, `official` | `#FFD700` |

### Create a Custom Theme

```yaml
# themes/custom-cyber.yaml
name: "Custom Cyber"
extends: "cyberpunk"
colors:
  primary: "#00FFCC"
  accent: "#FF007F"
  background: "#08090C"
radius:
  card: 16
  badge: 8
```

```bash
# Preview all themes
profileforge themes build
```

---

## 🎨 ProfileForge Studio

> **Visual, No-Code GitHub Profile Builder — runs entirely in your browser.**

<div align="center">

**Open `web/index.html` locally** (zero dependencies, zero install) and get:

| Feature | Details |
|---|---|
| 🎛️ **Visual Widget Picker** | Toggle any of the 15 widgets on/off with checkboxes |
| 👤 **Persona Auto-Config** | Pick a template → widgets + theme auto-select |
| 🖼️ **Live Preview Canvas** | See real themed SVG widget cards update in real time |
| 🎨 **Theme Selector Grid** | Click to apply any of the 14 themes instantly |
| 📋 **Copy README Markdown** | One-click copy of the ready-to-paste profile README snippet |
| 📥 **Export profileforge.yaml** | Download your config file to start building immediately |
| 📦 **Download SVG Bundle** | Batch-download all your enabled widget SVG assets |

</div>

```bash
# Clone and open Studio locally
git clone https://github.com/iisgaurav/profileforge
cd profileforge
# Open web/index.html in your browser — no server needed
start web/index.html   # Windows
open web/index.html    # macOS
```

---

## 🏗️ Architecture

ProfileForge uses a clean 6-layer decoupled pipeline — no side effects, no fragile string concatenation:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Configuration & Persona Layer (profileforge.yaml)       │
├─────────────────────────────────────────────────────────────┤
│  2. Data Connector Layer (GitHub REST/GraphQL, Local YAML)  │
├─────────────────────────────────────────────────────────────┤
│  3. Declarative Component Tree (Card, Row, Column, Badge)   │
├─────────────────────────────────────────────────────────────┤
│  4. Two-Pass Layout Engine (Flexbox, Bento Grid, Wrapping)  │
├─────────────────────────────────────────────────────────────┤
│  5. Theme Token Engine (Colors, Radius, Shadows, Motion)    │
├─────────────────────────────────────────────────────────────┤
│  6. SVG Visual Renderer (Linear Gradients, Defs, ARIA)      │
└─────────────────────────────────────────────────────────────┘
```

Every widget follows the same **6-phase lifecycle**: `metadata → fetch → transform → build → post_build → render_safe`. Failures are isolated — one broken connector never crashes your entire profile.

Read the formal [Architecture Decision Records (ADRs)](docs/adr/) for detailed technical rationale.

---

## 💻 CLI Cheat-Sheet

| Command | Flags | What It Does |
|---|---|---|
| `profileforge build` | `[--config <file>] [--output <dir>]` | Build all enabled widgets to SVG |
| `profileforge new <name>` | `[--template <id>]` | Scaffold a new project from a persona template |
| `profileforge init [dir]` | `[--template <id>]` | Init ProfileForge in an existing directory |
| `profileforge validate` | `[--config <file>]` | Validate config syntax and widget tree |
| `profileforge doctor` | — | Check Python version, deps, and env health |
| `profileforge benchmark` | `[--iterations N] [--budget-file <yaml>]` | Run multi-stage performance benchmark |
| `profileforge widgets list` | — | List all registered widgets with metadata |
| `profileforge widgets info <id>` | — | Display schema and options for a widget |
| `profileforge templates list` | — | List all official persona templates |
| `profileforge gallery export` | `[--out-dir <dir>]` | Export theme & widget catalog assets |
| `profileforge themes build` | `[--config <file>]` | Build theme preview SVG cards |

---

## ⚡ Performance Benchmarks

Sub-15ms end-to-end. Verified on every commit.

| Stage | SLA Budget | Actual (Mean) | Status |
|---|---|---|---|
| **Config Parsing** | `< 5.0ms` | **0.75ms** | ✅ |
| **Theme Token Resolution** | `< 2.0ms` | **1.02ms** | ✅ |
| **Widget Component Build** | `< 5.0ms` | **0.64ms** | ✅ |
| **Two-Pass Layout Engine** | `< 10.0ms` | **0.59ms** | ✅ |
| **SVG Renderer** | `< 10.0ms` | **6.43ms** | ✅ |
| **End-to-End** | `< 50.0ms` | **9.71ms** | ✅ |

- **Throughput:** >100 operations/second  
- **Peak Memory:** ~0.18 MB

```bash
# Verify on your machine
profileforge benchmark --budget-file budget.yaml
```

---

## 🔒 Governance & Stability

- **Public API Lock:** All public API signatures tracked in `api.lock.json`. Zero silent drift.
- **RFC Process:** Breaking changes require an approved RFC ([`docs/RFC_PROCESS.md`](docs/RFC_PROCESS.md)).
- **Release Verification:** Quality gates enforce tests, linting, links, benchmarks, and SemVer ([`docs/RELEASE_GUIDE.md`](docs/RELEASE_GUIDE.md)).

---

## 🤝 Contributing

ProfileForge welcomes contributions! The fastest ways to contribute:

1. **Add a widget** — Subclass `Widget`, implement `build()`, register with `@register_widget("my_widget")`. See [`docs/WIDGET_AUTHORING.md`](docs/WIDGET_AUTHORING.md).
2. **Add a theme** — Drop a YAML file in `src/profileforge/themes/`. Inherit from any existing theme.
3. **Add a template** — Create a folder in `src/profileforge/templates/` with `manifest.yaml`, `profileforge.yaml`, `config/*.yaml`, and `README.md`.

Read the full [Contributing Guide](CONTRIBUTING.md) before opening a PR.

---

## ❓ FAQ

**Q: Do I need a GitHub Personal Access Token?**  
*A: For local widgets (`hero`, `skills`, `roadmap`, etc.), no token needed. For live GitHub data (`github_stats`, `repositories`), set `GITHUB_TOKEN` to avoid API rate limits.*

**Q: How do I auto-update my README on a schedule?**  
*A: Use a GitHub Actions workflow that runs `profileforge build` on a cron schedule and commits the generated SVGs.*

**Q: Can I create custom widgets?**  
*A: Yes! See [`docs/WIDGET_AUTHORING.md`](docs/WIDGET_AUTHORING.md) for the complete guide.*

---

## 📄 License

ProfileForge is distributed under the [MIT License](LICENSE). © 2026 ProfileForge Team.
