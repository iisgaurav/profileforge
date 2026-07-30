import yaml
from pathlib import Path
from profileforge.core.models import ProfileForgeConfig, Theme, Outputs, OutputConfig, WidgetConfig
from profileforge.core.exceptions import ConfigurationError, ThemeError

class ConfigLoader:
    @staticmethod
    def load_main_config(filepath: str) -> ProfileForgeConfig:
        path = Path(filepath)
        if not path.exists():
            raise ConfigurationError(f"Config file not found: {filepath}")
            
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise ConfigurationError(f"Invalid YAML syntax in {filepath}: {e}")
                
        version = data.get('version', 1)
        project = data.get('project', {})
        themes = data.get('themes', {})
        outputs_data = data.get('outputs', {})
        
        svg_out = outputs_data.get('svg', {})
        md_out = outputs_data.get('markdown', {})
        png_out = outputs_data.get('png', {})
        
        outputs = Outputs(
            svg=OutputConfig(enabled=svg_out.get('enabled', True), dir=svg_out.get('dir', 'assets/widgets')),
            markdown=OutputConfig(enabled=md_out.get('enabled', False), dir=md_out.get('dir', 'assets')),
            png=OutputConfig(enabled=png_out.get('enabled', False), dir=png_out.get('dir', 'assets/widgets'))
        )
        
        widgets = []
        for w in data.get('widgets', []):
            if isinstance(w, str):
                widgets.append(WidgetConfig(name=w))
            elif isinstance(w, dict) and 'name' in w:
                name = w.pop('name')
                widgets.append(WidgetConfig(name=name, options=w))
            else:
                raise ConfigurationError(f"Invalid widget definition: {w}")

        return ProfileForgeConfig(
            version=version,
            project_name=project.get('name', 'Profile'),
            project_title=project.get('title', 'Developer'),
            active_theme=themes.get('active', 'github-dark'),
            widgets=widgets,
            datasources_config=data.get('datasources', {}),
            outputs=outputs
        )

    @staticmethod
    def load_theme(theme_name: str, themes_dir: str = 'themes') -> Theme:
        theme_file = Path(themes_dir) / f"{theme_name}.yaml"
        if not theme_file.exists():
            raise ThemeError(f"Theme file not found: {theme_file}")
            
        with open(theme_file, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise ThemeError(f"Invalid YAML syntax in theme {theme_name}: {e}")
        
        # Future implementation would handle `extends` logic here
        
        return Theme(
            name=data.get('name', theme_name),
            background=data.get('background', '#0D1117'),
            primary=data.get('primary', '#58A6FF'),
            secondary=data.get('secondary', '#8B5CF6'),
            text=data.get('text', '#C9D1D9'),
            text_muted=data.get('text_muted', '#8B949E'),
            border=data.get('border', '#30363D'),
            progress_bg=data.get('progress_bg', '#21262D'),
            extends=data.get('extends')
        )
