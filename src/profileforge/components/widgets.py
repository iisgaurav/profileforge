from typing import List, Optional
from profileforge.components.layout import Component
from profileforge.components.style import Style

class Card(Component):
    def __init__(self, title: str, child: Component, style: Optional[Style] = None):
        super().__init__(style)
        self.title = title
        self.child = child

class Text(Component):
    def __init__(self, value: str, style: Optional[Style] = None):
        super().__init__(style)
        self.value = value

class ProgressBar(Component):
    def __init__(self, progress: int, style: Optional[Style] = None):
        super().__init__(style)
        self.progress = progress

class Icon(Component):
    def __init__(self, svg_path: str, style: Optional[Style] = None):
        super().__init__(style)
        self.svg_path = svg_path
