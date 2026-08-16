# Submit a Theme

Themes in ProfileForge define the look and feel of your GitHub profile. They are purely declarative YAML files that specify colors, typography, border radii, shadows, and motion properties.

## Theme YAML Schema

A valid ProfileForge theme must include the following fields:

- `name`: The display name of the theme.
- `extends`: The base theme to inherit from (e.g., `github-light` or `github-dark`).
- `colors`: A mapping of semantic color variables (primary, secondary, background, text, borders, etc.).
- `radius`: Border radius tokens (small, medium, large, full).
- `shadows`: Box shadow definitions.
- `typography`: Font family settings for sans, serif, and mono.
- `motion`: Transition speeds and easing curves.

### Full Example: `tokyo-night.yaml`

```yaml
name: Tokyo Night
extends: github-dark
colors:
  background: "#1a1b26"
  surface: "#24283b"
  primary: "#7aa2f7"
  secondary: "#bb9af7"
  success: "#9ece6a"
  warning: "#e0af68"
  danger: "#f7768e"
  text_primary: "#c0caf5"
  text_secondary: "#a9b1d6"
  border: "#414868"
radius:
  sm: "4px"
  md: "8px"
  lg: "12px"
  full: "9999px"
shadows:
  sm: "0 1px 2px rgba(0, 0, 0, 0.4)"
  md: "0 4px 6px rgba(0, 0, 0, 0.5)"
typography:
  sans: "'Inter', sans-serif"
  mono: "'Fira Code', monospace"
motion:
  default: "0.2s ease"
```

## How to Test Your Theme

Before submitting, you must ensure your theme builds and validates correctly.

1. **Validate**:
   ```bash
   profileforge validate --theme tokyo-night
   ```

2. **Build**:
   ```bash
   profileforge themes build --theme tokyo-night
   ```

3. **Check with Doctor**:
   ```bash
   profileforge doctor
   ```

## PR Checklist

When opening a Pull Request to add a new official theme, ensure you have:

- [ ] Added your theme file to `src/profileforge/themes/`.
- [ ] Used `kebab-case` for the filename (e.g., `tokyo-night.yaml`).
- [ ] Ensured your theme `extends` an official base theme (`github-light` or `github-dark`).
- [ ] Checked that there are **no hardcoded pixel values** for colors in widgets.
- [ ] Verified that the CI pipeline passes.
- [ ] Included a **preview screenshot** of the rendered profile using your theme in the PR description.

## Including a Preview

Run `profileforge build --theme <your-theme>` against the Kitchen Sink template, take a screenshot, and drop the image into your PR description so reviewers can immediately see the design!
