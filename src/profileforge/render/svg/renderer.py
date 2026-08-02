import html
from typing import List, Tuple

from profileforge.components.layout import Column, Component, Padding, Row, Spacer, Wrap
from profileforge.components.widgets import (
    Badge,
    Card,
    CircularMetric,
    Divider,
    Icon,
    Metric,
    MetricGroup,
    ProgressBar,
    Text,
)
from profileforge.render.base import Renderer
from profileforge.services.icons import IconRegistry

TECH_COLORS: List[Tuple[str, str]] = [
    ("#3B82F6", "#1D3557"),
    ("#10B981", "#064E3B"),
    ("#8B5CF6", "#2E1065"),
    ("#F59E0B", "#451A03"),
    ("#EF4444", "#450A0A"),
    ("#06B6D4", "#083344"),
    ("#EC4899", "#500724"),
    ("#84CC16", "#1A2E05"),
]


class SVGRenderer(Renderer):
    def get_color(self, color_key: str) -> str:
        return getattr(self.theme.colors, color_key, color_key)

    def get_defs(self) -> str:
        primary = self.get_color("primary")
        accent = self.get_color("accent")
        surface = self.get_color("surface")
        border = self.get_color("border")
        muted = self.get_color("muted")

        badge_grads = []
        for i, (fg, bg_dark) in enumerate(TECH_COLORS):
            badge_grads.append(f"""  <linearGradient id="pf-badge-{i}" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{fg}" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="{fg}" stop-opacity="0.1"/>
  </linearGradient>""")
        badge_grad_xml = "\n".join(badge_grads)

        glow_filter = ""
        if self.theme.effects.glow != "none":
            glow_filter = """
  <filter id="pf-glow" x="-5%" y="-100%" width="110%" height="300%">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>"""

        shadow_filter = ""
        if self.theme.effects.shadow != "none":
            shadow_filter = f"""
  <filter id="pf-shadow" x="-4%" y="-4%" width="108%" height="114%">
    <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="{primary}" flood-opacity="0.07"/>
  </filter>"""

        return f"""<defs>
  <linearGradient id="pf-progress-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.75"/>
    <stop offset="70%" stop-color="{primary}"/>
    <stop offset="100%" stop-color="{accent}" stop-opacity="0.9"/>
  </linearGradient>

  <linearGradient id="pf-card-border" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{primary}" stop-opacity="0.6"/>
    <stop offset="60%" stop-color="{border}" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="{border}" stop-opacity="0.4"/>
  </linearGradient>

  <linearGradient id="pf-card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{surface}" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="{surface}" stop-opacity="0.8"/>
  </linearGradient>

  <linearGradient id="pf-card-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#3b0918"/>
    <stop offset="50%" stop-color="#1e1333"/>
    <stop offset="100%" stop-color="#091629"/>
  </linearGradient>

  <linearGradient id="pf-track-bg" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{muted}" stop-opacity="0.15"/>
    <stop offset="100%" stop-color="{muted}" stop-opacity="0.08"/>
  </linearGradient>
{glow_filter}
{shadow_filter}
{badge_grad_xml}
</defs>"""

    def _badge_color(self, index: int) -> Tuple[str, str]:
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

            if escaped_title:
                accent_bar = f'<rect x="{x + 24}" y="{y + 24}" width="4" height="20" rx="2" fill="{primary}" opacity="0.9"/>'
                title_el = (
                    f'<text x="{x + 36}" y="{y + 40}" '
                    f'font-family="{self.theme.typography.font_family}" '
                    f'font-size="{self.theme.typography.heading}" '
                    f'font-weight="700" fill="{text_color}" '
                    f'letter-spacing="0.3">{escaped_title}</text>'
                )
                sep = (
                    f'<line x1="{x + 24}" y1="{y + 60}" x2="{x + w - 24}" y2="{y + 60}" '
                    f'stroke="{primary}" stroke-width="0.5" stroke-opacity="0.25"/>'
                )
            else:
                accent_bar = title_el = sep = ""

            bg_fill = (
                "url(#pf-card-gradient)"
                if component.style.variant == "hero"
                else "url(#pf-card-bg)"
            )
            filter_attr = (
                ' filter="url(#pf-shadow)"'
                if self.theme.effects.shadow != "none"
                else ""
            )

            return f"""
<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="group"{filter_attr}>
    <title>{escaped_title} Card</title>
    <desc>Card component for {escaped_title}</desc>
    <rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" fill="{bg_fill}" stroke="url(#pf-card-border)" stroke-width="1" rx="{radius}"/>
    {accent_bar}
    {title_el}
    {sep}
    {child_svg}
</svg>"""

        elif isinstance(component, Icon):
            color = self.get_color(component.style.color or "primary")
            path = IconRegistry.get(component.svg_path)
            if not path:
                path = component.svg_path  # Use directly if not in registry
            return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 16 16" fill="{color}">{path}</svg>'

        elif isinstance(component, Metric):
            bg_fill = "url(#pf-card-bg)"
            radius = getattr(self.theme.radius, "card", 10)
            text_color = self.get_color("text")
            muted = self.get_color("muted")
            primary = self.get_color("primary")
            escaped_label = html.escape(component.label)
            escaped_value = html.escape(str(component.value))
            
            try:
                formatted_value = f"{int(component.value):,}"
            except ValueError:
                formatted_value = escaped_value

            icon_svg = ""
            label_x = x + 16
            if component.icon:
                path = IconRegistry.get(component.icon) or component.icon
                icon_svg = f'<svg x="{x + 16}" y="{y + 16}" width="18" height="18" viewBox="0 0 16 16" fill="{primary}">{path}</svg>'
                label_x += 18 + 10

            filter_attr = (
                ' filter="url(#pf-shadow)"'
                if self.theme.effects.shadow != "none"
                else ""
            )

            trend_svg = ""
            if component.trend is not None:
                trend_color = (
                    self.get_color("success")
                    if component.trend > 0
                    else self.get_color("warning")
                )
                trend_text = (
                    f"+{component.trend}%"
                    if component.trend > 0
                    else f"{component.trend}%"
                )
                trend_svg = f'<text x="{x + w - 16}" y="{y + h - 20}" font-family="{self.theme.typography.font_family}" font-size="{self.theme.typography.small}" font-weight="600" fill="{trend_color}" text-anchor="end">{trend_text}</text>'

            return f"""
<g{filter_attr}>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg_fill}" stroke="url(#pf-card-border)" stroke-width="1" rx="{radius}"/>
    {icon_svg}
    <text x="{label_x}" y="{y + 30}" font-family="{self.theme.typography.font_family}" font-size="{self.theme.typography.small}" fill="{muted}" font-weight="600">{escaped_label}</text>
    <text x="{x + 16}" y="{y + h - 20}" font-family="{self.theme.typography.font_family}" font-size="{self.theme.typography.heading}" font-weight="700" fill="{text_color}">{formatted_value}</text>
    {trend_svg}
</g>"""

        elif isinstance(component, CircularMetric):
            cx = x + w / 2
            cy = y + h / 2
            r = min(w, h) / 2 - 8

            progress = min(1.0, component.value / (component.max_value or 1.0))
            circumference = 2 * 3.14159 * r
            dashoffset = circumference * (1 - progress)

            muted = self.get_color("muted")
            primary = self.get_color("primary")
            text_color = self.get_color("text")

            glow_attr = (
                ' filter="url(#pf-glow)"' if self.theme.effects.glow != "none" else ""
            )

            icon_svg = ""
            if component.icon:
                path = IconRegistry.get(component.icon) or component.icon
                icon_svg = f'<svg x="{cx - 10}" y="{cy - 24}" width="20" height="20" viewBox="0 0 16 16" fill="{primary}">{path}</svg>'
                
            try:
                formatted_value = f"{int(component.value):,}"
            except ValueError:
                formatted_value = str(int(component.value))

            return f"""
<g>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{muted}" stroke-width="6" stroke-opacity="0.15"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{primary}" stroke-width="6" stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" transform="rotate(-90 {cx} {cy})" stroke-linecap="round"{glow_attr}>
        <animate attributeName="stroke-dashoffset" from="{circumference}" to="{dashoffset}" dur="1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
    </circle>
    {icon_svg}
    <text x="{cx}" y="{cy + 12}" font-family="{self.theme.typography.font_family}" font-size="{self.theme.typography.heading}" font-weight="700" fill="{text_color}" text-anchor="middle">{formatted_value}</text>
    <text x="{cx}" y="{cy + 28}" font-family="{self.theme.typography.font_family}" font-size="{self.theme.typography.small}" fill="{muted}" text-anchor="middle">{html.escape(component.label)}</text>
</g>"""

        elif isinstance(component, Text):
            color = self.get_color(component.style.color or "text")
            fs = component.style.font_size or self.theme.typography.body
            fw = component.style.font_weight or "normal"
            escaped_value = html.escape(component.value)

            return f'<text x="{x}" y="{y + fs}" font-family="{self.theme.typography.font_family}" font-size="{fs}" font-weight="{fw}" fill="{color}">{escaped_value}</text>'

        elif isinstance(component, ProgressBar):
            filled_w = max(4, (component.progress / 100.0) * w)
            radius = component.style.border_radius or getattr(
                self.theme.radius, "progress", 4
            )
            dur_s = 0.6 + (component.progress / 100.0) * 0.8
            glow_attr = (
                ' filter="url(#pf-glow)"' if self.theme.effects.glow != "none" else ""
            )

            return f"""
<g role="meter" aria-valuenow="{component.progress}" aria-valuemin="0" aria-valuemax="100">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pf-track-bg)" rx="{radius}"/>
    <rect x="{x}" y="{y}" width="{filled_w}" height="{h}" fill="url(#pf-progress-grad)" rx="{radius}"{glow_attr}>
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

        elif isinstance(component, Divider):
            primary = self.get_color("primary")
            return f'<line x1="{x}" y1="{y + h/2}" x2="{x + w}" y2="{y + h/2}" stroke="{primary}" stroke-width="1" stroke-opacity="{component.opacity}"/>'

        elif isinstance(component, MetricGroup):
            parts = []
            for c in component.metrics:
                parts.append(self.render(c, _badge_idx))
            return "\n".join(parts)

        elif isinstance(component, (Row, Column, Padding, Wrap)):
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
