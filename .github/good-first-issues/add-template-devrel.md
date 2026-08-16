# [Good First Issue] Create a DevRel Persona Template

## 🌟 Background

Developer Relations (DevRel) engineers, developer advocates, and technical community managers need a GitHub profile template tailored to their unique priorities: highlighting community engagement, conference talks, blog publications, social reach, and open source activity. Currently, ProfileForge lacks a dedicated DevRel template.

## 🎯 Target User Persona

- Developer Advocates & DevRel Engineers
- Community Managers & Technical Evangelists
- Open Source Advocates

## 🧩 Suggested Widget Set & Theme

- **Widgets**: `hero`, `about`, `social`, `repositories`, `skills`, `activity_timeline`
- **Default Theme**: `github-dark` or `modern`

## 📁 Required Directory & File Structure

Create the template files under `src/profileforge/templates/devrel/`:

```
src/profileforge/templates/devrel/
├── manifest.yaml        # Template metadata
├── profileforge.yaml    # Main configuration
├── config/
│   ├── hero.yaml
│   ├── about.yaml
│   ├── skills.yaml
│   └── social.yaml
└── README.md            # Target audience & setup instructions
```

### `manifest.yaml` Required Fields

```yaml
id: devrel
name: "Developer Relations Advocate"
description: "Tailored profile template for DevRel engineers, community leads, and tech advocates."
author: "ProfileForge Community"
theme: "github-dark"
widgets:
  - hero
  - about
  - social
  - repositories
    - skills
  - activity_timeline
tags:
  - devrel
  - advocacy
  - community
  - speaking
version: "1.0.0"
```

## ✅ Acceptance Criteria

- [ ] All required files and folders are created under `src/profileforge/templates/devrel/`
- [ ] Running `profileforge new test-devrel --template devrel` scaffolds a project cleanly
- [ ] Seed configuration YAML files contain realistic, helpful example data (e.g. sample talks, blog links)
- [ ] `profileforge build` completes and renders SVG widgets without errors
- [ ] `README.md` clearly explains how DevRel advocates can customize the template

## 💡 Technical Hints & Guidance

1. Look at existing templates in `src/profileforge/templates/` (such as `backend` or `minimalist`) for reference layout structure.
2. Verify template registration by testing CLI scaffolding:
   ```bash
   profileforge new my-devrel-profile --template devrel
   cd my-devrel-profile
   profileforge build
   ```

## 📚 Resources & Documentation

- **Template Contribution Guide**: [`docs/community/SUBMIT_TEMPLATE.md`](docs/community/SUBMIT_TEMPLATE.md)

---

- **Labels**: `good first issue`, `template`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 2–3 hours
