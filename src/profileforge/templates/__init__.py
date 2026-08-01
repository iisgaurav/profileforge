from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from profileforge.templates.loader import (
    TEMPLATES_DIR,
    TemplateLoader,
    TemplateManifest,
)

# Backwards-compatible TEMPLATE_METADATA mapping
TEMPLATE_METADATA: Dict[str, Dict[str, Any]] = {}
for _tid in TemplateLoader.list_templates():
    _info = TemplateLoader.get_template_info(_tid)
    if _info:
        TEMPLATE_METADATA[_tid] = _info


def list_builtin_templates() -> List[str]:
    """Returns a list of all built-in template IDs."""
    return TemplateLoader.list_templates()


def get_template_info(name: str) -> Optional[Dict[str, Any]]:
    """Returns metadata for a given template ID."""
    return TemplateLoader.get_template_info(name)


def load_template_manifest(name_or_path: str | Path) -> Optional[TemplateManifest]:
    """Loads typed manifest for a given template."""
    return TemplateLoader.load_manifest(name_or_path)


def get_builtin_template_path(name: str) -> Path:
    """Returns the path to a built-in template directory."""
    return TemplateLoader.get_template_path(name)


def scaffold_template(
    template_name: str, target_dir: Path, project_name: Optional[str] = None
) -> Path:
    """Copies the template directory cleanly into the target path, renaming project name in profileforge.yaml if requested."""
    return TemplateLoader.scaffold(template_name, target_dir, project_name)


__all__ = [
    "TEMPLATES_DIR",
    "TEMPLATE_METADATA",
    "TemplateLoader",
    "TemplateManifest",
    "get_builtin_template_path",
    "get_template_info",
    "list_builtin_templates",
    "load_template_manifest",
    "scaffold_template",
]
