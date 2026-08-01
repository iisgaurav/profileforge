import argparse
import os
import sys
import time
from pathlib import Path

import profileforge.connectors.github.connector

# Ensure registries populate via side-effects
import profileforge.connectors.local
import profileforge.widgets.about
import profileforge.widgets.achievements
import profileforge.widgets.activity_timeline
import profileforge.widgets.experience
import profileforge.widgets.expertise
import profileforge.widgets.focus
import profileforge.widgets.github_languages
import profileforge.widgets.github_stats
import profileforge.widgets.hero
import profileforge.widgets.now
import profileforge.widgets.repositories
import profileforge.widgets.roadmap
import profileforge.widgets.skills
import profileforge.widgets.social
import profileforge.widgets.streak  # noqa: F401
from profileforge.core.config import ConfigLoader
from profileforge.core.context import BuildContext, Services
from profileforge.core.exceptions import ProfileForgeError
from profileforge.core.registry import WIDGET_REGISTRY, ConnectorRegistry
from profileforge.render.layout import LayoutEngine
from profileforge.render.svg.renderer import SVGRenderer
from profileforge.services.gallery import export_gallery
from profileforge.templates import (
    get_template_info,
    list_builtin_templates,
    scaffold_template,
)

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BANNER = """+----------------------------------------------------------+
|  ProfileForge -- GitHub Profile & SVG Widget Engine      |
+----------------------------------------------------------+"""


def print_banner():
    print(f"\n{BANNER}\n")


def print_success(msg: str):
    print(f"  [OK]   {msg}")


def print_info(msg: str):
    print(f"  [INFO] {msg}")


def print_warn(msg: str):
    print(f"  [WARN] {msg}")


def print_error(msg: str, hint: str = ""):
    print(f"\n  [FAIL] {msg}")
    if hint:
        print(f"         Hint: {hint}\n")
    else:
        print()


def cmd_build(args):
    start_time = time.perf_counter()
    config_path = Path(args.config)

    if not config_path.exists():
        print_error(
            f"Configuration file '{config_path}' not found.",
            hint="Run 'profileforge init' to scaffold a new project or pass '--config <path>'.",
        )
        sys.exit(1)

    try:
        config = ConfigLoader.load_main_config(str(config_path))
        print_success(f"Loaded configuration from '{config_path}'")

        theme_dir = config_path.parent / "themes"
        theme = ConfigLoader.load_theme(config.active_theme, themes_dir=str(theme_dir))
        print_success(f"Loaded theme '{theme.name}' (mode: {theme.mode})")

        connectors = {}
        for name, ds_config in config.connectors_config.items():
            if name in ConnectorRegistry:
                # adjust relative path
                if "root" in ds_config:
                    ds_config["root"] = str(config_path.parent / ds_config["root"])
                connectors[name] = ConnectorRegistry[name](ds_config)

        services = Services(connectors=connectors)
        context = BuildContext(theme=theme, config=config, services=services)
        svg_renderer = SVGRenderer(context)

        out_dir = (
            Path(args.output)
            if args.output
            else config_path.parent / config.outputs.svg.dir
        )
        out_dir.mkdir(parents=True, exist_ok=True)

        print_info(f"Building {len(config.widgets)} registered widget(s)...")

        # Generate standalone SVGs for all widgets
        built_count = 0
        if config.outputs.svg.enabled:
            import html as html_mod

            defs_block = svg_renderer.get_defs()

            for w_config in config.widgets:
                if w_config.name not in WIDGET_REGISTRY:
                    print_warn(
                        f"Widget '{w_config.name}' not found in registry. Skipping."
                    )
                    continue

                widget = WIDGET_REGISTRY[w_config.name]()
                component_tree = widget.render_safe(context)
                LayoutEngine.calculate(component_tree)

                inner_svg = svg_renderer.render(component_tree)
                total_w = component_tree.computed_width
                total_h = component_tree.computed_height
                escaped_title = html_mod.escape(w_config.name.title())

                svg_content = (
                    f'<svg width="{total_w}" height="{total_h}" '
                    f'viewBox="0 0 {total_w} {total_h}" '
                    f'xmlns="http://www.w3.org/2000/svg" '
                    f'role="img">\n'
                    f"  <title>{escaped_title} Widget</title>\n"
                    f"  <desc>ProfileForge {escaped_title} widget</desc>\n"
                    f"  {defs_block}\n"
                    f"  {inner_svg}\n"
                    f"</svg>"
                )

                header = f"<!--\nGenerated by ProfileForge (Widget Engine)\nVersion: {config.version}\nTheme: {theme.name}\nWidget: {w_config.name}\n-->\n"

                out_file = out_dir / f"{w_config.name}.svg"
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(header + svg_content)
                print_success(f"Generated {w_config.name}.svg -> {out_file}")
                built_count += 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        print(
            f"\n[DONE] Built {built_count} widget(s) in {elapsed_ms:.1f}ms -> {out_dir}\n"
        )

    except ProfileForgeError as e:
        print_error(
            str(e),
            hint="Run 'profileforge doctor' to diagnose configuration or registry issues.",
        )
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected build error: {e}")
        sys.exit(1)


