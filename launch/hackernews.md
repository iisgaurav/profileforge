# ProfileForge HackerNews Launch

## Post Details
**Title:** Show HN: ProfileForge – Declarative GitHub Profile & SVG Widget Engine (Python, YAML)
**URL:** https://github.com/iisgaurav/profileforge

## First Comment (Maker Note)

Hi HN,

I build a lot of open source, and my GitHub profile is basically my resume. But managing it was frustrating. Relying on remote servers to dynamically render SVGs on every page load meant constant rate-limiting issues, broken images, and zero layout control. 

So I built ProfileForge to fix this. It’s a local-first engine written in Python (3.9+) that takes a declarative YAML config and generates static, beautiful SVG widgets. You run it locally or hook it into GitHub Actions to update your profile automatically.

I tried to engineer this properly. Under the hood, it uses a 6-layer pipeline (Parse → Fetch → Context → Render → Assemble → Output). A few technical decisions I'm happy with:

- **Performance Budgets:** By parsing and rendering SVGs locally instead of hitting dynamic endpoints, the engine runs extremely fast. It hits sub-15ms build times (100+ ops/sec), meaning it barely consumes any compute time on CI/CD.
- **`render_safe()` Isolation:** I implemented a strict isolation layer. If an external API (like Spotify or a blog RSS feed) goes down or times out, `render_safe()` catches it. It will render a graceful fallback for that specific widget rather than failing the whole build or showing a broken image.
- **Extensibility:** The YAML DSL maps directly to Python classes. Adding a new widget is just a matter of subclassing `BaseWidget` and feeding it data.

It ships with 15 widgets, 14 color themes, and a visual builder called ProfileForge Studio if you don't want to hand-write YAML.

It’s completely open source (MIT). I’d love to hear your thoughts on the architecture, the pipeline design, or any critiques of the codebase. Happy to answer any questions!
