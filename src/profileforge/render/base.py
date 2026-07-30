from abc import ABC, abstractmethod

from profileforge.components.layout import Component
from profileforge.core.context import BuildContext


class Renderer(ABC):
    def __init__(self, context: BuildContext):
        self.context = context
        self.theme = context.theme

    @abstractmethod
    def render(self, component: Component) -> str:
        pass
