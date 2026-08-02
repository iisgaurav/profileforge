from __future__ import annotations

from typing import Optional

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


class LayoutEngine:
    """Calculates absolute X, Y coordinates and dimensions for all components in the tree."""

    @staticmethod
    def shift(component: Component, dx: int, dy: int):
        if dx == 0 and dy == 0:
            return
        component.computed_x += dx
        component.computed_y += dy
        if hasattr(component, "child") and component.child:
            LayoutEngine.shift(component.child, dx, dy)
        if hasattr(component, "children") and component.children:
            for child in component.children:
                LayoutEngine.shift(child, dx, dy)
        if hasattr(component, "metrics") and component.metrics:
            for child in component.metrics:
                LayoutEngine.shift(child, dx, dy)

    @staticmethod
    def calculate(
        component: Component,
        start_x: int = 0,
        start_y: int = 0,
        parent_width: Optional[int] = None,
        parent_height: Optional[int] = None,
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
                        target_x = (
                            start_x
                            + (component.computed_width - child.computed_width) // 2
                        )
                    elif align == "end":
                        target_x = (
                            start_x + component.computed_width - child.computed_width
                        )

                    if target_x != child.computed_x:
                        LayoutEngine.shift(child, target_x - child.computed_x, 0)

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
                            LayoutEngine.shift(c, 0, offset)
                    elif justify == "end":
                        for c in component.children:
                            LayoutEngine.shift(c, 0, free_space)
                    elif justify == "space-between" and len(component.children) > 1:
                        step = free_space // (len(component.children) - 1)
                        acc = 0
                        for i, c in enumerate(component.children):
                            LayoutEngine.shift(c, 0, acc)
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
                        target_y = (
                            start_y
                            + (component.computed_height - child.computed_height) // 2
                        )
                    elif align == "end":
                        target_y = (
                            start_y + component.computed_height - child.computed_height
                        )

                    if target_y != child.computed_y:
                        LayoutEngine.shift(child, 0, target_y - child.computed_y)

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
                            LayoutEngine.shift(c, offset, 0)
                    elif justify == "end":
                        for c in component.children:
                            LayoutEngine.shift(c, free_space, 0)
                    elif justify == "space-between" and len(component.children) > 1:
                        step = free_space // (len(component.children) - 1)
                        acc = 0
                        for i, c in enumerate(component.children):
                            LayoutEngine.shift(c, acc, 0)
                            acc += step

        elif isinstance(component, Wrap):
            current_x = start_x
            current_y = start_y
            max_h_in_run = 0
            max_w = 0

            for child in component.children:
                # Pre-calculate to get child dimensions
                LayoutEngine.calculate(child, 0, 0, None, None)
                cw = child.computed_width
                ch = child.computed_height

                # Check wrap condition
                if (
                    resolved_w
                    and (current_x + cw - start_x > resolved_w)
                    and current_x > start_x
                ):
                    current_x = start_x
                    current_y += max_h_in_run + component.run_spacing
                    max_h_in_run = 0

                # Assign actual positions
                child.computed_x = current_x
                child.computed_y = current_y

                # Advance layout engine over the child (recursive recalculation not needed if dimensions are fixed, but let's do it to set absolute coords for its children)
                LayoutEngine.calculate(child, current_x, current_y, None, None)

                current_x += cw + component.spacing
                max_w = max(max_w, current_x - start_x - component.spacing)
                max_h_in_run = max(max_h_in_run, ch)

            component.computed_width = resolved_w or max_w
            component.computed_height = resolved_h or (
                current_y - start_y + max_h_in_run
            )

        elif isinstance(component, Text):
            fs = component.style.font_size or 14
            component.computed_width = resolved_w or int(
                len(component.value) * (fs * 0.55)
            )
            component.computed_height = resolved_h or fs

        elif isinstance(component, ProgressBar):
            component.computed_width = resolved_w or 300
            component.computed_height = resolved_h or 8

        elif isinstance(component, Divider):
            component.computed_width = resolved_w or 400
            component.computed_height = resolved_h or 1

        elif isinstance(component, Badge):
            component.computed_width = (
                resolved_w or int(len(component.label) * (12 * 0.55)) + 40
            )
            component.computed_height = resolved_h or 24

        elif isinstance(component, Card):
            pad_x = 24
            pad_y_top = 64 if component.title else 24
            pad_y_bottom = 24

            child_pw = resolved_w - (pad_x * 2) if resolved_w else None
            child_ph = resolved_h - pad_y_top - pad_y_bottom if resolved_h else None

            LayoutEngine.calculate(
                component.child, start_x + pad_x, start_y + pad_y_top, child_pw, child_ph
            )
            component.computed_width = resolved_w or (
                component.child.computed_width + (pad_x * 2)
            )
            component.computed_height = resolved_h or (
                component.child.computed_height + pad_y_top + pad_y_bottom
            )

        elif isinstance(component, Icon):
            component.computed_width = resolved_w or 16
            component.computed_height = resolved_h or 16

        elif isinstance(component, Metric):
            component.computed_width = resolved_w or 140
            component.computed_height = resolved_h or 80

        elif isinstance(component, CircularMetric):
            component.computed_width = resolved_w or 120
            component.computed_height = resolved_h or 120

        elif isinstance(component, MetricGroup):
            current_x = start_x
            current_y = start_y
            max_w = 0
            max_h_in_row = 0
            
            col_w = None
            if resolved_w:
                col_w = (resolved_w - (component.spacing * (component.columns - 1))) // component.columns

            for i, child in enumerate(component.metrics):
                if i > 0 and i % component.columns == 0:
                    current_x = start_x
                    current_y += max_h_in_row + component.spacing
                    max_h_in_row = 0

                LayoutEngine.calculate(child, 0, 0, col_w, None)
                cw = child.computed_width
                ch = child.computed_height

                child.computed_x = current_x
                child.computed_y = current_y
                LayoutEngine.calculate(child, current_x, current_y, col_w, None)

                current_x += cw + component.spacing
                max_w = max(max_w, current_x - start_x - component.spacing)
                max_h_in_row = max(max_h_in_row, ch)

            component.computed_width = resolved_w or max_w
            component.computed_height = resolved_h or (
                current_y - start_y + max_h_in_row
            )

        # Enforce hard width/height if explicitly provided via style properties
        if component.style.width is not None and component.style.width != "fill":
            component.computed_width = component.style.width
        if component.style.height is not None and component.style.height != "fill":
            component.computed_height = component.style.height
