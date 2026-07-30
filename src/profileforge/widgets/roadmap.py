from profileforge.widgets.base import Widget
from profileforge.core.context import BuildContext
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_widget
from profileforge.components.layout import Column, Row, Spacer, Padding, Component
from profileforge.components.widgets import Card, Text, ProgressBar
from profileforge.components.style import Style

@register_widget('roadmap')
class RoadmapWidget(Widget):
    def build(self, context: BuildContext) -> Component:
        # Request data from Local DataSource
        datasource = context.services.datasources.get("local")
        request = DataRequest(resource="roadmap.yaml")
        data = datasource.fetch(request) if datasource else []
        
        # Build declarative layout tree
        rows = []
        for item in data:
            skill = item.get('skill', 'Unknown')
            progress = item.get('progress', 0)
            
            label_row = Row(
                children=[
                    Text(skill, style=Style(font_weight="600", color="text")),
                    Spacer(width=300 - (len(skill)*8)), # Simplistic alignment spacer
                    Text(f"{progress}%", style=Style(font_size=12, color="text_muted")),
                ],
                spacing=5
            )
            
            bar = ProgressBar(progress, style=Style(width=350, height=8))
            
            item_col = Column(children=[label_row, bar], spacing=10)
            rows.append(item_col)
            
        content = Column(children=rows, spacing=25)
        return Card(title="Learning Roadmap", child=Padding(child=content, value=25), style=Style(width=400))
