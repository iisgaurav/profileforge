# [Good First Issue] Add an Education Widget

## 🌟 Background

Many developers have impressive educational backgrounds—such as university degrees, industry certifications, bootcamps, and online specializations—that they want to display on their developer profile. Currently, ProfileForge has no dedicated widget to showcase education and credentials.

## 📋 Data Schema (`config/education.yaml`)

The widget should read user configuration matching this schema:

```yaml
education:
  - institution: "MIT"
    degree: "B.S. Computer Science"
    year: 2020
    type: degree   # Options: degree | certification | course | bootcamp
  - institution: "Coursera"
    certification: "Deep Learning Specialization"
    provider: "DeepLearning.AI"
    year: 2022
    type: certification
```

## 🎨 Expected SVG Output

A clean, responsive SVG card displaying each entry with its institution name, degree/certification title, year, and a visual badge distinguishing certifications/bootcamps from traditional degrees.

## ✅ Acceptance Criteria

- [ ] Create `src/profileforge/widgets/education.py`
- [ ] Apply `@register_widget("education")` decorator
- [ ] Assign category `WidgetCategory.CAREER`
- [ ] Implement all 6 required lifecycle methods:
  1. `metadata()`
  2. `validate()`
  3. `resolve_connectors()`
  4. `fetch()`
  5. `transform()`
  6. `build()`
- [ ] Write unit tests in `tests/test_widgets.py` covering standard data and edge cases
- [ ] Ensure `render_safe()` handles empty or malformed `config/education.yaml` without crashing
- [ ] Register and document the new widget in `docs/WIDGETS.md` and the README widget list

## 💡 Implementation Notes

- Use token-driven colors via `self.theme.get_color(...)` (`primary`, `surface`, `text`, `muted`, `accent`).
- Support type badge pills (e.g. `[DEGREE]` in primary color, `[CERTIFICATION]` in accent color).

## 📚 Resources & Documentation

- **Widget Authoring Guide**: [`docs/WIDGET_AUTHORING.md`](docs/WIDGET_AUTHORING.md)
- **Submit Widget Checklist**: [`docs/community/SUBMIT_WIDGET.md`](docs/community/SUBMIT_WIDGET.md)

---

- **Labels**: `good first issue`, `widget`, `help wanted`
- **Difficulty**: ⭐⭐ Medium
- **Estimated Time**: 4–6 hours
