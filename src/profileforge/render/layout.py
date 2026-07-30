from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.widgets import Card, ProgressBar, Text


class LayoutEngine:
    """Calculates absolute X, Y coordinates and dimensions for all components in the tree."""

    @staticmethod
    def calculate(component: Component, start_x: int = 0, start_y: int = 0):
        component.computed_x = start_x
        component.computed_y = start_y

        # Base styles overrides
        w = component.style.width or 0
        h = component.style.height or 0

        if isinstance(component, Spacer):
            component.computed_width = w
            component.computed_height = h

        elif isinstance(component, Padding):
            pad = component.value
            LayoutEngine.calculate(component.child, start_x + pad, start_y + pad)
            component.computed_width = component.child.computed_width + (pad * 2)
            component.computed_height = component.child.computed_height + (pad * 2)

        elif isinstance(component, Column):
            current_y = start_y
            max_w = 0
            for child in component.children:
                LayoutEngine.calculate(child, start_x, current_y)
                current_y += child.computed_height + component.spacing
                max_w = max(max_w, child.computed_width)
            component.computed_width = max_w
            component.computed_height = (
                current_y - start_y - (component.spacing if component.children else 0)
            )

        elif isinstance(component, Row):
            current_x = start_x
            max_h = 0
            for child in component.children:
                LayoutEngine.calculate(child, current_x, start_y)
                current_x += child.computed_width + component.spacing
                max_h = max(max_h, child.computed_height)
            component.computed_width = (
                current_x - start_x - (component.spacing if component.children else 0)
            )
            component.computed_height = max_h

        elif isinstance(component, Text):
            # Very rough estimation of text bounds for layout purposes
            component.computed_width = len(component.value) * 8
            component.computed_height = component.style.font_size or 14

        elif isinstance(component, ProgressBar):
            component.computed_width = component.style.width or 300
            component.computed_height = component.style.height or 8

        elif isinstance(component, Card):
            title_offset = 50
            LayoutEngine.calculate(component.child, start_x, start_y + title_offset)

            card_w = component.style.width or (component.child.computed_width + 40)
            card_h = component.style.height or (
                component.child.computed_height + title_offset + 20
            )

            component.computed_width = card_w
            component.computed_height = card_h

        # Enforce hard width/height styles if provided
        if component.style.width is not None:
            component.computed_width = component.style.width
        if component.style.height is not None:
            component.computed_height = component.style.height
