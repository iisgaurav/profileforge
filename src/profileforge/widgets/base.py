from abc import ABC, abstractmethod
from profileforge.core.context import BuildContext
from profileforge.components.layout import Component

class Widget(ABC):
    @abstractmethod
    def build(self, context: BuildContext) -> Component:
        pass
