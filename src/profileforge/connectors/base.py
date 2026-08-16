__layer__ = "Layer 6 — Connectors"
from abc import ABC, abstractmethod
from typing import Any

from profileforge.core.models import DataRequest


class Connector(ABC):
    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def fetch(self, request: DataRequest) -> Any:
        pass
