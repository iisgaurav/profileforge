# [Good First Issue] Record and Embed a CLI Demo GIF in README

## 🌟 Background

A short animated GIF displaying the end-to-end ProfileForge CLI workflow (installation → project scaffolding → building SVG profile widgets) will make the `README.md` inviting and immediately demonstrate value to new visitors.

## 🎬 Terminal Commands to Capture

Record a clean terminal performing the following steps:

```bash
pip install profileforge
profileforge new my-profile --template backend
cd my-profile
profileforge build
```

## 📐 GIF Specifications & Guidelines

- **Duration**: Maximum 30 seconds
- **File Size**: Under 2 MB (compressed/optimized)
- **Typography**: Minimum 14px crisp terminal font
- **Environment**: Clean prompt with standard colors (no custom prompt junk or personal user paths visible)
- **File Location**: `docs/images/demo.gif`
- **Embedding**: Add to `README.md` under the *"Build in 30 Seconds"* section

## 🛠️ Recommended Recording Tools

- **macOS / Linux**: `asciinema record demo.cast` followed by `agg demo.cast docs/images/demo.gif`
- **Windows**: Terminalizer or ScreenToGif
- **Cross-Platform**: QuickTime / OBS Studio converted via `ffmpeg` / `gifsicle`

## ✅ Acceptance Criteria

- [ ] `docs/images/demo.gif` committed to repository
- [ ] `README.md` updated with embed syntax `![CLI Demo](docs/images/demo.gif)`
- [ ] Final GIF file size is strictly under 2 MB
- [ ] Text and output in GIF are legible on both light and dark GitHub themes
- [ ] Terminal environment is clean with no sensitive user paths visible

---

- **Labels**: `good first issue`, `documentation`, `media`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 1–2 hours
