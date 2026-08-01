# ADR-002: Theme Token Design System and Inheritance Model

## Status
**Accepted** (2026-08-02)

## Context & Problem Statement
ProfileForge users demand extensive visual personalization—from dark and light GitHub aesthetics to popular colorways like Catppuccin, Dracula, Nord, Vercel, and Apple macOS styling.

Hardcoding hex codes or individual CSS rules inside widgets results in:
1. Visual inconsistency across different widgets in the same profile.
2. Inability to switch themes globally via a single configuration option.
3. Severe friction for open-source contributors wanting to submit new community themes.
4. Duplicate theme definitions for slight color variations.

## Decision
We decided to implement a **Structured Theme Token Design System** with **Single Inheritance and Deep Merging** (Layer 2).

Key elements of this decision:
1. **Strongly Typed Token Schemas**:
   - `ColorTokens`: `primary`, `secondary`, `background`, `surface`, `border`, `text`, `muted`, `success`, `warning`, `info`, `accent`.
   - `TypographyTokens`: `font_family`, `heading`, `body`, `small`.
   - `SpacingTokens`: `xs`, `sm`, `md`, `lg`, `xl` (strictly 4px/8px modular scale).
   - `RadiusTokens`: `card`, `progress`, `badge`.
   - `ShadowTokens`: `none`, `low`, `medium`, `high`.
   - `MotionTokens`: `duration_fast`, `duration_normal`, `duration_slow`, `easing`.
   - `EffectsTokens`: `glow`, `shadow`, `glass`.
2. **YAML Serialization**: Themes are defined as human-readable YAML files placed in `themes/` or provided as built-ins in `profileforge/themes/`.
3. **Theme Inheritance (`extends:`)**: Themes can inherit from existing themes (e.g., `catppuccin-mocha` extends `catppuccin-base`), overriding only specific token subsets.
4. **Deep Merging & Cycle Detection**: The `ConfigLoader.load_theme` engine performs recursive dictionary merging with explicit cycle detection to eliminate infinite loops.

```yaml
# Example: Custom developer theme extending GitHub Dark
name: neon-cyberpunk
mode: modern
extends: github-dark
colors:
  primary: "#00FFCC"
  secondary: "#FF007F"
  background: "#0A0E17"
  surface: "#121824"
  border: "#1F293D"
  accent: "#7928CA"
effects:
  glow: "high"
  shadow: "medium"
```

## Consequences

### Positive
- **Guaranteed Consistency**: Every widget consuming `context.theme.colors.*` or semantic keys (`"primary"`, `"muted"`) renders seamlessly under any active theme.
- **Low-Friction Authoring**: Creating a new community theme requires only a few lines of YAML overriding base tokens.
- **Runtime Safety**: Strong dataclass validation ensures no missing tokens or invalid schemas reach rendering layers.

### Negative / Trade-offs
- **Token Rigidity**: Custom one-off colors outside the token schema require explicit fallback logic, incentivizing authors to use design tokens rather than ad-hoc color values.
