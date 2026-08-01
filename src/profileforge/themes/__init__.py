from pathlib import Path
from typing import List

THEMES_DIR = Path(__file__).parent


def list_builtin_themes() -> List[str]:
    """Returns a list of all built-in theme names."""
    return sorted([f.stem for f in THEMES_DIR.glob("*.yaml")])


def get_builtin_theme_path(name: str) -> Path:
    """Returns the path to a built-in theme YAML file."""
    return THEMES_DIR / f"{name}.yaml"


__all__ = ["THEMES_DIR", "get_builtin_theme_path", "list_builtin_themes"]
