from pathlib import Path
from typing import Any

import yaml

from profileforge.connectors.base import Connector
from profileforge.core.exceptions import ConnectorError
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_connector


@register_connector("local")
class LocalConnector(Connector):
    def fetch(self, request: DataRequest) -> Any:
        root_dir = self.config.get("root", "./")
        filename = request.resource
        filepath = Path(root_dir) / filename

        if not filepath.exists():
            raise ConnectorError(f"Local file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            if filepath.suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f)
            else:
                return f.read()
