# ProfileForge Roadmap

## Vision

ProfileForge aims to become an extensible framework for building beautiful, maintainable, and customizable developer profiles. 

The core architecture is considered stable. Future development prioritizes developer experience, visual quality, extensibility, and ecosystem growth.

---

## Phase 1 — Core Stabilization ✅

Freeze the foundational architecture. No breaking API changes without an explicit Request for Comments (RFC).

* Component System
* Layout Engine
* Theme Engine
* SVG Renderer
* Connector API
* Plugin API
* Metric System

---

## Phase 2 — Visual Identity & Design Language

Establish a distinctive, unmistakable "ProfileForge" aesthetic. Document the visual primitives that define the brand:

* Unified typography rules
* Perfect spacing and padding
* Consistent card hierarchy
* Standardized border radius
* Shadow and gradient definitions
* Iconography style guidelines

---

## Phase 3 — Theme Ecosystem

Deliver a suite of polished, professional themes out of the box.

* GitHub Dark / Light
* Nord
* Dracula
* Catppuccin
* Modern
* Minimal
* Cyberpunk
* Apple / Vercel-inspired

---

## Phase 4 — Widget Ecosystem

Expand the core widget library across distinct categories using the unified Design Language.

* **Identity:** About, Hero, Contact, Socials
* **Statistics:** GitHub Stats, Languages, Repository Stats, Followers, Contributions
* **Career:** Experience, Skills, Timeline, Achievements
* **Development:** Roadmap, Current Focus, Tech Stack, Learning Progress
* **Content:** Blog Posts, RSS, Spotify, WakaTime
* **Open Source:** Projects, Sponsors, Organizations, Releases

---

## Phase 5 — Templates

Provide ready-to-use boilerplate templates tailored to specific developer personas to drive adoption.

* Backend Engineer
* Frontend Engineer
* AI / ML Engineer
* Student
* DevOps
* Corporate
* Minimal

---

## Phase 6 — Developer Experience

Enhance the local workflow and debugging tools.

* `profileforge preview` local server
* Hot reloading on config save
* Improved CLI diagnostics
* Watch mode

---

## Phase 7 — Connectors & Plugins

Expand the data ingestion layer to support more platforms natively.

* GitHub (GraphQL & REST)
* RSS Feeds
* Spotify
* WakaTime
* Hashnode, Dev.to, Medium
* LeetCode, Codeforces

---

## Phase 8 — Documentation & Governance

Professionalize the OSS ecosystem.

* Complete documentation (Architecture, Plugin, Theme, and Widget Guides)
* Introduce the **RFC Process** for core API changes.
* Establish Contribution guidelines and Issue templates.

---

## Phase 9 — Community & Showcase

Launch initiatives to highlight community creations.

* **Benchmark Repository:** Establish `awesome-profileforge` or `profileforge-gallery` containing 100+ Profile Examples, Widgets, and Themes.
* **Website:** Launch `profileforge.dev` featuring a Live Playground, Theme Gallery, and Widget Gallery.

---

### Governance: The RFC Process
Any proposal that changes the Public API, Widget API, Theme API, Component API, Connector API, or Layout Engine must first go through an RFC (Request for Comments). This prevents breaking changes and gives contributors confidence that the core is stable.
