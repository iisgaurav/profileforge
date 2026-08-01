# Theme Architecture

Themes in ProfileForge are defined using YAML. They provide a complete set of design tokens that instruct components on how to render.

## Theme Structure

A theme file provides metadata and token values:
- `name`: Theme identifier
- `mode`: Light, dark, minimal, modern
- `colors`: Color tokens
- `typography`: Typography tokens
- `spacing`: Spacing tokens
- `radius`: Radius tokens
- `shadows`: Shadow tokens
- `motion`: Motion tokens
- `effects`: Effect tokens (glass, glow)
- `extends`: Base theme to inherit from.

## The `extends` feature

You can inherit from an existing theme to override only specific values. For example, to create a red variant of the Catppuccin theme:

```yaml
name: catppuccin-red
extends: catppuccin-mocha
colors:
  primary: "#F28FAD"
```

This ensures DRY (Don't Repeat Yourself) theme definitions.
