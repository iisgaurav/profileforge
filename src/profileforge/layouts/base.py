from abc import ABC, abstractmethod

from profileforge.components.layout import Component
from profileforge.core.context import BuildContext
from profileforge.dashboard.models import Dashboard


class DashboardLayout(ABC):
    """Abstract base class for all Dashboard Layout algorithms."""

    @abstractmethod
    def compose(self, dashboard: Dashboard, context: BuildContext) -> Component:
        """
        Takes a Dashboard model (with items) and returns a resolved Component tree.
        """
