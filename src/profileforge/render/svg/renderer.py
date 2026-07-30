import html

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.widgets import Badge, Card, ProgressBar, Text
from profileforge.render.base import Renderer


class SVGRenderer(Renderer):
    def get_color(self, color_key: str) -> str:
        return getattr(self.theme.colors, color_key, color_key)

    def get_defs(self) -> str:
        """Return SVG <defs> block with shared gradients and filters for premium visuals."""
        primary = self.get_color("primary")
        accent = self.get_color("accent")
        surface = self.get_color("surface")
        border = self.get_color("border")

        return f"""<defs>
  <!-- Progress bar gradient -->
  <linearGradient id="pf-progress-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.7"/>
    <stop offset="100%" stop-color="{primary}"/>
  </linearGradient>

  <!-- Badge fill gradient -->
  <linearGradient id="pf-badge-grad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="{accent}" stop-opacity="0.08"/>
  </linearGradient>

  <!-- Card border gradient -->
  <linearGradient id="pf-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="{border}" stop-opacity="0.8"/>
  </linearGradient>

  <!-- Card background gradient -->
  <linearGradient id="pf-card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{surface}"/>
    <stop offset="100%" stop-color="{surface}" stop-opacity="0.85"/>
  </linearGradient>

  <!-- Progress bar glow filter -->
  <filter id="pf-progress-glow" x="-5%" y="-80%" width="110%" height="260%">
    <feGaussianBlur stdDeviation="2" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>

  <!-- Card shadow filter -->
  <filter id="pf-card-shadow" x="-3%" y="-3%" width="106%" height="110%">
    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="{primary}" flood-opacity="0.08"/>
  </filter>
</defs>"""

    def render(self, component: Component) -> str:
        x = component.computed_x
        y = component.computed_y
        w = component.computed_width
        h = component.computed_height

        if isinstance(component, Card):
            child_svg = self.render(component.child)
            radius = component.style.border_radius or getattr(self.theme.radius, "card", 8)
            title_color = self.get_color("text")
            primary = self.get_color("primary")

            escaped_title = html.escape(component.title)
            title_tag = f"<title>{escaped_title} Card</title>"
            desc_tag = f"<desc>Card component for {escaped_title}</desc>"

            # Accent line under the title
            accent_line = f'<rect x="{x + 24}" y="{y + 38}" width="32" height="2" rx="1" fill="{primary}" opacity="0.7"/>'

            return f"""
<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="group" filter="url(#pf-card-shadow)">
    {title_tag}
    {desc_tag}
    <rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" fill="url(#pf-card-bg)" stroke="url(#pf-card-border)" stroke-width="1" rx="{radius}"/>
    <text x="{x + 24}" y="{y + 30}" font-family="{self.theme.typography.font_family}" font-size="{self.theme.typography.heading}" font-weight="700" fill="{title_color}" letter-spacing="0.2">{escaped_title}</text>
    {accent_line}
    {child_svg}
</svg>"""

        elif isinstance(component, Text):
            color = self.get_color(component.style.color or "text")
            fs = component.style.font_size or self.theme.typography.body
            fw = component.style.font_weight or "normal"
            escaped_value = html.escape(component.value)

            return f"""
<g role="text">
    <title>Text</title>
    <desc>{escaped_value}</desc>
    <text x="{x}" y="{y + fs}" font-family="{self.theme.typography.font_family}" font-size="{fs}" font-weight="{fw}" fill="{color}">{escaped_value}</text>
</g>"""

        elif isinstance(component, ProgressBar):
            bg = self.get_color("border")
            filled_w = (component.progress / 100.0) * w
            radius = component.style.border_radius or getattr(self.theme.radius, "progress", h / 2)

            return f"""
<g role="meter" aria-valuenow="{component.progress}" aria-valuemin="0" aria-valuemax="100">
    <title>Progress Bar</title>
    <desc>Progress: {component.progress}%</desc>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" rx="{radius}" opacity="0.6"/>
    <rect x="{x}" y="{y}" width="{filled_w}" height="{h}" fill="url(#pf-progress-grad)" rx="{radius}" filter="url(#pf-progress-glow)">
        <animate attributeName="width" from="0" to="{filled_w}" dur="1.1s" calcMode="spline" keySplines="0.4 0 0.2 1" fill="freeze"/>
    </rect>
</g>"""

        elif isinstance(component, Badge):
            primary = self.get_color("primary")
            escaped_label = html.escape(component.label)

            return f"""
<g role="term">
    <title>Badge</title>
    <desc>Badge: {escaped_label}</desc>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}" fill="url(#pf-badge-grad)" stroke="{primary}" stroke-width="0.6" stroke-opacity="0.4"/>
    <text x="{x + w / 2}" y="{y + h / 2}" font-family="{self.theme.typography.font_family}" font-size="12" fill="{primary}" text-anchor="middle" dominant-baseline="central" font-weight="500" letter-spacing="0.2">{escaped_label}</text>
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
