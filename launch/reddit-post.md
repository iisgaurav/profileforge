# ProfileForge Reddit Posts

## Option 1: r/github (Show-don't-tell, casual tone)

**Title:** I got tired of my GitHub profile breaking, so I built a local Python engine to generate SVGs from YAML instead.

**Body:**
Hey r/github,

My GitHub profile used to be embarrassing. Half the time the third-party stat SVGs I was using were broken due to rate limits, or the themes didn't match, and my README was just a giant mess of markdown links I was afraid to touch.

I realized relying on external servers to render SVGs dynamically on every page load was fragile. So I built **ProfileForge**. 

Instead of external links, you write a simple YAML config (`profileforge new`). You run `profileforge build` locally (or via GitHub actions), and it pulls your GitHub data, generates the SVGs on your own machine in milliseconds, and updates your README.

Some cool parts:
* **15 widgets built-in:** Top languages, commit graphs, Spotify, latest blogs.
* **Themes:** 14 built-in themes like Dracula, Nord, Monokai.
* **No-code UI:** If you hate YAML, there's `ProfileForge Studio` (an HTML file in the repo) where you can drag, drop, and preview your profile, then just copy the YAML.

It's completely free and MIT licensed. You can try it out with `pip install profileforge`.

Repo is here: https://github.com/iisgaurav/profileforge

Would love to know what widgets you guys usually put on your profiles so I can add them!

---

## Option 2: r/Python (Technical, architecture focus)

**Title:** Show r/Python: ProfileForge - A declarative SVG rendering engine for GitHub profiles (Sub-15ms builds)

**Body:**
Hey folks,

I've been working on a new CLI tool called **ProfileForge** (Python 3.9+) that transforms YAML configurations into dynamic SVG widgets for GitHub profiles. 

I wanted to share it here because I spent a lot of time optimizing the Python architecture and I'm really proud of how it turned out.

**How it works under the hood:**
The core is a 6-layer declarative pipeline:
1. Config parsing (YAML DSL validation)
2. Data Fetching (async API connectors)
3. Context Building
4. Widget Rendering
5. Layout Assembly
6. Output Generation

**Interesting Technical Decisions:**
* **Widget Lifecycle & `render_safe()`:** I built an isolation layer. If a connector (like Spotify API or GitHub GraphQL) times out or fails, `render_safe()` catches it. The engine will gracefully render a fallback or skip the widget rather than crashing the pipeline. 
* **Performance:** It parses and renders the SVG DOM locally. We're hitting sub-15ms build times and >100 ops/sec, meaning it's incredibly cheap to run on GitHub Actions.
* **Extensibility:** Adding a new widget is just subclassing a Python BaseWidget and defining an SVG template. 

It comes with 15 built-in widgets, 14 themes, and a visual UI builder (ProfileForge Studio). 

You can `pip install profileforge` to test it out.

Source code (MIT): https://github.com/iisgaurav/profileforge

I'd love some feedback on the codebase, specifically the pipeline implementation or if you have ideas on optimizing the SVG templating further. Happy to answer any questions about the architecture!
