from __future__ import annotations

__layer__ = "Layer 1 — Core"

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
    OpticalSpacingTokens,
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

        try:
            from yaml import CSafeLoader as YAMLLoader
        except ImportError:
            from yaml import SafeLoader as YAMLLoader

        with open(path, "r", encoding="utf-8") as f:
            try:
                data = yaml.load(f, Loader=YAMLLoader) or {}
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
    def _deep_merge(base: dict, override: dict) -> dict:
        merged = base.copy()
        for key, value in override.items():
            if (
                isinstance(value, dict)
                and key in merged
                and isinstance(merged[key], dict)
            ):
                merged[key] = ConfigLoader._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    @staticmethod
    def _load_raw_theme(
        theme_name: str, themes_dir: str = "themes", visited: set[str] = None
    ) -> tuple[dict, str | None]:
        if visited is None:
            visited = set()

        if theme_name in visited:
            raise ThemeError(
                f"Inheritance cycle detected: {' -> '.join(visited)} -> {theme_name}"
            )

        visited.add(theme_name)

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

        try:
            from yaml import CSafeLoader as YAMLLoader
        except ImportError:
            from yaml import SafeLoader as YAMLLoader

        with open(theme_file, "r", encoding="utf-8") as f:
            try:
                data = yaml.load(f, Loader=YAMLLoader) or {}
            except yaml.YAMLError as e:
                raise ThemeError(f"Invalid YAML syntax in theme {theme_name}: {e}")

        extends = data.get("extends")
        if extends:
            base_data, _ = ConfigLoader._load_raw_theme(
                extends, themes_dir, visited.copy()
            )
            data = ConfigLoader._deep_merge(base_data, data)

        return data, extends

    @staticmethod
    def load_theme(
        theme_name: str, themes_dir: str = "themes", visited: set[str] = None
    ) -> Theme:
        data, extends = ConfigLoader._load_raw_theme(theme_name, themes_dir, visited)

        color_data = ConfigLoader._resolve_semantic_colors(data.get("colors", {}))
        colors = ColorTokens(**color_data)
        typography = TypographyTokens(**data.get("typography", {}))

        spacing_data = data.get("spacing", {})
        optical_data = (
            spacing_data.pop("optical", {}) if isinstance(spacing_data, dict) else {}
        )

        spacing = SpacingTokens(
            **(spacing_data if isinstance(spacing_data, dict) else {})
        )
        spacing.optical = OpticalSpacingTokens(**optical_data)

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
            schema=data.get("schema", 1),
            id=data.get("id"),
            tags=data.get("tags", []),
            extends=extends,
            author=data.get("author"),
            version=data.get("version"),
            license=data.get("license"),
            description=data.get("description"),
            homepage=data.get("homepage"),
            animations=data.get("animations"),
            icons=data.get("icons"),
            fonts=data.get("fonts"),
            assets=data.get("assets"),
            variables=data.get("variables"),
        )

    @staticmethod
    def _resolve_semantic_colors(colors: dict) -> dict:
        """Fill semantic visual tokens and guarantee readable hero foregrounds.

        Older themes only expose primitive colours.  Resolving semantic tokens at
        the theme boundary keeps the renderer free of mode-specific colour hacks
        while preserving backwards compatibility with existing theme YAML.
        """
        resolved = dict(colors)
        surface = resolved.get("surface", resolved.get("background", "#111827"))
        hero_surface = resolved.get("hero_surface") or surface
        hero_on_surface = resolved.get("hero_on_surface") or resolved.get("text")
        if not ConfigLoader._has_contrast(hero_on_surface, hero_surface, 4.5):
            hero_on_surface = (
                "#FFFFFF"
                if ConfigLoader._relative_luminance(hero_surface) < 0.45
                else "#111827"
            )

        resolved.update(
            {
                "hero_surface": hero_surface,
                "hero_on_surface": hero_on_surface,
                "badge_primary": resolved.get("badge_primary")
                or resolved.get("primary"),
                "badge_secondary": resolved.get("badge_secondary")
                or resolved.get("accent"),
                "badge_success": resolved.get("badge_success")
                or resolved.get("success"),
                "badge_info": resolved.get("badge_info") or resolved.get("info"),
                "badge_warning": resolved.get("badge_warning")
                or resolved.get("warning"),
                "badge_neutral": resolved.get("badge_neutral") or resolved.get("muted"),
                "progress_start": resolved.get("progress_start")
                or resolved.get("primary"),
                "progress_end": resolved.get("progress_end") or resolved.get("accent"),
            }
        )
        return resolved

    @staticmethod
    def _relative_luminance(color: str | None) -> float:
        if not color or not color.startswith("#") or len(color) not in (4, 7):
            return 0.0
        raw = color[1:]
        if len(raw) == 3:
            raw = "".join(channel * 2 for channel in raw)
        channels = [int(raw[index : index + 2], 16) / 255 for index in range(0, 6, 2)]
        linear = [
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
            for channel in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    @staticmethod
    def _has_contrast(
        foreground: str | None, background: str | None, minimum: float
    ) -> bool:
        fg_lum = ConfigLoader._relative_luminance(foreground)
        bg_lum = ConfigLoader._relative_luminance(background)
        return (max(fg_lum, bg_lum) + 0.05) / (min(fg_lum, bg_lum) + 0.05) >= minimum
