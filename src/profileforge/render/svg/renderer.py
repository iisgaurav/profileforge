from profileforge.core.context import BuildContext
from profileforge.components.layout import Component, Row, Column, Padding, Spacer
from profileforge.components.widgets import Card, Text, ProgressBar, Icon

class SVGRenderer:
    def __init__(self, context: BuildContext):
        self.theme = context.theme

    def get_color(self, color_key: str) -> str:
        # Resolve keys like "primary", "background" to theme values, or use raw hex if not found
        return getattr(self.theme, color_key, color_key)

    def render(self, component: Component) -> str:
        # The components already have computed_x, computed_y, computed_width, computed_height
        x = component.computed_x
        y = component.computed_y
        w = component.computed_width
        h = component.computed_height

        if isinstance(component, Card):
            child_svg = self.render(component.child)
            bg = self.get_color("background")
            border = self.get_color("border")
            title_color = self.get_color("text")
            
            return f"""
<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .card-bg {{ fill: {bg}; stroke: {border}; stroke-width: 1px; rx: 6px; }}
        .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 600; fill: {title_color}; }}
    </style>
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" class="card-bg" />
    <text x="25" y="35" class="title">{component.title}</text>
    {child_svg}
</svg>"""

        elif isinstance(component, Text):
            color = self.get_color(component.style.color or "text")
            fs = component.style.font_size or 14
            fw = component.style.font_weight or "normal"
            return f'<text x="{x}" y="{y + fs}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="{fs}" font-weight="{fw}" fill="{color}">{component.value}</text>'

        elif isinstance(component, ProgressBar):
            bg = self.get_color("progress_bg")
            fill = self.get_color("primary")
            filled_w = (component.progress / 100.0) * w
            radius = h / 2
            return f"""
<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}" rx="{radius}" />
<rect x="{x}" y="{y}" width="{filled_w}" height="{h}" fill="{fill}" rx="{radius}" />"""

        elif isinstance(component, (Row, Column, Padding)):
            # These are purely structural, just render their children
            children_svgs = []
            if hasattr(component, 'children'):
                children_svgs = [self.render(c) for c in component.children]
            elif hasattr(component, 'child'):
                children_svgs = [self.render(component.child)]
            return "\\n".join(children_svgs)

        elif isinstance(component, Spacer):
            return "" # Spacers just take up space in the layout engine

        return ""
