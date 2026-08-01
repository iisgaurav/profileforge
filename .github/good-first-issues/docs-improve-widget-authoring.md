# [Good First Issue] Add More Examples to WIDGET_AUTHORING.md

## 🌟 Background

`docs/WIDGET_AUTHORING.md` is our primary developer guide for building custom SVG widgets in ProfileForge. Currently, it only contains a single widget example (`ProjectSpotlightWidget`). New contributors would greatly benefit from seeing additional code examples illustrating different widget lifecycle patterns, error handling, and experimental flags.

## 🎯 Task Overview

Add **2 complete, fully functional Python code examples** to `docs/WIDGET_AUTHORING.md`:

### 1. `QuoteWidget` (`WidgetCategory.UTILITY`)
- **Pattern**: Simple fetch, transform, and build pattern using local data.
- **Functionality**: Reads a random inspirational tech quote from `config/quotes.yaml` and renders it inside a styled SVG card with author attribution.
- **Connector**: Uses the `local` file connector.

### 2. `BlogFeedWidget` (`WidgetCategory.CONTENT`)
- **Pattern**: External RSS feed connector (stubbed gracefully) showing error resilience and experimental flagging.
- **Functionality**: Shows how to handle missing external credentials or connectors gracefully, and demonstrates setting `experimental=True` in the `@register_widget` decorator.

## ✅ Acceptance Criteria

- [ ] Two new complete, working Python code examples added to `docs/WIDGET_AUTHORING.md`
- [ ] Both examples include all required widget lifecycle methods:
  - `metadata()`
  - `validate()`
  - `resolve_connectors()`
  - `fetch()`
  - `transform()`
  - `build()`
- [ ] Code strictly follows ProfileForge design standards: no hardcoded CSS colors, uses design token methods (`self.theme.get_color(...)`)
- [ ] Clear prose explaining each step accompanies both examples
- [ ] Existing guide content remains intact with new sections appended logically

## 💡 Technical Code Snippets to Include

### Example 1: `QuoteWidget` Code Snippet

```python
from profileforge.widgets.base import BaseWidget, WidgetCategory, register_widget
from profileforge.core.models import WidgetMetadata
from typing import Dict, Any, List

@register_widget("quote")
class QuoteWidget(BaseWidget):
    """Utility widget rendering a daily or random quote."""

    @classmethod
    def metadata(cls) -> WidgetMetadata:
        return WidgetMetadata(
            id="quote",
            name="Quote Card",
            category=WidgetCategory.UTILITY,
            description="Displays a random or configured inspirational quote.",
            version="1.0.0"
        )

    def validate(self, config: Dict[str, Any]) -> List[str]:
        errors = super().validate(config)
        return errors

    def resolve_connectors(self) -> List[str]:
        return ["local"]

    def fetch(self, connectors: Dict[str, Any]) -> Dict[str, Any]:
        local_conn = connectors.get("local")
        data = local_conn.read_yaml("config/quotes.yaml") if local_conn else {}
        return data

    def transform(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        quotes = raw_data.get("quotes", [{"quote": "Keep pushing code.", "author": "Anonymous"}])
        import random
        selected = random.choice(quotes)
        return {"quote": selected.get("quote"), "author": selected.get("author")}

    def build(self, data: Dict[str, Any]) -> str:
        bg = self.theme.get_color("surface")
        text_color = self.theme.get_color("text")
        accent = self.theme.get_color("accent")
        return f'''<svg width="400" height="120" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="8" fill="{bg}"/>
  <text x="20" y="45" fill="{text_color}" font-size="14" font-style="italic">"{data['quote']}"</text>
  <text x="20" y="85" fill="{accent}" font-size="12" font-weight="bold">— {data['author']}</text>
</svg>'''
```

### Example 2: `BlogFeedWidget` Code Snippet (Experimental / Stubbed RSS)

```python
from profileforge.widgets.base import BaseWidget, WidgetCategory, register_widget
from profileforge.core.models import WidgetMetadata
from typing import Dict, Any, List

@register_widget("blog_feed", experimental=True)
class BlogFeedWidget(BaseWidget):
    """Content widget fetching recent articles via RSS feed (Experimental)."""

    @classmethod
    def metadata(cls) -> WidgetMetadata:
        return WidgetMetadata(
            id="blog_feed",
            name="Blog Feed",
            category=WidgetCategory.CONTENT,
            description="Fetches recent blog posts from an RSS feed.",
            version="0.1.0"
        )

    def validate(self, config: Dict[str, Any]) -> List[str]:
        errors = super().validate(config)
        if "feed_url" not in config:
            errors.append("Missing required field 'feed_url' in blog_feed configuration.")
        return errors

    def resolve_connectors(self) -> List[str]:
        return ["rss"]

    def fetch(self, connectors: Dict[str, Any]) -> Dict[str, Any]:
        rss_conn = connectors.get("rss")
        if not rss_conn:
            # Fallback when RSS connector is unavailable
            return {"posts": [], "error": "RSS connector not initialized"}
        return rss_conn.fetch_posts(self.config.get("feed_url"))

    def transform(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        posts = raw_data.get("posts", [])
        return {"items": posts[:3], "error": raw_data.get("error")}

    def build(self, data: Dict[str, Any]) -> str:
        bg = self.theme.get_color("surface")
        text_color = self.theme.get_color("text")
        if data.get("error"):
            return f'''<svg width="400" height="80" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="8" fill="{bg}"/>
  <text x="20" y="45" fill="{text_color}" font-size="12">Feed unavailable: {data['error']}</text>
</svg>'''
        # Build SVG card list...
        return f'<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" rx="8" fill="{bg}"/></svg>'
```

## 📚 Resources & Documentation

- Target documentation file: [`docs/WIDGET_AUTHORING.md`](docs/WIDGET_AUTHORING.md)

---

- **Labels**: `good first issue`, `documentation`, `help wanted`
- **Difficulty**: ⭐ Easy
- **Estimated Time**: 2–4 hours
