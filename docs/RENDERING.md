# Rendering Architecture

ProfileForge uses a strict, unidirectional rendering pipeline. The architecture is explicitly designed to separate data acquisition, composition, measurement, layout, and rendering into distinct layers.

## The Rendering Pipeline

```text
Widget
  │
  ▼
Declarative Components
  │
  ▼
IntrinsicMeasurer
  │
  ▼
Layout Engine
  │
  ▼
RenderNode AST
  │
  ▼
Renderer
  │
  ▼
SVG
  │
  ▼
Browser
```

---

## Render Contract (v1.x)

This contract is immutable for the entire v1.x lifecycle. No exceptions or pull requests will be accepted if they violate these boundaries.

### Components
- ✓ Expose intrinsic geometry via `.intrinsic_size(measurer)`
- ✓ Expose semantic information
- ✗ Never inspect parent components
- ✗ Never inspect sibling components
- ✗ Never mutate layout

### Layout Engine (Layer 4)
- ✓ Computes geometry
- ✓ Allocates constraints
- ✓ Positions children relative to bounds
- ✗ Never paints
- ✗ Never resolves colors or theme tokens
- ✗ Never resolves typography settings
- ✗ Never mutates component definitions

### Renderer (Layer 2)
- ✓ Paints the layout tree
- ✓ Resolves theme tokens and colors
- ✓ Emits final SVG string
- ✗ Never computes layout
- ✗ Never changes component bounds
- ✗ Never modifies constraints

## Measurement Abstraction
Layout Engine computes geometry strictly using deterministic nodes and boundaries. To determine the natural size of variable content (like `Text`), it delegates to the `IntrinsicMeasurer` abstraction.

This allows ProfileForge to swap measurement heuristics—from fast approximations (`ApproximateTextMeasurer`) to pixel-perfect headless browser implementations (`BrowserTextMeasurer`) in the future without touching the layout logic.