def cmd_doctor(args):
    print_banner()
    print("Running ProfileForge system diagnostics...\n")
    print_info(f"Python runtime: {sys.version.split()[0]}")

    config_path = Path("profileforge.yaml")
    if config_path.exists():
        print_success("profileforge.yaml found")
        try:
            config = ConfigLoader.load_main_config(str(config_path))
            print_success("Configuration parsed successfully")

            theme_dir = config_path.parent / "themes"
            ConfigLoader.load_theme(config.active_theme, themes_dir=str(theme_dir))
            print_success(f"Active theme '{config.active_theme}' loaded successfully")

            if theme_dir.exists():
                valid_themes = 0
                for theme_file in theme_dir.glob("*.yaml"):
                    try:
                        theme = ConfigLoader.load_theme(
                            theme_file.stem, themes_dir=str(theme_dir)
                        )
                        valid_themes += 1
                        meta_ok = bool(theme.id and theme.schema and theme.tags)
                        tokens_ok = bool(
                            theme.colors and theme.typography and theme.spacing
                        )
                        inherits = theme.extends if theme.extends else "None"
                        print_success(
                            f"Theme '{theme.name}': Metadata {'OK' if meta_ok else 'MISSING'}, "
                            f"Tokens {'OK' if tokens_ok else 'MISSING'}, Inheritance: {inherits}"
                        )
                    except Exception as e:
                        print_error(f"Failed to load theme {theme_file.name}: {e}")
                print_success(f"Validated {valid_themes} theme(s) in {theme_dir}")
        except ProfileForgeError as e:
            print_error(f"Config/Theme validation error: {e}")
    else:
        print_warn("profileforge.yaml NOT found in current directory")

    print_success(
        f"Registered Widgets ({len(WIDGET_REGISTRY)}): {list(WIDGET_REGISTRY.keys())}"
    )
    print_success(
        f"Registered Connectors ({len(ConnectorRegistry)}): {list(ConnectorRegistry.keys())}"
    )

    builtin_themes_dir = Path(__file__).parent.parent / "themes"
    if builtin_themes_dir.exists():
        valid_builtin = 0
        for theme_file in builtin_themes_dir.glob("*.yaml"):
            try:
                theme = ConfigLoader.load_theme(
                    theme_file.stem, themes_dir=str(builtin_themes_dir)
                )
                valid_builtin += 1
                meta_ok = bool(theme.id and theme.schema and theme.tags)
                tokens_ok = bool(theme.colors and theme.typography and theme.spacing)
                inherits = theme.extends if theme.extends else "None"
                print_success(
                    f"Built-in Theme '{theme.name}': Metadata {'OK' if meta_ok else 'MISSING'}, "
                    f"Tokens {'OK' if tokens_ok else 'MISSING'}, Inheritance: {inherits}"
                )
            except Exception as e:
                print_error(f"Failed to load built-in theme {theme_file.name}: {e}")
        print_success(f"Validated {valid_builtin} built-in theme(s)")

    templates = list_builtin_templates()
    if templates:
        print_success(f"Built-in Templates ({len(templates)}): {', '.join(templates)}")

    print("\n[DONE] Diagnostics complete. Environment is healthy.\n")


