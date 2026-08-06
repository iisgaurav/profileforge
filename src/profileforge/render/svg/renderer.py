import html
from typing import List, Tuple

from profileforge.components.layout import Column, Component, Padding, Row, Spacer, Wrap, Inline, Grid, Stack
from profileforge.components.widgets import (
    Badge,
    Card,
    CircularMetric,
    Divider,
    Icon,
    Metric,
    MetricGroup,
    ProgressBar,
    ProgressMetric,
    Text,
)
from profileforge.render.base import Renderer, RenderNode
from profileforge.core.models import TypographyRole, HorizontalAlign, VerticalAlign, PercentageDisplay
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

    def get_typography_size(self, role_or_int: TypographyRole | int | None) -> int:
        if isinstance(role_or_int, int):
            return role_or_int
        if isinstance(role_or_int, TypographyRole):
            return getattr(self.typography, role_or_int.value, 14)
        return self.typography.body

    def get_defs(self) -> str:
        primary = self.get_color("primary")
        accent = self.get_color("accent")
        surface = self.get_color("surface")
        border = self.get_color("border")
        muted = self.get_color("muted")

        badge_grads = []
        for i, (fg, _) in enumerate(TECH_COLORS):
            badge_grads.append(f"""  <linearGradient id="pf-badge-{i}" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{fg}" stop-opacity="0.25"/>
    <stop offset="100%" stop-color="{fg}" stop-opacity="0.1"/>
  </linearGradient>""")
        badge_grad_xml = "\n".join(badge_grads)

        glow_filter = ""
        if self.context.effects.glow != "none" and self.context.capabilities.supports_filters:
            glow_filter = """
  <filter id="pf-glow" x="-5%" y="-100%" width="110%" height="300%">
    <feGaussianBlur stdDeviation="1.5" result="blur"/>
    <feComposite in="SourceGraphic" in2="blur" operator="over"/>
  </filter>"""

        shadow_filter = ""
        if self.context.effects.shadow != "none" and self.context.capabilities.supports_filters:
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

    def render(self, root_node: RenderNode) -> str:
        """Entrypoint for the Render Pass Pipeline."""
        # Pass 1: Definitions
        defs = self.get_defs()
        
        # Pass 2 -> N: Traversal
        badge_idx = [0]
        body = self._render_node(root_node, badge_idx)
        
        w, h = root_node.width, root_node.height
        return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
{defs}
{body}
</svg>"""

    def _render_node(self, node: RenderNode, badge_idx: List[int]) -> str:
        component = node.component
        x, y, w, h = node.x, node.y, node.width, node.height

        if isinstance(component, Card):
            child_svg = "\n".join(self._render_node(c, badge_idx) for c in node.children)
            radius = component.style.border_radius or getattr(self.theme.radius, "card", 10)
            text_color = self.get_color("text")
            primary = self.get_color("primary")
            escaped_title = html.escape(component.title)

            if escaped_title:
                accent_bar = f'<rect x="{x + 24}" y="{y + 24}" width="4" height="20" rx="2" fill="{primary}" opacity="0.9"/>'
                title_el = (
                    f'<text x="{x + 36}" y="{y + 40}" '
                    f'font-family="{self.typography.font_family}" '
                    f'font-size="{self.typography.heading}" '
                    f'font-weight="700" fill="{text_color}" '
                    f'letter-spacing="0.3">{escaped_title}</text>'
                )
                sep = (
                    f'<line x1="{x + 24}" y1="{y + 60}" x2="{x + w - 24}" y2="{y + 60}" '
                    f'stroke="{primary}" stroke-width="0.5" stroke-opacity="0.25"/>'
                )
            else:
                accent_bar = title_el = sep = ""

            bg_fill = "url(#pf-card-gradient)" if component.style.variant == "hero" else "url(#pf-card-bg)"
            filter_attr = ' filter="url(#pf-shadow)"' if self.context.effects.shadow != "none" else ""

            return f"""<g role="group"{filter_attr} data-pf-id="{node.debug.get('id', '')}">
    <rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" fill="{bg_fill}" stroke="url(#pf-card-border)" stroke-width="1" rx="{radius}"/>
    {accent_bar}
    {title_el}
    {sep}
    {child_svg}
</g>"""

        elif isinstance(component, Icon):
            color = self.get_color(component.style.color or "primary")
            path = IconRegistry.get(component.svg_path) or component.svg_path
            return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 16 16" fill="{color}" data-pf-id="{node.debug.get('id', '')}">{path}</svg>'

        elif isinstance(component, Metric):
            bg_fill = "url(#pf-card-bg)"
            radius = getattr(self.theme.radius, "card", 10)
            text_color = self.get_color("text")
            muted = self.get_color("muted")
            primary = self.get_color("primary")
            escaped_label = html.escape(component.label)
            
            try:
                formatted_value = f"{int(component.value):,}"
            except ValueError:
                formatted_value = html.escape(str(component.value))

            icon_svg = ""
            label_x = x + 16
            if component.icon:
                path = IconRegistry.get(component.icon) or component.icon
                icon_svg = f'<svg x="{x + 16}" y="{y + 16}" width="18" height="18" viewBox="0 0 16 16" fill="{primary}">{path}</svg>'
                label_x += 18 + self.spacing.optical.text_icon

            filter_attr = ' filter="url(#pf-shadow)"' if self.context.effects.shadow != "none" else ""
            trend_svg = ""
            if component.trend is not None:
                trend_color = self.get_color("success") if component.trend > 0 else self.get_color("warning")
                trend_text = f"+{component.trend}%" if component.trend > 0 else f"{component.trend}%"
                trend_svg = f'<text x="{x + w - 16}" y="{y + h - 20}" font-family="{self.typography.font_family}" font-size="{self.typography.small}" font-weight="600" fill="{trend_color}" text-anchor="end">{trend_text}</text>'

            return f"""<g{filter_attr} data-pf-id="{node.debug.get('id', '')}">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg_fill}" stroke="url(#pf-card-border)" stroke-width="1" rx="{radius}"/>
    {icon_svg}
    <text x="{label_x}" y="{y + 30}" font-family="{self.typography.font_family}" font-size="{self.typography.small}" fill="{muted}" font-weight="600">{escaped_label}</text>
    <text x="{x + 16}" y="{y + h - 20}" font-family="{self.typography.font_family}" font-size="{self.typography.value}" font-weight="700" fill="{text_color}">{formatted_value}</text>
    {trend_svg}
</g>"""

        elif isinstance(component, CircularMetric):
            cx, cy = x + w / 2, y + h / 2
            r = min(w, h) / 2 - 8
            progress = min(1.0, component.value / (component.max_value or 1.0))
            circumference = 2 * 3.14159 * r
            dashoffset = circumference * (1 - progress)

            muted = self.get_color("muted")
            primary = self.get_color("primary")
            text_color = self.get_color("text")
            glow_attr = ' filter="url(#pf-glow)"' if self.context.effects.glow != "none" else ""

            icon_svg = ""
            if component.icon:
                path = IconRegistry.get(component.icon) or component.icon
                icon_svg = f'<svg x="{cx - 10}" y="{cy - 24}" width="20" height="20" viewBox="0 0 16 16" fill="{primary}">{path}</svg>'
                
            try:
                formatted_value = f"{int(component.value):,}"
            except ValueError:
                formatted_value = str(int(component.value))

            return f"""<g data-pf-id="{node.debug.get('id', '')}">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{muted}" stroke-width="6" stroke-opacity="0.15"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{primary}" stroke-width="6" stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" transform="rotate(-90 {cx} {cy})" stroke-linecap="round"{glow_attr}>
        <animate attributeName="stroke-dashoffset" from="{circumference}" to="{dashoffset}" dur="1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
    </circle>
    {icon_svg}
    <text x="{cx}" y="{cy + 12}" font-family="{self.typography.font_family}" font-size="{self.typography.heading}" font-weight="700" fill="{text_color}" text-anchor="middle">{formatted_value}</text>
    <text x="{cx}" y="{cy + 28}" font-family="{self.typography.font_family}" font-size="{self.typography.small}" fill="{muted}" text-anchor="middle">{html.escape(component.label)}</text>
</g>"""

        elif isinstance(component, Text):
            color = self.get_color(component.style.color or "text")
            fs = self.get_typography_size(component.style.font_size)
            fw = component.style.font_weight or "normal"
            align = component.style.align or HorizontalAlign.LEFT
            valign = component.style.valign or VerticalAlign.TOP
            escaped_value = html.escape(component.value)

            font_family = self.typography.font_family
            base_attr = f'font-family="{font_family}" font-size="{fs}" font-weight="{fw}" fill="{color}"'

            text_y = y
            if valign in (VerticalAlign.TOP, "top"):
                text_y = y + fs
                dominant = ""
            elif valign in (VerticalAlign.MIDDLE, "middle"):
                text_y = y + h / 2
                dominant = 'dominant-baseline="central"'
            elif valign in (VerticalAlign.BOTTOM, "bottom"):
                text_y = y + h
                dominant = ""
            else:
                text_y = y + fs
                dominant = ""

            if align in (HorizontalAlign.CENTER, "center"):
                return f'<text x="{x + w / 2}" y="{text_y}" {base_attr} text-anchor="middle" {dominant} data-pf-id="{node.debug.get("id", "")}">{escaped_value}</text>'
            elif align in (HorizontalAlign.RIGHT, "end"):
                return f'<text x="{x + w}" y="{text_y}" {base_attr} text-anchor="end" {dominant} data-pf-id="{node.debug.get("id", "")}">{escaped_value}</text>'
            else:
                return f'<text x="{x}" y="{text_y}" {base_attr} {dominant} data-pf-id="{node.debug.get("id", "")}">{escaped_value}</text>'

        elif isinstance(component, ProgressBar):
            filled_w = max(4, (component.progress / 100.0) * w)
            radius = component.style.border_radius or getattr(self.theme.radius, "progress", 4)
            dur_s = 0.6 + (component.progress / 100.0) * 0.8
            glow_attr = ' filter="url(#pf-glow)"' if self.context.effects.glow != "none" else ""

            return f"""<g role="meter" aria-valuenow="{component.progress}" aria-valuemin="0" aria-valuemax="100" data-pf-id="{node.debug.get('id', '')}">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#pf-track-bg)" rx="{radius}"/>
    <rect x="{x}" y="{y}" width="{filled_w}" height="{h}" fill="url(#pf-progress-grad)" rx="{radius}"{glow_attr}>
        <animate attributeName="width" from="0" to="{filled_w}" dur="{dur_s:.2f}s" calcMode="spline" keySplines="0.25 0.1 0.25 1" fill="freeze"/>
    </rect>
</g>"""

        elif isinstance(component, ProgressMetric):
            # Compound component encapsulating Label, Value, ProgressBar
            progress_h = 8
            text_color = self.get_color("text")
            muted = self.get_color("muted")
            font_family = self.typography.font_family
            fs_label = self.typography.label
            fs_value = self.typography.small
            
            label_text = f'<text x="{x}" y="{y + fs_label}" font-family="{font_family}" font-size="{fs_label}" fill="{text_color}">{html.escape(component.label)}</text>'
            pct_text = ""
            if component.display == PercentageDisplay.RIGHT:
                pct_text = f'<text x="{x + w}" y="{y + fs_label}" font-family="{font_family}" font-size="{fs_value}" fill="{muted}" text-anchor="end">{component.value}%</text>'
            
            bar_y = y + fs_label + self.spacing.optical.label_value
            filled_w = max(4, (component.value / 100.0) * w)
            radius = getattr(self.theme.radius, "progress", 4)
            glow_attr = ' filter="url(#pf-glow)"' if self.context.effects.glow != "none" else ""
            
            bar_svg = f"""<g role="meter" aria-valuenow="{component.value}" aria-valuemin="0" aria-valuemax="100">
    <rect x="{x}" y="{bar_y}" width="{w}" height="{progress_h}" fill="url(#pf-track-bg)" rx="{radius}"/>
    <rect x="{x}" y="{bar_y}" width="{filled_w}" height="{progress_h}" fill="url(#pf-progress-grad)" rx="{radius}"{glow_attr}>
        <animate attributeName="width" from="0" to="{filled_w}" dur="1s" calcMode="spline" keySplines="0.25 0.1 0.25 1" fill="freeze"/>
    </rect>
</g>"""
            return f'<g data-pf-id="{node.debug.get("id", "")}">{label_text}{pct_text}{bar_svg}</g>'

        elif isinstance(component, Badge):
            idx = badge_idx[0]
            badge_idx[0] += 1
            fg_color, grad_id = self._badge_color(idx)
            escaped_label = html.escape(component.label)
            br = h // 2

            return f"""<g role="term" data-pf-id="{node.debug.get('id', '')}">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{br}" fill="url(#{grad_id})" stroke="{fg_color}" stroke-width="0.8" stroke-opacity="0.5"/>
    <text x="{x + w / 2}" y="{y + h / 2}" font-family="{self.typography.font_family}" font-size="{self.typography.caption}" fill="{fg_color}" text-anchor="middle" dominant-baseline="central" font-weight="600" letter-spacing="0.3">{escaped_label}</text>
</g>"""

        elif isinstance(component, Divider):
            primary = self.get_color("primary")
            return f'<line x1="{x}" y1="{y + h/2}" x2="{x + w}" y2="{y + h/2}" stroke="{primary}" stroke-width="1" stroke-opacity="{component.opacity}" data-pf-id="{node.debug.get("id", "")}"/>'

        elif isinstance(component, Inline):
            # Special renderer logic for Inline. Renders text + icon using layout hacks (native SVG flow).
            # For simplicity, we just render children with hardcoded internal offset in this pass.
            parts = []
            curr_x = x
            for child_node in node.children:
                child_node_copy = RenderNode(
                    component=child_node.component,
                    x=curr_x,
                    y=y,
                    width=child_node.width,
                    height=child_node.height,
                    children=child_node.children,
                    debug=child_node.debug
                )
                parts.append(self._render_node(child_node_copy, badge_idx))
                # Very rough intrinsic estimation for inline layout within the renderer
                if isinstance(child_node.component, Text):
                    curr_x += len(child_node.component.value) * (self.get_typography_size(child_node.component.style.font_size) * 0.55) + component.gap
                elif isinstance(child_node.component, Icon):
                    curr_x += (child_node.width or 16) + component.gap
                elif isinstance(child_node.component, Badge):
                    curr_x += (child_node.width or 100) + component.gap
            return f'<g data-pf-id="{node.debug.get("id", "")}">' + "".join(parts) + "</g>"

        elif isinstance(component, (Row, Column, Padding, Wrap, Stack, MetricGroup)):
            parts = []
            for child_node in node.children:
                parts.append(self._render_node(child_node, badge_idx))
            return f'<g data-pf-id="{node.debug.get("id", "")}">' + "\n".join(parts) + "</g>"

        elif isinstance(component, Spacer):
            return ""

        return ""
