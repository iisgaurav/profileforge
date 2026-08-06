from __future__ import annotations

import uuid
from typing import Optional

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
from profileforge.render.base import RenderNode
from profileforge.core.models import HorizontalAlign, VerticalAlign


class LayoutEngine:
    """Deterministic Layout Engine calculating constraints and producing an immutable RenderNode AST."""

    @staticmethod
    def calculate(
        component: Component,
        x: int = 0,
        y: int = 0,
        parent_w: Optional[int] = None,
        parent_h: Optional[int] = None,
    ) -> RenderNode:
        
        # 1. Resolve constraints
        w = parent_w if component.constraints.fill and parent_w else (component.constraints.preferred_width or parent_w or 0)
        
        # Backward compatibility for old style.width
        if component.style.width == "fill" and parent_w:
            w = parent_w
        elif isinstance(component.style.width, (int, float)):
            w = component.style.width
            
        h = parent_h if component.constraints.fill and parent_h else parent_h or 0
        if component.style.height == "fill" and parent_h:
            h = parent_h
        elif isinstance(component.style.height, (int, float)):
            h = component.style.height
            
        c_id = f"{component.__class__.__name__.lower()}_{uuid.uuid4().hex[:6]}"
        children_nodes = []

        # 2. Component-specific layout logic
        if isinstance(component, Spacer):
            pass # w, h already resolved

        elif isinstance(component, Padding):
            pad = component.value
            child_w = w - (pad * 2) if w else None
            child_h = h - (pad * 2) if h else None
            child_node = LayoutEngine.calculate(component.child, x + pad, y + pad, child_w, child_h)
            children_nodes.append(child_node)
            w = w or (child_node.width + pad * 2)
            h = h or (child_node.height + pad * 2)

        elif isinstance(component, Column):
            current_y = y
            max_w = 0
            for child in component.children:
                child_node = LayoutEngine.calculate(child, x, current_y, w, None)
                children_nodes.append(child_node)
                current_y += child_node.height + component.gap
                max_w = max(max_w, child_node.width)

            w = w or max_w
            h = h or (current_y - y - (component.gap if component.children else 0))

            # Alignment pass
            align = component.style.align
            if align in (HorizontalAlign.CENTER, HorizontalAlign.RIGHT, "center", "end"):
                new_children = []
                for child_node in children_nodes:
                    target_x = x
                    if align in (HorizontalAlign.CENTER, "center"):
                        target_x = x + (w - child_node.width) // 2
                    elif align in (HorizontalAlign.RIGHT, "end"):
                        target_x = x + w - child_node.width
                    
                    if target_x != child_node.x:
                        new_children.append(LayoutEngine._shift_node(child_node, target_x - child_node.x, 0))
                    else:
                        new_children.append(child_node)
                children_nodes = new_children

        elif isinstance(component, Row):
            current_x = x
            max_h = 0
            for child in component.children:
                child_node = LayoutEngine.calculate(child, current_x, y, None, h)
                children_nodes.append(child_node)
                current_x += child_node.width + component.gap
                max_h = max(max_h, child_node.height)

            w = w or (current_x - x - (component.gap if component.children else 0))
            h = h or max_h

            align = component.style.align
            if align in (VerticalAlign.MIDDLE, VerticalAlign.BOTTOM, "center", "end"):
                new_children = []
                for child_node in children_nodes:
                    target_y = y
                    if align in (VerticalAlign.MIDDLE, "center"):
                        target_y = y + (h - child_node.height) // 2
                    elif align in (VerticalAlign.BOTTOM, "end"):
                        target_y = y + h - child_node.height
                    
                    if target_y != child_node.y:
                        new_children.append(LayoutEngine._shift_node(child_node, 0, target_y - child_node.y))
                    else:
                        new_children.append(child_node)
                children_nodes = new_children

        elif isinstance(component, Inline):
            # Inline allocates available width, does not layout children internally with strict geometry.
            # Intrinsic sizing deferred to Renderer/Browser.
            w = w or parent_w or 400
            h = h or 24
            for child in component.children:
                # We just pass 0 width/height nodes to renderer, renderer will handle flow natively
                children_nodes.append(LayoutEngine.calculate(child, x, y, 0, 0))
                
        elif isinstance(component, Stack):
            w = w or 0
            h = h or 0
            for child in component.children:
                child_node = LayoutEngine.calculate(child, x, y, w, h)
                children_nodes.append(child_node)
                w = max(w, child_node.width)
                h = max(h, child_node.height)
                
        elif isinstance(component, Grid):
            # Placeholder for future Grid
            pass

        elif isinstance(component, Wrap):
            current_x = x
            current_y = y
            max_h_in_run = 0
            max_w = 0

            for child in component.children:
                child_node = LayoutEngine.calculate(child, current_x, current_y, None, None)
                
                if w and (current_x + child_node.width - x > w) and current_x > x:
                    current_x = x
                    current_y += max_h_in_run + component.run_spacing
                    max_h_in_run = 0
                    child_node = LayoutEngine.calculate(child, current_x, current_y, None, None)

                children_nodes.append(child_node)
                current_x += child_node.width + component.spacing
                max_w = max(max_w, current_x - x - component.spacing)
                max_h_in_run = max(max_h_in_run, child_node.height)

            w = w or max_w
            h = h or (current_y - y + max_h_in_run)

        elif isinstance(component, Card):
            pad_x = 24
            pad_y_top = 64 if component.title else 24
            pad_y_bottom = 24

            child_pw = w - (pad_x * 2) if w else None
            child_ph = h - pad_y_top - pad_y_bottom if h else None

            child_node = LayoutEngine.calculate(component.child, x + pad_x, y + pad_y_top, child_pw, child_ph)
            children_nodes.append(child_node)
            w = w or (child_node.width + (pad_x * 2))
            h = h or (child_node.height + pad_y_top + pad_y_bottom)

        elif isinstance(component, MetricGroup):
            current_x = x
            current_y = y
            max_w = 0
            max_h_in_row = 0
            
            col_w = None
            if w:
                col_w = (w - (component.spacing * (component.columns - 1))) // component.columns

            for i, child in enumerate(component.metrics):
                if i > 0 and i % component.columns == 0:
                    current_x = x
                    current_y += max_h_in_row + component.spacing
                    max_h_in_row = 0

                child_node = LayoutEngine.calculate(child, current_x, current_y, col_w, None)
                children_nodes.append(child_node)

                current_x += child_node.width + component.spacing
                max_w = max(max_w, current_x - x - component.spacing)
                max_h_in_row = max(max_h_in_row, child_node.height)

            w = w or max_w
            h = h or (current_y - y + max_h_in_row)
            
        elif isinstance(component, ProgressMetric):
            w = w or 300
            h = h or 40

        elif isinstance(component, Text):
            # No width estimation anymore. Default to constraints or 0.
            # Intrinsic text bounds cannot be calculated without font metrics.
            w = w or 0
            h = h or 20 # Fallback

        elif isinstance(component, ProgressBar):
            w = w or 300
            h = h or 8

        elif isinstance(component, Divider):
            w = w or 400
            h = h or 1

        elif isinstance(component, Badge):
            # Arbitrary fixed default to satisfy older widgets before migration
            w = w or 100
            h = h or 24

        elif isinstance(component, Icon):
            w = w or 16
            h = h or 16

        elif isinstance(component, Metric):
            w = w or 140
            h = h or 80

        elif isinstance(component, CircularMetric):
            w = w or 120
            h = h or 120

        # Construct AST node
        return RenderNode(
            component=component,
            x=x,
            y=y,
            width=w,
            height=h,
            children=children_nodes,
            debug={"id": c_id, "type": component.__class__.__name__}
        )

    @staticmethod
    def _shift_node(node: RenderNode, dx: int, dy: int) -> RenderNode:
        if dx == 0 and dy == 0:
            return node
        new_children = [LayoutEngine._shift_node(c, dx, dy) for c in node.children]
        return RenderNode(
            component=node.component,
            x=node.x + dx,
            y=node.y + dy,
            width=node.width,
            height=node.height,
            children=new_children,
            debug=node.debug
        )
