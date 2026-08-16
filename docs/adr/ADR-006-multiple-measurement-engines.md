# ADR-006: Abstracting Intrinsic Measurement and Future Pluggable Engines

**Status:** Accepted (For v2.x architecture planning)  
**Date:** 2026-08-08  
**Context:** ProfileForge Rendering Pipeline (Layer 4)

## Context
During the finalization of the ProfileForge v1.x rendering pipeline, we extracted the intrinsic geometry calculation out of the `LayoutEngine`. The layout engine now purely coordinates structural layout constraints and relies on an `IntrinsicMeasurer` interface and components' `.intrinsic_size(measurer)` implementation.

For v1.x, we are defaulting to the `ApproximateTextMeasurer` which uses a fast, heuristic-based `0.55` multiplier for proportional typography width. However, as the ecosystem grows and ProfileForge expands to more complex designs, the heuristic measurement will become insufficient for pixel-perfect SVGs, particularly regarding varying font families, emoji support, or non-Latin glyphs.

## Decision
We have decided to architect Layer 4 to support **Multiple Measurement Engines**, but we **will not implement them in v1.x**. The `IntrinsicMeasurer` abstraction has been locked in place to allow future pluggable engines without breaking component compatibility.

When the ecosystem requires higher-fidelity measurement, we will implement multiple engines:
```text
IntrinsicMeasurer
├── ApproximateTextMeasurer (Default, lightweight heuristic)
├── CairoTextMeasurer (High fidelity, requires cairo)
├── BrowserTextMeasurer (Headless playwright/puppeteer integration)
├── SkiaTextMeasurer (High performance pixel-perfect)
└── FontToolsTextMeasurer (Direct TTF/OTF parsing)
```

Users will be able to inject their preferred high-fidelity measurer via the `BuildContext` or `RenderContext` when building their profile.

## Consequences
- **Positive:** Layer 4 (Layout Engine) is fully decoupled from font rendering knowledge and remains mathematically pure.
- **Positive:** We avoid imposing heavy, native dependencies (like Cairo or Skia) onto the default v1.x installation footprint, honoring the goal to keep ProfileForge lightweight for new users.
- **Positive:** The rendering contract remains strictly backward-compatible.
- **Negative:** For the remainder of v1.x, developers must rely on approximation limits for font width. Widgets with precise boundary requirements may see slight padding inconsistencies across different font families.

## Implementation Notes (Future)
When implementing these advanced measurers, we must also introduce an `IntrinsicMeasurementCache` inside `BuildContext` to memoize the bounds (e.g. `(text, typography_role)` tuple mapping to `Size`). This will be critical to offset the computational overhead of invoking Skia or headless browsers.
