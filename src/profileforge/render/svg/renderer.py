import html

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.widgets import Badge, Card, ProgressBar, Text
from profileforge.render.base import Renderer


class SVGRenderer(Renderer):
    def get_color(self, color_key: str) -> str:
        # Resolve keys from theme.colors, or use raw hex if not found
        return getattr(self.theme.colors, color_key, color_key)

    def _get_filter_def(self, elevation: str) -> str:
        shadow_val = getattr(self.theme.shadows, elevation, None)
        if not shadow_val or shadow_val == "none":
            return ""

        # Simple heuristic to extract blur and color from something like "0 4px 6px rgba(0,0,0,0.1)"
        # For full implementation, one would parse the shadow string.
        # But we can just use CSS drop-shadow in a style block instead of raw SVG filters for simplicity.
        return ""

    def render(self, component: Component) -> str:
        # The components already have computed_x, computed_y, computed_width, computed_height
        x = component.computed_x
        y = component.computed_y
        w = component.computed_width
        h = component.computed_height

        if isinstance(component, Card):
            child_svg = self.render(component.child)
            bg = self.get_color(component.style.background_color or "surface")
            border = self.get_color(component.style.border_color or "border")
            title_color = self.get_color("text")
            radius = component.style.border_radius or getattr(
                self.theme.radius, "card", 6
            )

            elevation = component.style.elevation or "none"
            shadow_css = getattr(self.theme.shadows, elevation, "none")

            filter_css = ""
            if shadow_css != "none":
                filter_css = f"filter: drop-shadow({shadow_css});"

            escaped_title = html.escape(component.title)
            title_tag = f"<title>{escaped_title} Card</title>"
            desc_tag = f"<desc>Card component for {escaped_title}</desc>"

            return f"""
<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="group">
    {title_tag}
    {desc_tag}
    <style>
        .card-bg {{ fill: {bg}; stroke: {border}; stroke-width: 1px; rx: {radius}px; {filter_css} }}
        .title {{ font-family: {self.theme.typography.font_family}; font-size: {self.theme.typography.heading}px; font-weight: 600; fill: {title_color}; }}
        text {{ -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; text-rendering: optimizeLegibility; }}
    </style>
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" class="card-bg" />
    <text x="24" y="32" class="title">{escaped_title}</text>
    {child_svg}
</svg>"""

        elif isinstance(component, Text):
            color = self.get_color(component.style.color or "text")
            fs = component.style.font_size or self.theme.typography.body
            fw = component.style.font_weight or "normal"
            escaped_value = html.escape(component.value)

            title_tag = "<title>Text</title>"
            desc_tag = f"<desc>{escaped_value}</desc>"

            return f"""
<g role="text">
    {title_tag}
    {desc_tag}
    <text x="{x}" y="{y + fs}" font-family="{self.theme.typography.font_family}" font-size="{fs}" font-weight="{fw}" fill="{color}">{escaped_value}</text>
</g>"""

        elif isinstance(component, ProgressBar):
            bg = self.get_color("surface")
            fill = self.get_color(component.style.color or "primary")
            filled_w = (component.progress / 100.0) * w
            radius = component.style.border_radius or getattr(
                self.theme.radius, "progress", h / 2
            )

            title_tag = "<title>Progress Bar</title>"
            desc_tag = f"<desc>Progress: {component.progress}%</desc>"

            return f"""
<g role="meter" aria-valuenow="{component.progress}" aria-valuemin="0" aria-valuemax="100">
    {title_tag}
    {desc_tag}
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" rx="{radius}" />
    <rect x="{x}" y="{y}" width="{filled_w}" height="{h}" fill="{fill}" rx="{radius}" />
</g>"""

        elif isinstance(component, Badge):
            primary = self.get_color("primary")
            escaped_label = html.escape(component.label)

            title_tag = "<title>Badge</title>"
            desc_tag = f"<desc>Badge: {escaped_label}</desc>"

            return f"""
<g role="term">
    {title_tag}
    {desc_tag}
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{primary}" fill-opacity="0.15" />
    <text x="{x + w / 2}" y="{y + h / 2}" font-family="{self.theme.typography.font_family}" font-size="12" fill="{primary}" text-anchor="middle" dominant-baseline="central">{escaped_label}</text>
</g>"""

        elif isinstance(component, (Row, Column, Padding)):
            children_svgs = []
            if hasattr(component, "children"):
                children_svgs = [self.render(c) for c in component.children]
            elif hasattr(component, "child"):
                children_svgs = [self.render(component.child)]
            return "\n".join(children_svgs)

        elif isinstance(component, Spacer):
            return ""

        return ""
