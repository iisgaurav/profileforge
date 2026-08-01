from profileforge.components.layout import Column, Component, Padding, Row, Spacer
from profileforge.components.style import Style
from profileforge.components.widgets import Text
from profileforge.core.context import BuildContext
from profileforge.dashboard.models import Dashboard
from profileforge.layouts.base import DashboardLayout


class BentoLayout(DashboardLayout):
    """
    A basic grid-packing layout strategy that organizes widgets into rows based on
    their GridConfig (width).
    """

    def compose(self, dashboard: Dashboard, context: BuildContext) -> Component:
        gap = context.theme.spacing.xl

        rows = []

        # Build header
        if dashboard.header.enabled:
            header_items = []
            if dashboard.title:
                header_items.append(
                    Text(
                        value=dashboard.title,
                        style=Style(font_size=24, color=context.theme.colors.primary),
                    )
                )
            if dashboard.subtitle:
                header_items.append(
                    Text(
                        value=dashboard.subtitle,
                        style=Style(font_size=16, color=context.theme.colors.muted),
                    )
                )

            if header_items:
                rows.append(
                    Column(children=header_items, spacing=context.theme.spacing.sm)
                )
                rows.append(Spacer(style=Style(height=gap // 2)))

        # Pack items based on width
        current_row = []
        current_row_width = 0

        for item in dashboard.items:
            widget_component = item.widget.render_safe(context)

            # If widget asks for full width (width >= 2)
            if item.grid.width >= 2:
                # Flush existing row if any
                if current_row:
                    rows.append(Row(children=current_row, spacing=gap))
                    current_row = []
                    current_row_width = 0

                # Add full width item as its own row
                rows.append(widget_component)
            else:
                # Pack into current row
                current_row.append(widget_component)
                current_row_width += 1

                # If row is full (assuming 2 columns max for bento)
                if current_row_width >= 2:
                    rows.append(Row(children=current_row, spacing=gap))
                    current_row = []
                    current_row_width = 0

        # Flush remaining
        if current_row:
            rows.append(Row(children=current_row, spacing=gap))

        # Build footer
        if dashboard.footer.enabled and dashboard.footer.text:
            rows.append(Spacer(style=Style(height=gap // 2)))
            rows.append(
                Row(
                    children=[
                        Text(
                            value=dashboard.footer.text,
                            style=Style(font_size=12, color=context.theme.colors.muted),
                        )
                    ],
                    style=Style(justify="center"),
                )
            )

        return Padding(
            value=context.theme.spacing.xl,
            child=Column(children=rows, spacing=gap),
        )
