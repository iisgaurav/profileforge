import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

TEMPLATES_DIR = Path(__file__).parent

TEMPLATE_METADATA: Dict[str, Dict[str, Any]] = {
    "backend": {
        "id": "backend",
        "name": "Backend Engineer",
        "description": "Tailored for backend and distributed systems engineers with skills, repositories, stats, and work experience.",
        "default_theme": "github-dark",
        "widgets": ["hero", "skills", "repositories", "github_stats", "experience"],
    },
    "frontend": {
        "id": "frontend",
        "name": "Frontend Engineer",
        "description": "Tailored for frontend, design technologist, and UI/UX developers with modern UI stack, projects, and now widget.",
        "default_theme": "modern",
        "widgets": ["hero", "skills", "repositories", "github_stats", "now"],
    },
    "minimal": {
        "id": "minimal",
        "name": "Minimalist",
        "description": "Clean, elegant monochromatic layout with essential hero identity, about bio, and featured repositories.",
        "default_theme": "minimal",
        "widgets": ["hero", "about", "repositories"],
    },
    "student": {
        "id": "student",
        "name": "Student & Learner",
        "description": "Designed for students and early-career developers with learning roadmaps, skills, projects, and social contacts.",
        "default_theme": "catppuccin-mocha",
        "widgets": ["hero", "skills", "roadmap", "repositories", "social"],
    },
    "opensource": {
        "id": "opensource",
        "name": "Open Source Maintainer",
        "description": "Showcase-focused template highlighting pinned OSS repositories, language breakdowns, GitHub stats, and community channels.",
        "default_theme": "github-dark",
        "widgets": [
            "hero",
            "repositories",
            "github_stats",
            "github_languages",
            "social",
        ],
    },
    "ai-engineer": {
        "id": "ai-engineer",
        "name": "AI & Machine Learning Engineer",
        "description": "Specialized for AI/ML engineers and researchers featuring deep learning frameworks, CUDA, LLM agents, and active research focus.",
        "default_theme": "dracula",
        "widgets": ["hero", "skills", "repositories", "now", "github_stats"],
    },
}


def list_builtin_templates() -> List[str]:
    """Returns a list of all built-in template IDs."""
    templates = []
    if TEMPLATES_DIR.exists():
        for d in sorted(TEMPLATES_DIR.iterdir()):
            if d.is_dir() and (d / "profileforge.yaml").exists():
                templates.append(d.name)
    if not templates:
        templates = sorted(list(TEMPLATE_METADATA.keys()))
    return templates


def get_template_info(name: str) -> Optional[Dict[str, Any]]:
    """Returns metadata for a given template ID."""
    if name in TEMPLATE_METADATA:
        info = dict(TEMPLATE_METADATA[name])
        info["path"] = str(TEMPLATES_DIR / name)
        return info

    template_dir = TEMPLATES_DIR / name
    if template_dir.exists() and (template_dir / "profileforge.yaml").exists():
        return {
            "id": name,
            "name": name.replace("-", " ").title(),
            "description": f"Custom template '{name}'",
            "default_theme": "github-dark",
            "widgets": [],
            "path": str(template_dir),
        }
    return None


def get_builtin_template_path(name: str) -> Path:
    """Returns the path to a built-in template directory."""
    return TEMPLATES_DIR / name


def scaffold_template(
    template_name: str, target_dir: Path, project_name: Optional[str] = None
) -> Path:
    """Copies the template directory cleanly into the target path, renaming project name in profileforge.yaml if requested."""
    src_dir = get_builtin_template_path(template_name)
    if not src_dir.exists() or not (src_dir / "profileforge.yaml").exists():
        available = ", ".join(list_builtin_templates())
        raise ValueError(
            f"Template '{template_name}' not found. Available templates: {available}"
        )

    target_dir = Path(target_dir).resolve()
    if target_dir.exists() and any(target_dir.iterdir()):
        raise FileExistsError(
            f"Target directory '{target_dir}' already exists and is not empty."
        )

    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy all files and folders recursively
    for item in src_dir.iterdir():
        if item.name.startswith("__") or item.name.startswith("."):
            continue
        dest_item = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest_item, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest_item)

    # Update project name in profileforge.yaml if custom name specified
    config_file = target_dir / "profileforge.yaml"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if project_name:
            if "project" not in data or not isinstance(data["project"], dict):
                data["project"] = {}
            data["project"]["name"] = project_name

        with open(config_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)

    return target_dir


__all__ = [
    "TEMPLATES_DIR",
    "TEMPLATE_METADATA",
    "get_builtin_template_path",
    "get_template_info",
    "list_builtin_templates",
    "scaffold_template",
]
