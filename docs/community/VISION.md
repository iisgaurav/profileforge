# Product Vision

**Core Belief: GitHub profiles are a developer's living portfolio.** 
They should be dynamic, beautiful, fast, and effortless to maintain.

ProfileForge is designed to take the friction out of maintaining a stunning personal brand as a developer.

## Today: Developer Profile Platform (v1.0)
Currently, ProfileForge is a powerful CLI and engine. Developers can write declarative YAML, utilize 15 rich widgets, apply 14 beautiful themes, and automatically build SVG-based profiles using GitHub Actions.

## Near-Term: Studio v2
The current Studio provides a visual preview. The near-term vision is a **complete drag-and-drop experience**:
- Real-time live SVG rendering as you adjust sliders.
- A visual Theme Customizer (pick colors visually, export as YAML).
- Seamless integration to copy-paste the generated setup directly to your repository.

## Medium-Term: Community Marketplace
We envision a thriving ecosystem of community creations.
- A future install command to instantly grab a theme (e.g. `tokyo-night`) from the registry.
- A future install command to add custom widgets (e.g. `spotify-now-playing`) from the community.
- A centralized marketplace website to browse, rate, and discover community themes, widgets, and templates.

## Long-Term: Cloud-Hosted ProfileForge
The ultimate goal is zero-configuration:
- A hosted web service.
- **OAuth GitHub Login:** Sign in, pick a persona template, and click "Publish".
- We handle the cron jobs, data fetching, and updating of your GitHub README on our servers.
- **Team Profiles:** Aggregated stats for entire GitHub organizations.

## Design Principles for Future Work
1. **Developer First:** Everything must be controllable via code (YAML) and CLI, even if a GUI exists.
2. **Performant:** SVGs must be lightweight; no massive JavaScript bundles inside SVGs.
3. **Beautiful Defaults:** Fallback states and default themes must look premium.
