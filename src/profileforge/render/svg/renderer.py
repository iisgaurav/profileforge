import html
from typing import List, Tuple

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.widgets import Badge, Card, ProgressBar, Text
from profileforge.render.base import Renderer

# Tech-specific color palette for badges — makes expertise feel rich and varied
TECH_COLORS: List[Tuple[str, str]] = [
    ("#3B82F6", "#1D3557"),  # blue / deep navy
    ("#10B981", "#064E3B"),  # emerald / dark green
    ("#8B5CF6", "#2E1065"),  # violet / deep purple
    ("#F59E0B", "#451A03"),  # amber / dark orange
    ("#EF4444", "#450A0A"),  # red / dark red
    ("#06B6D4", "#083344"),  # cyan / dark cyan
    ("#EC4899", "#500724"),  # pink / dark pink
    ("#84CC16", "#1A2E05"),  # lime / dark lime
]


class SVGRenderer(Renderer):
    def get_color(self, color_key: str) -> str:
        return getattr(self.theme.colors, color_key, color_key)

    def get_defs(self) -> str:
        """Return SVG <defs> with shared gradients and filters for premium visuals."""
        primary = self.get_color("primary")
        accent = self.get_color("accent")
        surface = self.get_color("surface")
        border = self.get_color("border")
        muted = self.get_color("muted")

        # Build per-badge gradient defs
        badge_grads = []
        for i, (fg, bg_dark) in enumerate(TECH_COLORS):
            badge_grads.append(f"""  <linearGradient id="pf-badge-{i}" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{fg}" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="{fg}" stop-opacity="0.1"/>
  </linearGradient>""")
        badge_grad_xml = "\n".join(badge_grads)

        return f"""<defs>
  <!-- Animated gradient for progress bar fill -->
  <linearGradient id="pf-progress-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.75"/>
    <stop offset="70%" stop-color="{primary}"/>
    <stop offset="100%" stop-color="{accent}" stop-opacity="0.9"/>
  </linearGradient>

  <!-- Card border: subtle blue-to-transparent gradient -->
  <linearGradient id="pf-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.6"/>
    <stop offset="60%" stop-color="{border}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{border}" stop-opacity="0.4"/>
  </linearGradient>

  <!-- Card background: very subtle top-to-bottom gradient -->
  <linearGradient id="pf-card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{surface}" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="{surface}" stop-opacity="0.8"/>
  </linearGradient>

  <!-- Card background: Hero vibrant gradient -->
  <linearGradient id="pf-card-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#3b0918"/>
    <stop offset="50%" stop-color="#1e1333"/>
    <stop offset="100%" stop-color="#091629"/>
  </linearGradient>

  <!-- Glow for progress bar fill -->
  <filter id="pf-progress-glow" x="-5%" y="-100%" width="110%" height="300%">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>

  <!-- Soft drop shadow for cards -->
  <filter id="pf-card-shadow" x="-4%" y="-4%" width="108%" height="114%">
    <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="{primary}" flood-opacity="0.07"/>
  </filter>

  <!-- Progress bar track background -->
  <linearGradient id="pf-track-bg" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{muted}" stop-opacity="0.15"/>
    <stop offset="100%" stop-color="{muted}" stop-opacity="0.08"/>
  </linearGradient>

{badge_grad_xml}
</defs>"""

    def _badge_color(self, index: int) -> Tuple[str, str]:
        """Return (fg_color, grad_id) for badge at given index."""
        fg, _ = TECH_COLORS[index % len(TECH_COLORS)]
        return fg, f"pf-badge-{index % len(TECH_COLORS)}"

    def render(self, component: Component, _badge_idx: List[int] = None) -> str:
        if _badge_idx is None:
            _badge_idx = [0]

        x = component.computed_x
        y = component.computed_y
        w = component.computed_width
        h = component.computed_height

        if isinstance(component, Card):
            child_svg = self.render(component.child, _badge_idx)
            radius = component.style.border_radius or getattr(
                self.theme.radius, "card", 10
            )
            text_color = self.get_color("text")
            primary = self.get_color("primary")

            escaped_title = html.escape(component.title)

            # Only render header elements if the card has a title
            if escaped_title:
                accent_bar = f'<rect x="{x + 20}" y="{y + 16}" width="3" height="20" rx="1.5" fill="{primary}" opacity="0.9"/>'
                title_el = (
                    f'<text x="{x + 32}" y="{y + 31}" '
                    f'font-family="{self.theme.typography.font_family}" '
                    f'font-size="{self.theme.typography.heading}" '
                    f'font-weight="700" fill="{text_color}" '
                    f'letter-spacing="0.3">{escaped_title}</text>'
                )
                sep = (
                    f'<line x1="{x + 20}" y1="{y + 44}" x2="{x + w - 20}" y2="{y + 44}" '
                    f'stroke="{primary}" stroke-width="0.5" stroke-opacity="0.25"/>'
                )
            else:
                accent_bar = title_el = sep = ""

            bg_fill = (
                "url(#pf-card-gradient)"
                if component.style.variant == "hero"
                else "url(#pf-card-bg)"
            )

            return f"""
<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="group" filter="url(#pf-card-shadow)">
    <title>{escaped_title} Card</title>
    <desc>Card component for {escaped_title}</desc>
    <rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" fill="{bg_fill}" stroke="url(#pf-card-border)" stroke-width="1" rx="{radius}"/>
    {accent_bar}
    {title_el}
    {sep}
    {child_svg}
</svg>"""

        elif isinstance(component, Text):
            color = self.get_color(component.style.color or "text")
            fs = component.style.font_size or self.theme.typography.body
            fw = component.style.font_weight or "normal"
            escaped_value = html.escape(component.value)

            return (
                f'<text x="{x}" y="{y + fs}" '
                f'font-family="{self.theme.typography.font_family}" '
                f'font-size="{fs}" font-weight="{fw}" fill="{color}">{escaped_value}</text>'
            )

        elif isinstance(component, ProgressBar):
            filled_w = max(4, (component.progress / 100.0) * w)
            radius = component.style.border_radius or getattr(
                self.theme.radius, "progress", 4
            )
            dur_s = 0.6 + (component.progress / 100.0) * 0.8

            return f"""
<g role="meter" aria-valuenow="{component.progress}" aria-valuemin="0" aria-valuemax="100">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pf-track-bg)" rx="{radius}"/>
    <rect x="{x}" y="{y}" width="{filled_w}" height="{h}" fill="url(#pf-progress-grad)" rx="{radius}" filter="url(#pf-progress-glow)">
        <animate attributeName="width" from="0" to="{filled_w}" dur="{dur_s:.2f}s" calcMode="spline" keySplines="0.25 0.1 0.25 1" fill="freeze"/>
    </rect>
</g>"""

        elif isinstance(component, Badge):
            idx = _badge_idx[0]
            _badge_idx[0] += 1
            fg_color, grad_id = self._badge_color(idx)
            escaped_label = html.escape(component.label)
            br = h // 2

            return f"""
<g role="term">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{br}" fill="url(#{grad_id})" stroke="{fg_color}" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="{x + w / 2}" y="{y + h / 2}" font-family="{self.theme.typography.font_family}" font-size="12" fill="{fg_color}" text-anchor="middle" dominant-baseline="central" font-weight="600" letter-spacing="0.3">{escaped_label}</text>
</g>"""

        elif isinstance(component, (Row, Column, Padding)):
            parts = []
            if hasattr(component, "children"):
                for c in component.children:
                    parts.append(self.render(c, _badge_idx))
            elif hasattr(component, "child"):
                parts.append(self.render(component.child, _badge_idx))
            return "\n".join(parts)

        elif isinstance(component, Spacer):
            return ""

        return ""
