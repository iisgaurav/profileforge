from pathlib import Path

import yaml

from profileforge.core.exceptions import ConfigurationError, ThemeError
from profileforge.core.models import (
    ColorTokens,
    DashboardConfig,
    DashboardFooterConfig,
    DashboardHeaderConfig,
    EffectsTokens,
    GridConfig,
    MetricsConfig,
    MotionTokens,
    OutputConfig,
    Outputs,
    ProfileForgeConfig,
    RadiusTokens,
    ShadowTokens,
    SpacingTokens,
    Theme,
    TypographyTokens,
    WidgetConfig,
)


class ConfigLoader:
    @staticmethod
    def load_main_config(filepath: str) -> ProfileForgeConfig:
        path = Path(filepath)
        if not path.exists():
            raise ConfigurationError(f"Config file not found: {filepath}")

        with open(path, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise ConfigurationError(f"Invalid YAML syntax in {filepath}: {e}")

        version = data.get("version", 1)
        project = data.get("project", {})
        themes = data.get("themes", {})
        outputs_data = data.get("outputs", {})

        svg_out = outputs_data.get("svg", {})
        md_out = outputs_data.get("markdown", {})
        png_out = outputs_data.get("png", {})

        outputs = Outputs(
            svg=OutputConfig(
                enabled=svg_out.get("enabled", True),
                dir=svg_out.get("dir", "assets/widgets"),
            ),
            markdown=OutputConfig(
                enabled=md_out.get("enabled", False), dir=md_out.get("dir", "assets")
            ),
            png=OutputConfig(
                enabled=png_out.get("enabled", False),
                dir=png_out.get("dir", "assets/widgets"),
            ),
        )

        widgets = []
        for w in data.get("widgets", []):
            if isinstance(w, str):
                widgets.append(WidgetConfig(name=w))
            elif isinstance(w, dict) and "name" in w:
                name = w.pop("name")

                # Parse grid metadata if present
                grid_data = w.pop("grid", {})
                grid = GridConfig(
                    width=grid_data.get("width", 1), height=grid_data.get("height", 1)
                )

                widgets.append(WidgetConfig(name=name, options=w, grid=grid))
            else:
                raise ConfigurationError(f"Invalid widget definition: {w}")

        # Parse dashboard
        dashboard_data = data.get("dashboard", {})
        header_data = dashboard_data.get("header", {})
        footer_data = dashboard_data.get("footer", {})

        dashboard = DashboardConfig(
            enabled=dashboard_data.get("enabled", False),
            layout=dashboard_data.get("layout", "bento"),
            title=dashboard_data.get("title", ""),
            subtitle=dashboard_data.get("subtitle"),
            header=DashboardHeaderConfig(
                enabled=header_data.get("enabled", True)
                if isinstance(header_data, dict)
                else (header_data is not False)
            ),
            footer=DashboardFooterConfig(
                enabled=footer_data.get("enabled", False)
                if isinstance(footer_data, dict)
                else (footer_data is not False),
                text=footer_data.get("text", "Powered by ProfileForge")
                if isinstance(footer_data, dict)
                else "Powered by ProfileForge",
            ),
        )

        metrics_data = data.get("metrics", {})
        metrics = MetricsConfig(
            enabled=metrics_data.get("enabled", True),
            strategy=metrics_data.get("strategy", "weighted_sum"),
        )

        return ProfileForgeConfig(
            version=version,
            project_name=project.get("name", "Profile"),
            project_title=project.get("title", "Developer"),
            active_theme=themes.get("active", "github-dark"),
            widgets=widgets,
            connectors_config=data.get("connectors", {}),
            outputs=outputs,
            dashboard=dashboard,
            metrics=metrics,
        )

    @staticmethod
    def load_theme(theme_name: str, themes_dir: str = "themes") -> Theme:
        theme_file = Path(themes_dir) / f"{theme_name}.yaml"
        if not theme_file.exists():
            # Fallback to built-in themes in the profileforge package
            builtin_theme = (
                Path(__file__).parent.parent / "themes" / f"{theme_name}.yaml"
            )
            if builtin_theme.exists():
                theme_file = builtin_theme
            else:
                raise ThemeError(
                    f"Theme file not found: {theme_name}.yaml in {themes_dir} or built-in themes."
                )

        with open(theme_file, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise ThemeError(f"Invalid YAML syntax in theme {theme_name}: {e}")

        # Future implementation would handle `extends` logic here

        colors = ColorTokens(**data.get("colors", {}))
        typography = TypographyTokens(**data.get("typography", {}))
        spacing = SpacingTokens(**data.get("spacing", {}))
        radius = RadiusTokens(**data.get("radius", {}))
        shadows = ShadowTokens(**data.get("shadows", {}))
        motion = MotionTokens(**data.get("motion", {}))
        effects = EffectsTokens(**data.get("effects", {}))

        return Theme(
            name=data.get("name", theme_name),
            mode=data.get("mode", "modern"),
            colors=colors,
            typography=typography,
            spacing=spacing,
            radius=radius,
            shadows=shadows,
            motion=motion,
            effects=effects,
            extends=data.get("extends"),
        )
