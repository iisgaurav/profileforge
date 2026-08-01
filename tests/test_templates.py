import argparse
import sys
from pathlib import Path

import pytest

from profileforge.cli.main import (
    cmd_init,
    cmd_new,
    cmd_templates_list,
    main,
)
from profileforge.connectors.github.connector import GithubConnector
from profileforge.connectors.local import LocalConnector
from profileforge.core.config import ConfigLoader
from profileforge.core.context import BuildContext, Services
from profileforge.core.registry import WIDGET_REGISTRY
from profileforge.render.layout import LayoutEngine
from profileforge.render.svg.renderer import SVGRenderer
from profileforge.templates import (
    TEMPLATE_METADATA,
    get_builtin_template_path,
    get_template_info,
    list_builtin_templates,
    scaffold_template,
)

EXPECTED_TEMPLATES = [
    "ai-engineer",
    "backend",
    "frontend",
    "minimal",
    "opensource",
    "student",
]


def test_list_builtin_templates():
    templates = list_builtin_templates()
    assert isinstance(templates, list)
    for expected in EXPECTED_TEMPLATES:
        assert expected in templates


def test_template_metadata_integrity():
    for template_id in EXPECTED_TEMPLATES:
        assert template_id in TEMPLATE_METADATA
        meta = TEMPLATE_METADATA[template_id]
        assert "name" in meta
        assert "description" in meta
        assert "default_theme" in meta
        assert "widgets" in meta
        assert isinstance(meta["widgets"], list)
        assert len(meta["widgets"]) > 0

        info = get_template_info(template_id)
        assert info is not None
        assert info["id"] == template_id
        assert Path(info["path"]).exists()


def test_get_template_info_unknown():
    assert get_template_info("non_existent_template_xyz") is None


def test_template_directory_structure():
    for template_id in EXPECTED_TEMPLATES:
        template_path = get_builtin_template_path(template_id)
        assert template_path.exists(), f"Template {template_id} path does not exist"
        assert (template_path / "profileforge.yaml").exists()
        assert (template_path / "README.md").exists()
        assert (template_path / "config").exists()
        assert (template_path / "config").is_dir()


def test_template_configs_load_and_build(tmp_path):
    themes_dir = Path(__file__).parent.parent / "src" / "profileforge" / "themes"

    for template_id in EXPECTED_TEMPLATES:
        template_path = get_builtin_template_path(template_id)
        config_file = template_path / "profileforge.yaml"

        # Load main config
        config = ConfigLoader.load_main_config(str(config_file))
        assert config.active_theme
        assert len(config.widgets) > 0

        # Load theme
        theme = ConfigLoader.load_theme(config.active_theme, themes_dir=str(themes_dir))
        assert theme.name

        # Setup local connector pointing to template config dir
        local_conn = LocalConnector({"root": str(template_path / "config")})
        gh_conn = GithubConnector({"username": "octocat"})
        services = Services(connectors={"local": local_conn, "github": gh_conn})
        context = BuildContext(theme=theme, config=config, services=services)

        # Render all widgets in template
        svg_renderer = SVGRenderer(context)
        for w_conf in config.widgets:
            assert w_conf.name in WIDGET_REGISTRY, (
                f"Widget '{w_conf.name}' not registered"
            )
            widget_cls = WIDGET_REGISTRY[w_conf.name]
            widget = widget_cls()
            tree = widget.render_safe(context)
            assert tree is not None
            LayoutEngine.calculate(tree)
            svg = svg_renderer.render(tree)
            assert svg is not None
            assert len(svg) > 0


def test_scaffold_template(tmp_path):
    target = tmp_path / "my_backend_project"
    result = scaffold_template("backend", target, project_name="My Custom Backend")
    assert result == target
    assert (target / "profileforge.yaml").exists()
    assert (target / "README.md").exists()
    assert (target / "config" / "hero.yaml").exists()
    assert (target / "config" / "skills.yaml").exists()
    assert (target / "config" / "experience.yaml").exists()

    config = ConfigLoader.load_main_config(str(target / "profileforge.yaml"))
    assert config.project_name == "My Custom Backend"
    assert config.active_theme == "github-dark"


def test_scaffold_template_non_empty_fails(tmp_path):
    target = tmp_path / "existing_dir"
    target.mkdir()
    (target / "existing_file.txt").write_text("hello", encoding="utf-8")

    with pytest.raises(FileExistsError):
        scaffold_template("frontend", target)


def test_scaffold_template_unknown_fails(tmp_path):
    target = tmp_path / "target"
    with pytest.raises(ValueError, match="Template 'unknown_template' not found"):
        scaffold_template("unknown_template", target)


def test_cli_templates_list(capsys):
    args = argparse.Namespace(command="templates", templates_command="list")
    cmd_templates_list(args)
    captured = capsys.readouterr()
    assert "Available ProfileForge Starter Templates:" in captured.out
    for template_id in EXPECTED_TEMPLATES:
        assert template_id in captured.out


def test_cli_new_command(tmp_path, capsys):
    target_dir = tmp_path / "new_ai_app"
    args = argparse.Namespace(name=str(target_dir), template="ai-engineer")
    cmd_new(args)

    captured = capsys.readouterr()
    assert "Created new ProfileForge project" in captured.out
    assert (target_dir / "profileforge.yaml").exists()
    assert (target_dir / "config" / "hero.yaml").exists()


def test_cli_new_unknown_template(tmp_path, capsys):
    target_dir = tmp_path / "bad_app"
    args = argparse.Namespace(name=str(target_dir), template="does-not-exist")
    with pytest.raises(SystemExit) as exc_info:
        cmd_new(args)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Unknown template 'does-not-exist'" in captured.out


def test_cli_new_existing_dir_fails(tmp_path, capsys):
    target_dir = tmp_path / "existing"
    target_dir.mkdir()
    (target_dir / "test.txt").write_text("data", encoding="utf-8")

    args = argparse.Namespace(name=str(target_dir), template="backend")
    with pytest.raises(SystemExit) as exc_info:
        cmd_new(args)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "already exists and is not empty" in captured.out


def test_cli_init_command(tmp_path, capsys):
    target_dir = tmp_path / "init_frontend"
    target_dir.mkdir()
    args = argparse.Namespace(
        directory=str(target_dir), template="frontend", name="Custom Frontend"
    )
    cmd_init(args)

    captured = capsys.readouterr()
    assert "Initialized ProfileForge project" in captured.out
    assert (target_dir / "profileforge.yaml").exists()
    config = ConfigLoader.load_main_config(str(target_dir / "profileforge.yaml"))
    assert config.project_name == "Custom Frontend"


def test_cli_init_existing_config_fails(tmp_path, capsys):
    target_dir = tmp_path / "already_inited"
    target_dir.mkdir()
    (target_dir / "profileforge.yaml").write_text("version: 1\n", encoding="utf-8")

    args = argparse.Namespace(directory=str(target_dir), template="minimal", name=None)
    with pytest.raises(SystemExit) as exc_info:
        cmd_init(args)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "already exists" in captured.out


def test_cli_main_dispatch(monkeypatch, tmp_path, capsys):
    target_dir = tmp_path / "dispatched_student"
    test_args = ["profileforge", "new", str(target_dir), "--template", "student"]
    monkeypatch.setattr(sys, "argv", test_args)
    main()

    captured = capsys.readouterr()
    assert "Created new ProfileForge project" in captured.out
    assert (target_dir / "profileforge.yaml").exists()
