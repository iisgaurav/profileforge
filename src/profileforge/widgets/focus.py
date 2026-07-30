from profileforge.widgets.base import Widget
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.components.layout import Column, Padding, Spacer
from profileforge.components.widgets import Card, Text, ProgressBar
from profileforge.components.style import Style

@register_widget('focus')
class FocusWidget(Widget):
    def build(self, context: BuildContext) -> Component:
        datasource = context.services.datasources.get("local")
        request = DataRequest(resource="focus.yaml")
        data = datasource.fetch(request) if datasource else {}
        
        sections = []
        for category, items in data.items():
            cat_label = Text(category.upper(), style=Style(font_size=12, font_weight="700", color="primary"))
            
            item_rows = []
            for item in items:
                name = item.get('name', 'Unknown')
                progress = item.get('progress', 0)
                item_rows.append(
                    Column(
                        children=[
                            Text(name, style=Style(font_weight="500")),
                            ProgressBar(progress, style=Style(width=350, height=6))
                        ],
                        spacing=10
                    )
                )
                
            category_col = Column(children=[cat_label, *item_rows], spacing=20)
            sections.append(category_col)
            
        content = Column(children=sections, spacing=30)
        return Card(title="Currently Doing", child=Padding(child=content, value=25), style=Style(width=400))
