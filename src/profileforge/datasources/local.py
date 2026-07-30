import yaml
from pathlib import Path
from profileforge.datasources.base import DataSource
from profileforge.core.models import DataRequest
from profileforge.core.registry import register_datasource
from profileforge.core.exceptions import DataSourceError

@register_datasource('local')
class LocalDataSource(DataSource):
    def fetch(self, request: DataRequest) -> Any:
        root_dir = self.config.get('root', './')
        filename = request.resource
        filepath = Path(root_dir) / filename
        
        if not filepath.exists():
            raise DataSourceError(f"Local file not found: {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            if filepath.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                return f.read()
