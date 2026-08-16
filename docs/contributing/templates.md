# Submit a Persona Template

Persona Templates are complete profile configurations designed for specific types of users (e.g., Backend Developer, AI Engineer, Indie Hacker). They provide a one-click starting point for new users.

## Folder Structure

Templates are stored in `src/profileforge/templates/<template-id>/`. A valid template directory looks like this:

```text
src/profileforge/templates/indie-hacker/
├── manifest.yaml
├── profileforge.yaml
├── config/
│   └── widgets.yaml
└── README.md
```

## `manifest.yaml` Schema

The `manifest.yaml` file defines the template's metadata:

```yaml
id: indie-hacker
name: "Indie Hacker"
description: "Perfect for makers shipping side projects rapidly. Focuses on recent launches, MRR stats, and active repositories."
author: "@yourusername"
theme: "modern"
widgets:
  - hero
  - roadmap
  - repositories
  - social
tags:
  - maker
  - entrepreneur
  - javascript
version: "1.0.0"
```

## Seed Data Requirements

Your template must render perfectly out-of-the-box. To ensure this, you must provide realistic **seed data** (or fallback data) in your configuration so that when a user previews the template before linking their data, it looks complete and impressive.

## Base Theme Dependency

The `profileforge.yaml` file in your template must reference a valid base theme (e.g., `theme: modern` or `theme: github-dark`). 

## PR Checklist

- [ ] Folder is named using `kebab-case` (e.g., `data-scientist`).
- [ ] `manifest.yaml` is fully populated.
- [ ] `profileforge.yaml` is valid and references a core theme.
- [ ] Includes realistic seed data for widget previews.
- [ ] `README.md` explains who the persona is for.
- [ ] Template validates cleanly with `profileforge validate --template <id>`.

## Naming Conventions

Always use `kebab-case` for the template ID and folder name. Ensure the display `name` in the manifest is title-cased.
