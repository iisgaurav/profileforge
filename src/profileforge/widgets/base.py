from abc import ABC, abstractmethod

from profileforge.components.layout import Component
from profileforge.core.context import BuildContext


class Widget(ABC):
    @abstractmethod
    def build(self, context: BuildContext) -> Component:
        pass