def cmd_validate(args):
    config_path = Path(args.config)
    print(f"Validating ProfileForge configuration at '{config_path}'...\n")

    if not config_path.exists():
        print_error(
            f"Configuration file '{config_path}' not found.",
            hint="Ensure the path is correct or run 'profileforge init'.",
        )
        sys.exit(1)

    try:
        config = ConfigLoader.load_main_config(str(config_path))
        print_success(f"Config syntax valid: '{config.project_name}'")

        theme_dir = config_path.parent / "themes"
        ConfigLoader.load_theme(config.active_theme, themes_dir=str(theme_dir))
        print_success(f"Theme '{config.active_theme}' resolved and validated")

        for w in config.widgets:
            if w.name in WIDGET_REGISTRY:
                print_success(f"Widget '{w.name}' verified")
            else:
                print_error(
                    f"Unknown widget '{w.name}'",
                    hint=f"Available widgets: {', '.join(sorted(WIDGET_REGISTRY.keys()))}",
                )
                sys.exit(1)

        out_dir = (
            Path(args.output)
            if args.output
            else config_path.parent / config.outputs.svg.dir
        )
        if not out_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)
        if os.access(out_dir, os.W_OK):
            print_success(f"Output directory '{out_dir}' is writable")
        else:
            print_error(f"Output directory '{out_dir}' is not writable.")
            sys.exit(1)

        print("\n[DONE] Configuration is 100% valid and ready to build.\n")
    except ProfileForgeError as e:
        print_error(str(e))
        sys.exit(1)


def cmd_new(args):
    template_name = getattr(args, "template", "backend") or "backend"
    available_templates = list_builtin_templates()

    if template_name not in available_templates:
        print_error(
            f"Unknown template '{template_name}'.",
            hint=f"Available templates: {', '.join(available_templates)}. Run 'profileforge templates list'.",
        )
        sys.exit(1)

    target = Path(args.name)
    if target.exists() and any(target.iterdir()):
        print_error(
            f"Directory '{args.name}' already exists and is not empty.",
            hint="Specify a new target directory name or use 'profileforge init' inside an empty directory.",
        )
        sys.exit(1)

    project_name = args.name.replace("-", " ").replace("_", " ").title() + " Profile"

    try:
        scaffold_template(
            template_name=template_name,
            target_dir=target,
            project_name=project_name,
        )
        print_success(
            f"Created new ProfileForge project in '{args.name}' (template: '{template_name}')"
        )
        print_success(
            f"Configuration and starter configs seeded in '{args.name}/config'"
        )
        print("\nNext steps:")
        print(f"  cd {args.name}")
        print("  profileforge build\n")
    except Exception as e:
        print_error(f"Failed to scaffold template: {e}")
        sys.exit(1)


def cmd_init(args):
    template_name = getattr(args, "template", "backend") or "backend"
    available_templates = list_builtin_templates()

    if template_name not in available_templates:
        print_error(
            f"Unknown template '{template_name}'.",
            hint=f"Available templates: {', '.join(available_templates)}. Run 'profileforge templates list'.",
        )
        sys.exit(1)

    target_dir = Path(args.directory).resolve()
    config_file = target_dir / "profileforge.yaml"
    if config_file.exists():
        print_error(
            f"A ProfileForge project already exists at '{target_dir}'.",
            hint="Run 'profileforge build' to compile or edit profileforge.yaml.",
        )
        sys.exit(1)

    project_name = getattr(args, "name", None)
    if not project_name:
        dir_name = target_dir.name
        project_name = (
            "Developer Profile"
            if dir_name in (".", "", "profileforge")
            else f"{dir_name.replace('-', ' ').replace('_', ' ').title()} Profile"
        )

    try:
        scaffold_template(
            template_name=template_name,
            target_dir=target_dir,
            project_name=project_name,
        )
        print_success(
            f"Initialized ProfileForge project in '{args.directory}' (template: '{template_name}')"
        )
        print("\nNext steps:")
        print("  profileforge build\n")
    except Exception as e:
        print_error(f"Failed to initialize project: {e}")
        sys.exit(1)


