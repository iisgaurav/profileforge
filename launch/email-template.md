# ProfileForge Newsletter Outreach Templates

## Subject Line Options
1. A faster, declarative way to build GitHub profiles (Sub-15ms python engine)
2. Stop copy-pasting SVG templates for GitHub Profiles 🛠️
3. ProfileForge: A new open-source engine for developer profiles

## Email Body

Hi [Name],

I've been a long-time reader of [Newsletter Name] and wanted to share an open-source tool I just released that I think your developer audience will appreciate.

It’s called **ProfileForge** (Python/MIT). 

Developers waste hours maintaining their GitHub profiles—copy-pasting markdown, relying on third-party servers to render SVGs dynamically, and dealing with broken images when APIs rate-limit them. 

ProfileForge fixes this by shifting to a local-first, declarative model. You write a clean YAML config, and our Python engine generates beautifully themed SVG widgets in under 15ms. It includes 15 widgets, 14 themes, and a visual browser-based builder for those who hate YAML. It's meant to be dropped into GitHub Actions and forgotten about.

GitHub: https://github.com/iisgaurav/profileforge

I'd be honored if you considered featuring it in an upcoming issue! Let me know if you need any other info.

Best,
Gaurav

---

## Customization Notes

**For Bytes.dev:**
*Tone should be a bit cheekier.* 
Add line: "Because the only thing worse than writing CSS is trying to center an SVG inside a GitHub Markdown table."

**For TLDR Tech:**
*Focus strictly on the architecture.*
Add line: "We used a 6-layer pipeline with `render_safe()` isolation to ensure that if a data-fetching API times out, the profile rendering never breaks."

**For Changelog:**
*Focus on the open-source community aspect.*
Add line: "We're building this to be highly extensible and are already seeing the community contribute custom widgets. We'd love to get it in front of the OSS community."
