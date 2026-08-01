from __future__ import annotations

import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

TEMPLATES_DIR = Path(__file__).parent


@dataclass
class TemplateManifest:
    """Schema descriptor for ProfileForge starter template manifests."""

    id: str
    name: str
    description: str = ""
    version: str = "1.0.0"
    minimum_profileforge: str = "1.0.0"
    author: str = "ProfileForge Team"
    license: str = "MIT"
    schema: int = 1
    widgets: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TemplateManifest:
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=str(data.get("version", "1.0.0")),
            minimum_profileforge=str(data.get("minimum_profileforge", "1.0.0")),
            author=data.get("author", "ProfileForge Team"),
            license=data.get("license", "MIT"),
            schema=int(data.get("schema", 1)),
            widgets=list(data.get("widgets", [])),
            themes=list(data.get("themes", [])),
            tags=list(data.get("tags", [])),
        )


class TemplateLoader:
    """Loader and manager for built-in and external template manifests and scaffolding."""

    @staticmethod
    def get_template_path(name_or_path: str | Path) -> Path:
        p = Path(name_or_path)
        if p.is_dir():
            return p
        return TEMPLATES_DIR / str(name_or_path)

    @classmethod
    def load_manifest(
        cls, template_dir_or_id: str | Path
    ) -> Optional[TemplateManifest]:
        template_dir = cls.get_template_path(template_dir_or_id)
        manifest_file = template_dir / "manifest.yaml"

        if manifest_file.exists():
            try:
                with open(manifest_file, "r", encoding="utf-8") as f:
                    raw_data = yaml.safe_load(f) or {}
                return TemplateManifest.from_dict(raw_data)
            except Exception:
                pass

        # Fallback to config inspection if manifest not present
        config_file = template_dir / "profileforge.yaml"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
                proj = cfg.get("project", {})
                tid = template_dir.name
                widgets = [
                    w.get("name") for w in cfg.get("widgets", []) if isinstance(w, dict)
                ]
                theme = cfg.get("themes", {}).get("active", "github-dark")
                return TemplateManifest(
                    id=tid,
                    name=proj.get("name", tid.replace("-", " ").title()),
                    description=proj.get("title", f"Starter template '{tid}'"),
                    widgets=widgets,
                    themes=[theme],
                    tags=[tid],
                )
            except Exception:
                pass

        return None

    @classmethod
    def list_templates(cls) -> List[str]:
        templates = []
        if TEMPLATES_DIR.exists():
            for d in sorted(TEMPLATES_DIR.iterdir()):
                if d.is_dir() and (d / "profileforge.yaml").exists():
                    templates.append(d.name)
        return templates

    @classmethod
    def get_template_info(cls, name: str) -> Optional[Dict[str, Any]]:
        manifest = cls.load_manifest(name)
        template_dir = cls.get_template_path(name)

        if manifest:
            info = manifest.to_dict()
            info["path"] = str(template_dir)
            if "default_theme" not in info:
                info["default_theme"] = (
                    manifest.themes[0] if manifest.themes else "github-dark"
                )
            return info

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

    @classmethod
    def scaffold(
        cls,
        template_name: str,
        target_dir: Path | str,
        project_name: Optional[str] = None,
    ) -> Path:
        src_dir = cls.get_template_path(template_name)
        if not src_dir.exists() or not (src_dir / "profileforge.yaml").exists():
            available = ", ".join(cls.list_templates())
            raise ValueError(
                f"Template '{template_name}' not found. Available templates: {available}"
            )

        target = Path(target_dir).resolve()
        if target.exists() and any(target.iterdir()):
            raise FileExistsError(
                f"Target directory '{target}' already exists and is not empty."
            )

        target.mkdir(parents=True, exist_ok=True)

        for item in src_dir.iterdir():
            if item.name.startswith("__") or item.name.startswith("."):
                continue
            dest_item = target / item.name
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_item)

        config_file = target / "profileforge.yaml"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}

            if project_name:
                if "project" not in data or not isinstance(data["project"], dict):
                    data["project"] = {}
                data["project"]["name"] = project_name

            with open(config_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, sort_keys=False)

        return target
