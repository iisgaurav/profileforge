# [Good First Issue] Add Search/Filter to ProfileForge Studio

## 🌟 Background

ProfileForge Studio (`web/index.html`) currently renders all 11 widgets and 17 themes in a single static gallery list without filtering. As the widget ecosystem grows, real-time search and filtering are necessary to improve discoverability.

## 🎯 Key Features Required

1. **Text Search Input**: Real-time debounced filtering of widget cards by widget name, ID, or tag keyword.
2. **Category Filter Buttons**: Interactive filter pill buttons corresponding to each `WidgetCategory`:
   - `Identity`
   - `Stats`
   - `Career`
   - `Projects`
   - `Development`
   - `Social`
   - `Utility`
   - `Content`
3. **Clear Filter Button**: Resets text query and active category buttons to display all widgets.
4. **Theme Filter Compatibility**: Maintain full compatibility with existing theme selection dropdowns.

## ⚠️ Technical Constraints

- **Vanilla JavaScript only**: No external libraries (React, Vue, jQuery, Tailwind JS) are permitted.
- **Serverless execution**: Must function when loading `web/index.html` directly via the `file://` protocol.
- **Accessibility**: All filter buttons and inputs must be tab-navigable with clear ARIA states.

## ✅ Acceptance Criteria

- [ ] Real-time text search filters widget cards smoothly with ~300ms debouncing
- [ ] Category buttons filter widget cards accurately, supporting single or multi-select states
- [ ] Clear button resets search inputs and restores full list view
- [ ] Tested and functional on Chrome 120+, Firefox 120+, and Safari 17+
- [ ] Existing theme switching and preview functions remain intact
- [ ] **Bonus**: Filter state synchronizes with URL location hash (`#category=stats&q=github`) for link sharing

---

- **Labels**: `good first issue`, `studio`, `frontend`, `help wanted`
- **Difficulty**: ⭐⭐ Medium
- **Estimated Time**: 3–5 hours