def cmd_templates_list(args):
    print_banner()
    print("Available ProfileForge Starter Templates:\n")
    template_ids = list_builtin_templates()
    for t_id in template_ids:
        info = get_template_info(t_id) or {}
        name = info.get("name", t_id.title())
        theme = info.get("default_theme", "github-dark")
        desc = info.get("description", "")
        widgets = ", ".join(info.get("widgets", []))
        print(f"  * {t_id:<15} {name} (Theme: {theme})")
        if widgets:
            print(f"    Widgets:      {widgets}")
        if desc:
            print(f"    Description:  {desc}")
        print()
    print("Scaffold a new project:")
    print("  profileforge new <dir-name> --template <template-id>")
    print("  profileforge init --template <template-id>\n")


def cmd_gallery_export(args):
    start_time = time.perf_counter()
    out_dir = getattr(args, "out_dir", "gallery") or "gallery"
    print_banner()
    print_info(f"Exporting ProfileForge ecosystem gallery to '{out_dir}'...")

    try:
        result = export_gallery(out_dir=out_dir)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        print_success(
            f"Extracted {result['themes_count']} theme(s) -> {out_dir}/themes.json"
        )
        print_success(
            f"Extracted {result['widgets_count']} widget(s) -> {out_dir}/widgets.json"
        )
        print_success(
            f"Extracted {result['templates_count']} template(s) -> {out_dir}/templates.json"
        )
        print_success(
            f"Rendered {result['rendered_assets_count']} SVG asset(s) -> {out_dir}/assets/"
        )
        print_success(f"Generated gallery index -> {out_dir}/gallery.json")

        print(
            f"\n[DONE] Gallery export completed in {elapsed_ms:.1f}ms ({result['rendered_assets_count']} assets built in '{out_dir}').\n"
        )
    except Exception as e:
        print_error(f"Gallery export failed: {e}")
        sys.exit(1)


def cmd_themes_build(args):
    config_path = Path(args.config)
    try:
        if not config_path.exists():
            print_error(f"Config file not found: {args.config}")
            sys.exit(1)

        config = ConfigLoader.load_main_config(str(config_path))
        print_success("Loaded configuration")

        theme_dir = config_path.parent / "themes"
        if not theme_dir.exists():
            theme_dir = Path(__file__).parent.parent / "themes"

        gallery_dir = config_path.parent / "gallery"
        gallery_dir.mkdir(parents=True, exist_ok=True)

        from profileforge.core.models import WidgetConfig

        widget_config = WidgetConfig(name="github_stats")
        config.widgets = [widget_config]

        connectors = {}
        for name, ds_config in config.connectors_config.items():
            if name in ConnectorRegistry:
                if "root" in ds_config:
                    ds_config["root"] = str(config_path.parent / ds_config["root"])
                connectors[name] = ConnectorRegistry[name](ds_config)
        services = Services(connectors=connectors)

        if "github_stats" not in WIDGET_REGISTRY:
            print_error("Widget 'github_stats' not found in registry.")
            sys.exit(1)

        theme_files = []
        if theme_dir.exists():
            theme_files.extend(list(theme_dir.glob("*.yaml")))

        builtin_themes_dir = Path(__file__).parent.parent / "themes"
        if builtin_themes_dir.exists():
            theme_files.extend(list(builtin_themes_dir.glob("*.yaml")))

        import html as html_mod

        seen_themes = set()
        for theme_file in theme_files:
            theme_name = theme_file.stem
            if theme_name in seen_themes:
                continue
            seen_themes.add(theme_name)
            try:
                theme = ConfigLoader.load_theme(theme_name, themes_dir=str(theme_dir))

                config.active_theme = theme_name
                context = BuildContext(theme=theme, config=config, services=services)
                svg_renderer = SVGRenderer(context)

                widget = WIDGET_REGISTRY["github_stats"]()
                component_tree = widget.render_safe(context)
                LayoutEngine.calculate(component_tree)

                inner_svg = svg_renderer.render(component_tree)
                defs_block = svg_renderer.get_defs()
                total_w = component_tree.computed_width
                total_h = component_tree.computed_height

                escaped_title = html_mod.escape(f"github_stats - {theme_name}")

                svg_content = (
                    f'<svg width="{total_w}" height="{total_h}" '
                    f'viewBox="0 0 {total_w} {total_h}" '
                    f'xmlns="http://www.w3.org/2000/svg" '
                    f'role="img">\n'
                    f"  <title>{escaped_title}</title>\n"
                    f"  <desc>ProfileForge widget preview</desc>\n"
                    f"  {defs_block}\n"
                    f"  {inner_svg}\n"
                    f"</svg>"
                )

                out_file = gallery_dir / f"{theme_name}.svg"
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(svg_content)
                print_success(f"Generated gallery/{theme_name}.svg")
            except Exception as e:
                print_error(f"Failed to build gallery for theme {theme_name}: {e}")

    except ProfileForgeError as e:
        print_error(str(e))
        sys.exit(1)


