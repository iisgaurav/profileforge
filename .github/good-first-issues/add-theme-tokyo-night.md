# [Good First Issue] Add Tokyo Night Theme

## 🌟 Background

Tokyo Night is a popular VS Code and terminal color scheme loved by developers for its soothing dark palette and vibrant neon accents. Adding Tokyo Night to ProfileForge will provide users with a sleek, modern aesthetic for their GitHub profile widgets.

## 🎨 Color Palette & Tokens

Implement the following design tokens in your theme definition:

- **background**: `#1a1b26` (Dark storm blue)
- **surface**: `#24283b` (Elevated card background)
- **primary**: `#7aa2f7` (Vibrant blue)
- **accent**: `#bb9af7` (Soft purple)
- **text**: `#c0caf5` (High-contrast body text)
- **muted**: `#565f89` (Subtle secondary text)
- **border**: `#292e42` (Card and divider outline)

## ✅ Acceptance Criteria

- [ ] A new theme YAML file is created at `src/profileforge/themes/tokyo-night.yaml`
- [ ] The theme includes `name: "Tokyo Night"` and extends `github-dark` (`extends: "github-dark"`)
- [ ] All required color design tokens listed above are defined
- [ ] Running `profileforge themes build` compiles the theme without errors
- [ ] Running `profileforge doctor` passes cleanly without warnings
- [ ] The PR description includes a rendered preview screenshot of at least one widget using the Tokyo Night theme
- [ ] File name follows kebab-case naming conventions (`tokyo-night.yaml`)

## 💡 Technical Hints & Guidance

1. Refer to `src/profileforge/themes/dracula.yaml` as an example of a complete theme definition.
2. Compile and test themes locally with:
   ```bash
   profileforge themes build
   ```
3. Test your new theme against a test profile config:
   ```bash
   profileforge build --config my-test-profile.yaml --theme tokyo-night
   ```

## 📚 Resources & Documentation

- **Theme Authoring Guide**: [`docs/community/SUBMIT_THEME.md`](docs/community/SUBMIT_THEME.md)
- **Design Tokens Reference**: [`docs/TOKENS.md`](docs/TOKENS.md)

---

- **Labels**: `good first issue`, `theme`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 1–2 hours
