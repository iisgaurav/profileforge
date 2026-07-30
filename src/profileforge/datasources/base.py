from abc import ABC, abstractmethod
from typing import Any

from profileforge.core.models import DataRequest


class DataSource(ABC):
    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def fetch(self, request: DataRequest) -> Any:
        pass