def cmd_benchmark(args):
    import json

    from profileforge.services.benchmark import run_benchmark

    config_path = None
    if getattr(args, "config", None):
        config_path = Path(args.config)
    elif Path("profileforge.yaml").exists():
        config_path = Path("profileforge.yaml")
    elif (Path("examples") / "backend" / "profileforge.yaml").exists():
        config_path = Path("examples") / "backend" / "profileforge.yaml"
    else:
        builtin_backend = (
            Path(__file__).parent.parent / "templates" / "backend" / "profileforge.yaml"
        )
        if builtin_backend.exists():
            config_path = builtin_backend

    if not config_path or not config_path.exists():
        print_error(
            f"Benchmark configuration file '{args.config or 'profileforge.yaml'}' not found.",
            hint="Provide a valid config file path using '--config <path>' or run from a project directory.",
        )
        sys.exit(1)

    iterations = getattr(args, "iterations", 10) or 10
    print_banner()
    print_info(
        f"Running high-precision benchmark on '{config_path}' ({iterations} iterations)..."
    )

    try:
        result = run_benchmark(config_path, iterations=iterations)
        print("\n" + result.format_table() + "\n")

        if getattr(args, "output", None):
            out_file = Path(args.output)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result.to_dict(), f, indent=2)
            print_success(f"Benchmark results saved -> {out_file}")

        budget_file = getattr(args, "budget_file", None)
        if budget_file:
            b_path = Path(budget_file)
            if not b_path.exists():
                print_error(f"Budget file '{budget_file}' not found.")
                sys.exit(1)

            import yaml

            with open(b_path, "r", encoding="utf-8") as f:
                b_data = yaml.safe_load(f) or {}
            budgets = b_data.get("budgets", {})

            passed, evals = result.evaluate_budget(budgets)
            print("\nPerformance Budget Verification:")
            print("-" * 65)
            print(
                f"{'Stage':<20} | {'Actual (ms)':<12} | {'Budget (ms)':<12} | {'Status':<10}"
            )
            print("-" * 65)
            for ev in evals:
                status_str = "[PASS]" if ev["passed"] else "[FAIL]"
                print(
                    f"{ev['stage']:<20} | {ev['actual_ms']:>10.3f}ms | {ev['limit_ms']:>10.3f}ms | {status_str}"
                )
            print("-" * 65)

            if not passed:
                print_error("Performance budget verification failed.")
                sys.exit(1)
            else:
                print_success("All stages within budget thresholds!")

    except Exception as e:
        print_error(f"Benchmark execution failed: {e}")
        sys.exit(1)


