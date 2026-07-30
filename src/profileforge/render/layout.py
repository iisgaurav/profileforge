from __future__ import annotations

from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.widgets import Card, ProgressBar, Text


class LayoutEngine:
    """Calculates absolute X, Y coordinates and dimensions for all components in the tree."""

    @staticmethod
    def calculate(
        component: Component,
        start_x: int = 0,
        start_y: int = 0,
        parent_width: int | None = None,
        parent_height: int | None = None,
    ):
        component.computed_x = start_x
        component.computed_y = start_y

        w = component.style.width
        h = component.style.height

        # Resolve 'fill' if parent dims are available
        resolved_w = (
            parent_width
            if w == "fill" and parent_width is not None
            else (w if isinstance(w, (int, float)) else 0)
        )
        resolved_h = (
            parent_height
            if h == "fill" and parent_height is not None
            else (h if isinstance(h, (int, float)) else 0)
        )

        if isinstance(component, Spacer):
            component.computed_width = resolved_w
            component.computed_height = resolved_h

        elif isinstance(component, Padding):
            pad = component.value
            child_pw = resolved_w - (pad * 2) if resolved_w else None
            child_ph = resolved_h - (pad * 2) if resolved_h else None

            LayoutEngine.calculate(
                component.child, start_x + pad, start_y + pad, child_pw, child_ph
            )
            component.computed_width = resolved_w or (
                component.child.computed_width + (pad * 2)
            )
            component.computed_height = resolved_h or (
                component.child.computed_height + (pad * 2)
            )

        elif isinstance(component, Column):
            current_y = start_y
            max_w = 0
            for child in component.children:
                LayoutEngine.calculate(child, start_x, current_y, resolved_w, None)
                current_y += child.computed_height + component.spacing
                max_w = max(max_w, child.computed_width)

            component.computed_width = resolved_w or max_w
            component.computed_height = resolved_h or (
                current_y - start_y - (component.spacing if component.children else 0)
            )

            # Align items (cross-axis)
            align = component.style.align or "start"
            if align in ("center", "end"):
                for child in component.children:
                    if align == "center":
                        child.computed_x = (
                            start_x
                            + (component.computed_width - child.computed_width) // 2
                        )
                    elif align == "end":
                        child.computed_x = (
                            start_x + component.computed_width - child.computed_width
                        )

            # Justify content (main-axis)
            justify = component.style.justify or "start"
            if (
                justify in ("center", "end", "space-between")
                and component.computed_height > 0
            ):
                total_children_h = sum(c.computed_height for c in component.children)
                free_space = (
                    component.computed_height
                    - total_children_h
                    - (component.spacing * (len(component.children) - 1))
                )
                if free_space > 0:
                    if justify == "center":
                        offset = free_space // 2
                        for c in component.children:
                            c.computed_y += offset
                    elif justify == "end":
                        for c in component.children:
                            c.computed_y += free_space
                    elif justify == "space-between" and len(component.children) > 1:
                        step = free_space // (len(component.children) - 1)
                        acc = 0
                        for i, c in enumerate(component.children):
                            c.computed_y += acc
                            acc += step

        elif isinstance(component, Row):
            current_x = start_x
            max_h = 0
            for child in component.children:
                LayoutEngine.calculate(child, current_x, start_y, None, resolved_h)
                current_x += child.computed_width + component.spacing
                max_h = max(max_h, child.computed_height)

            component.computed_width = resolved_w or (
                current_x - start_x - (component.spacing if component.children else 0)
            )
            component.computed_height = resolved_h or max_h

            # Align items (cross-axis)
            align = component.style.align or "start"
            if align in ("center", "end"):
                for child in component.children:
                    if align == "center":
                        child.computed_y = (
                            start_y
                            + (component.computed_height - child.computed_height) // 2
                        )
                    elif align == "end":
                        child.computed_y = (
                            start_y + component.computed_height - child.computed_height
                        )

            # Justify content (main-axis)
            justify = component.style.justify or "start"
            if (
                justify in ("center", "end", "space-between")
                and component.computed_width > 0
            ):
                total_children_w = sum(c.computed_width for c in component.children)
                free_space = (
                    component.computed_width
                    - total_children_w
                    - (component.spacing * (len(component.children) - 1))
                )
                if free_space > 0:
                    if justify == "center":
                        offset = free_space // 2
                        for c in component.children:
                            c.computed_x += offset
                    elif justify == "end":
                        for c in component.children:
                            c.computed_x += free_space
                    elif justify == "space-between" and len(component.children) > 1:
                        step = free_space // (len(component.children) - 1)
                        acc = 0
                        for i, c in enumerate(component.children):
                            c.computed_x += acc
                            acc += step

        elif isinstance(component, Text):
            component.computed_width = resolved_w or (len(component.value) * 8)
            component.computed_height = resolved_h or (component.style.font_size or 14)

        elif isinstance(component, ProgressBar):
            component.computed_width = resolved_w or 300
            component.computed_height = resolved_h or 8

        elif isinstance(component, Card):
            title_offset = 50
            child_pw = resolved_w - 40 if resolved_w else None
            child_ph = resolved_h - title_offset - 20 if resolved_h else None

            LayoutEngine.calculate(
                component.child, start_x, start_y + title_offset, child_pw, child_ph
            )
            component.computed_width = resolved_w or (
                component.child.computed_width + 40
            )
            component.computed_height = resolved_h or (
                component.child.computed_height + title_offset + 20
            )

        # Enforce hard width/height if explicitly provided via style properties
        if component.style.width is not None and component.style.width != "fill":
            component.computed_width = component.style.width
        if component.style.height is not None and component.style.height != "fill":
            component.computed_height = component.style.height
