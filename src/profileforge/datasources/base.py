from abc import ABC, abstractmethod
from typing import Any, Dict
from profileforge.core.models import DataRequest

class DataSource(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    @abstractmethod
    def fetch(self, request: DataRequest) -> Any:
        pass