def cmd_widgets_list(args):
    print_banner()
    print("Registered ProfileForge Widgets:\n")
    header = f"{'Widget ID':<18} | {'Name':<22} | {'Category':<14} | {'Status':<15} | {'Connectors':<18}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for widget_id in sorted(WIDGET_REGISTRY.keys()):
        widget_cls = WIDGET_REGISTRY[widget_id]
        try:
            widget_inst = widget_cls()
            meta = widget_inst.metadata()
            status = (
                "[Experimental]" if getattr(meta, "experimental", False) else "[Stable]"
            )
            connectors = (
                ", ".join(meta.required_connectors)
                if meta.required_connectors
                else "none"
            )
            name = meta.name or widget_id.replace("_", " ").title()
            cat = getattr(meta, "category", "general")
            print(
                f"{meta.id:<18} | {name:<22} | {cat:<14} | {status:<15} | {connectors:<18}"
            )
        except Exception:
            print(
                f"{widget_id:<18} | {widget_id.title():<22} | {'unknown':<14} | {'[Stable]':<15} | {'none':<18}"
            )

    print("-" * len(header))
    print(
        f"Total: {len(WIDGET_REGISTRY)} registered widget(s). Use 'profileforge widgets info <id>' for details.\n"
    )


def cmd_widgets_info(args):
    widget_id = args.widget_id
    if widget_id not in WIDGET_REGISTRY:
        print_error(
            f"Widget '{widget_id}' not found in registry.",
            hint=f"Available widgets: {', '.join(sorted(WIDGET_REGISTRY.keys()))}",
        )
        sys.exit(1)

    print_banner()
    widget_cls = WIDGET_REGISTRY[widget_id]
    widget_inst = widget_cls()
    meta = widget_inst.metadata()

    status = "Experimental" if getattr(meta, "experimental", False) else "Stable"
    deprecated = "Yes" if getattr(meta, "deprecated", False) else "No"
    tags = ", ".join(meta.tags) if meta.tags else "none"
    connectors = (
        ", ".join(meta.required_connectors) if meta.required_connectors else "none"
    )

    print(f"Widget Information: {meta.name} ({meta.id})\n")
    print(f"  ID:                  {meta.id}")
    print(f"  Name:                {meta.name}")
    print(f"  Category:            {meta.category}")
    print(f"  Version:             {meta.version}")
    print(f"  Author:              {meta.author or 'ProfileForge Team'}")
    print(f"  License:             {meta.license}")
    print(f"  Status:              {status}")
    print(f"  Deprecated:          {deprecated}")
    print(f"  Schema:              {meta.schema}")
    print(f"  Required Connectors: {connectors}")
    print(f"  Tags:                {tags}")
    print(f"  Description:         {meta.description or 'No description provided.'}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ProfileForge: Open-Source GitHub Profile & SVG Widget Engine"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. build
    build_parser = subparsers.add_parser(
        "build", help="Build profile widgets from configuration"
    )
    build_parser.add_argument(
        "--config",
        default="profileforge.yaml",
        help="Path to config file (default: profileforge.yaml)",
    )
    build_parser.add_argument(
        "--output", default=None, help="Override output directory"
    )

    # 2. doctor
    subparsers.add_parser(
        "doctor", help="Run system diagnostics and verify environment health"
    )

    # 3. init
    init_parser = subparsers.add_parser(
        "init", help="Initialize a ProfileForge project in target directory"
    )
    init_parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Target directory (default: current directory)",
    )
    init_parser.add_argument(
        "--template",
        "-t",
        default="backend",
        help="Starter template to use (backend, frontend, minimal, student, opensource, ai-engineer)",
    )
    init_parser.add_argument(
        "--name", default=None, help="Custom project name override"
    )

    # 4. new
    new_parser = subparsers.add_parser(
        "new", help="Scaffold a new ProfileForge project in a new directory"
    )
    new_parser.add_argument("name", help="Name of the new project directory")
    new_parser.add_argument(
        "--template",
        "-t",
        default="backend",
        help="Starter template to use (backend, frontend, minimal, student, opensource, ai-engineer)",
    )

    # 5. validate
    validate_parser = subparsers.add_parser(
        "validate", help="Validate configuration file and widget tree"
    )
    validate_parser.add_argument(
        "--config", default="profileforge.yaml", help="Path to config file"
    )
    validate_parser.add_argument(
        "--output", default=None, help="Output directory to check write access"
    )

    # 6. templates
    templates_parser = subparsers.add_parser(
        "templates", help="Starter template commands"
    )
    templates_subparsers = templates_parser.add_subparsers(dest="templates_command")
    templates_subparsers.add_parser(
        "list", help="List all available official starter templates"
    )

    # 7. gallery
    gallery_parser = subparsers.add_parser(
        "gallery", help="Ecosystem gallery and export commands"
    )
    gallery_subparsers = gallery_parser.add_subparsers(dest="gallery_command")
    gallery_export_parser = gallery_subparsers.add_parser(
        "export",
        help="Export full theme, widget, and template gallery metadata and SVG assets",
    )
    gallery_export_parser.add_argument(
        "--out-dir",
        default="gallery",
        help="Output directory for gallery assets (default: gallery)",
    )

    # 8. themes
    themes_parser = subparsers.add_parser("themes", help="Theme commands")
    themes_subparsers = themes_parser.add_subparsers(
        dest="themes_command", required=True
    )
    themes_build_parser = themes_subparsers.add_parser(
        "build", help="Build theme gallery previews"
    )
    themes_build_parser.add_argument(
        "--config", default="profileforge.yaml", help="Path to config file"
    )

    # 9. benchmark
    benchmark_parser = subparsers.add_parser(
        "benchmark", help="Run multi-stage performance benchmark"
    )
    benchmark_parser.add_argument(
        "--config",
        "-c",
        default=None,
        help="Path to config file (default: profileforge.yaml or examples/backend/profileforge.yaml)",
    )
    benchmark_parser.add_argument(
        "--iterations",
        "-n",
        type=int,
        default=10,
        help="Number of iterations (default: 10)",
    )
    benchmark_parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output path to save JSON benchmark report",
    )
    benchmark_parser.add_argument(
        "--budget-file",
        "-b",
        default=None,
        help="Path to budget.yaml to verify SLA thresholds",
    )

    # 10. widgets
    widgets_parser = subparsers.add_parser(
        "widgets", help="Discover and inspect widgets"
    )
    widgets_subparsers = widgets_parser.add_subparsers(
        dest="widgets_command", required=True
    )
    widgets_subparsers.add_parser(
        "list", help="List all registered widgets with metadata and status badges"
    )
    widgets_info_parser = widgets_subparsers.add_parser(
        "info", help="Display detailed metadata for a specific widget"
    )
    widgets_info_parser.add_argument(
        "widget_id",
        help="ID of the widget to inspect (e.g. github_stats, hero, skills)",
    )

    args = parser.parse_args()

    if args.command == "build":
        cmd_build(args)
    elif args.command == "doctor":
        cmd_doctor(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "new":
        cmd_new(args)
    elif args.command == "templates":
        if args.templates_command in ("list", None):
            cmd_templates_list(args)
        else:
            print_error(
                f"Command 'templates {args.templates_command}' is not implemented.",
                hint="Run 'profileforge templates list'.",
            )
            sys.exit(1)
    elif args.command == "gallery":
        if args.gallery_command in ("export", None):
            cmd_gallery_export(args)
        else:
            print_error(
                f"Command 'gallery {args.gallery_command}' is not implemented.",
                hint="Run 'profileforge gallery export --out-dir gallery'.",
            )
            sys.exit(1)
    elif args.command == "themes":
        if args.themes_command == "build":
            cmd_themes_build(args)
        else:
            print_error(
                f"Command 'themes {args.themes_command}' is not implemented.",
                hint="Run 'profileforge themes build'.",
            )
            sys.exit(1)
    elif args.command == "benchmark":
        cmd_benchmark(args)
    elif args.command == "widgets":
        if args.widgets_command == "list":
            cmd_widgets_list(args)
        elif args.widgets_command == "info":
            cmd_widgets_info(args)
        else:
            print_error(
                f"Command 'widgets {args.widgets_command}' is not implemented.",
                hint="Run 'profileforge widgets list' or 'profileforge widgets info <id>'.",
            )
            sys.exit(1)
    else:
        print_error(f"Command '{args.command}' is not recognized.")
        sys.exit(1)


if __name__ == "__main__":
    main()
