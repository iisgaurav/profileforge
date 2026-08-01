from profileforge.components.layout import Component
from profileforge.core.context import BuildContext as Context
from profileforge.core.models import Theme
from profileforge.core.registry import register_widget
from profileforge.widgets.base import Widget, WidgetCategory, WidgetMetadata

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "Component",
    "Context",
    "Theme",
    "Widget",
    "WidgetCategory",
    "WidgetMetadata",
    "register_widget",
]
