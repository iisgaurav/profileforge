# ADR-001: Declarative Component Tree Architecture

## Status
**Accepted** (2026-08-02)

## Context & Problem Statement
ProfileForge produces SVG cards, charts, and metric displays embedded into GitHub profile readmes and dashboards. In traditional profile generator tools, widgets typically generate raw SVG strings by concatenating XML templates or using string formatting (e.g. `f"<svg><rect width='{w}' height='{h}'... />"`).

This raw string template approach introduces severe architectural limitations:
1. **Lack of Composability**: Reusable UI components (like badges, progress bars, metric groups) cannot be nested or combined cleanly without brittle string splicing.
2. **Untestable Visual Logic**: Verifying that a widget produces correct layout structures requires complex XML regex or DOM parsing in unit tests.
3. **Tight Coupling to SVG**: The widget logic is tightly coupled to SVG markup, making it impossible to support alternative backends (such as HTML, PNG canvas, or terminal ANSI output) in the future.
4. **Fragile Theming**: Dynamic theme tokens and style properties must be manually interpolated at every string formatting call site.

## Decision
We decided to introduce a **Declarative Component Tree** architecture (Layer 3) representing the UI as a tree of composable Python objects.

Key elements of this decision:
1. **Base Component**: An abstract `Component` base class that holds a `Style` descriptor and layout state fields (`computed_x`, `computed_y`, `computed_width`, `computed_height`).
2. **Structural Primitives**: Declarative container components (`Inline`, `Column`, `Padding`, `Constraints`, `Wrap`) that encapsulate child hierarchies and spacing properties.
3. **Visual Primitives**: High-level semantic components (`Card`, `Text`, `Badge`, `Icon`, `ProgressBar`, `Metric`, `MetricGroup`, `CircularMetric`) that encapsulate visual intent without emitting raw XML.
4. **Style Abstraction**: A strongly typed `Style` dataclass that normalizes colors, margins, padding, radii, font weights, and flex alignment flags (`align`, `justify`, `width="fill"`).

```python
# Example declarative composition in a widget build() method:
content = Column(
    children=[
        Text("Weekly Velocity", style=Style(font_size=14, color="text")),
        ProgressBar(progress=75, style=Style(height=8, border_radius=4)),
        Inline(
            children=[
                Badge(label="Python", style=Style(color="primary")),
                Badge(label="FastAPI", style=Style(color="secondary")),
            ],
            spacing=8,
        ),
    ],
    spacing=12,
)
return Card(title="Engineering Overview", child=Padding(child=content, value=16))
```

## Consequences

### Positive
- **Complete Decoupling**: Widgets construct pure UI data trees and have zero knowledge of SVG XML tags, coordinates, or string escaping.
- **Enhanced Testability**: Unit tests can inspect the component hierarchy and property assertions without regex or XML parsers.
- **Pluggable Renderers**: The same component tree can be passed to `SVGRenderer`, future canvas renderers, or headless validation tools.
- **Maintainable Design Language**: UI primitives strictly enforce the ProfileForge design system.

### Negative / Trade-offs
- **Object Overhead**: Constructing trees of Python objects introduces minimal memory overhead, which is completely negligible for profile dashboards (~sub-millisecond overhead for 50-100 nodes).
- **Learning Curve**: Widget authors must learn the ProfileForge component taxonomy instead of writing quick raw SVG snippets. Comprehensive documentation and templates in `docs/WIDGET_AUTHORING.md` mitigate this.
