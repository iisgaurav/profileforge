#!/usr/bin/env python3
"""
API Snapshot Lock Tool for ProfileForge.

Inspects public symbols and API contracts across core layers:
- profileforge.components
- profileforge.core.models
- profileforge.widgets.base
- profileforge.themes
- profileforge.render

Usage:
    python tools/api_lock.py --update   # Generate or update api.lock.json
    python tools/api_lock.py --check    # Verify current code against api.lock.json
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Target modules representing the frozen public architectural layers
TARGET_MODULES = [
    "profileforge.components",
    "profileforge.components.layout",
    "profileforge.components.style",
    "profileforge.components.widgets",
    "profileforge.core.models",
    "profileforge.widgets.base",
    "profileforge.themes",
    "profileforge.render",
    "profileforge.render.base",
    "profileforge.render.layout",
    "profileforge.render.svg.renderer",
]

DEFAULT_LOCK_FILE = Path("api.lock.json")


def _format_annotation(annotation: Any) -> str:
    if annotation is inspect.Parameter.empty:
        return "<empty>"
    ann_str = str(annotation)
    # Ensure consistent cross-version formatting for Union and Generic types
    if "Union" in ann_str or "|" in ann_str or "typing." in ann_str or "[" in ann_str:
        return ann_str
    if hasattr(annotation, "__name__"):
        return annotation.__name__
    return ann_str


def _format_default(default: Any) -> str:
    if default is inspect.Parameter.empty:
        return "<empty>"
    if default is dataclasses.MISSING:
        return "<MISSING>"
    return repr(default)


def inspect_function(func: Any) -> Dict[str, Any]:
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return {"signature": "unavailable"}

    params = []
    for name, param in sig.parameters.items():
        params.append(
            {
                "name": name,
                "kind": str(param.kind),
                "default": _format_default(param.default),
                "annotation": _format_annotation(param.annotation),
            }
        )

    return {
        "parameters": params,
        "return_annotation": _format_annotation(sig.return_annotation),
    }


def inspect_class(cls: Any) -> Dict[str, Any]:
    class_info: Dict[str, Any] = {
        "doc": (cls.__doc__ or "").strip().split("\n")[0] if cls.__doc__ else "",
        "bases": [b.__name__ for b in cls.__bases__ if b is not object],
        "is_dataclass": dataclasses.is_dataclass(cls),
        "fields": {},
        "methods": {},
        "attributes": {},
    }

    if dataclasses.is_dataclass(cls):
        for f in dataclasses.fields(cls):
            class_info["fields"][f.name] = {
                "type": _format_annotation(f.type),
                "default": _format_default(f.default),
                "default_factory": (
                    f.default_factory.__name__
                    if callable(f.default_factory)
                    and f.default_factory is not dataclasses.MISSING
                    else "<empty>"
                ),
            }

    for attr_name in sorted(dir(cls)):
        if attr_name.startswith("_") and attr_name not in ("__init__",):
            continue

        try:
            attr_val = getattr(cls, attr_name)
        except Exception:
            continue

        if inspect.isfunction(attr_val) or inspect.ismethod(attr_val):
            class_info["methods"][attr_name] = inspect_function(attr_val)
        elif not dataclasses.is_dataclass(cls) or attr_name not in class_info["fields"]:
            if not inspect.isroutine(attr_val) and not isinstance(
                attr_val, (property, classmethod, staticmethod)
            ):
                if isinstance(attr_val, (int, float, str, bool, list, dict, tuple)):
                    class_info["attributes"][attr_name] = {
                        "type": type(attr_val).__name__,
                        "value": repr(attr_val),
                    }

    return class_info


def inspect_module(mod_name: str) -> Dict[str, Any]:
    try:
        mod = importlib.import_module(mod_name)
    except ImportError as e:
        return {"error": f"Failed to import {mod_name}: {e}"}

    mod_info: Dict[str, Any] = {
        "classes": {},
        "functions": {},
        "constants": {},
    }

    all_symbols = getattr(mod, "__all__", None)
    symbol_names = all_symbols if all_symbols is not None else dir(mod)

    for sym_name in sorted(symbol_names):
        if sym_name.startswith("_"):
            continue

        if not hasattr(mod, sym_name):
            continue

        sym_val = getattr(mod, sym_name)

        # Check if the symbol is defined in this module or explicitly exported via __all__
        origin_mod = getattr(sym_val, "__module__", None)
        is_exported = all_symbols is not None and sym_name in all_symbols
        is_local = origin_mod == mod_name or (
            origin_mod is not None and origin_mod.startswith("profileforge.")
        )

        if not (is_exported or is_local):
            continue

        if inspect.isclass(sym_val):
            mod_info["classes"][sym_name] = inspect_class(sym_val)
        elif inspect.isfunction(sym_val):
            mod_info["functions"][sym_name] = inspect_function(sym_val)
        elif isinstance(sym_val, (int, float, str, bool, list, dict, tuple, Path)):
            mod_info["constants"][sym_name] = {
                "type": type(sym_val).__name__,
                "value": repr(sym_val),
            }

    return mod_info


def generate_snapshot() -> Dict[str, Any]:
    # Ensure working directory is in sys.path
    cwd = os.getcwd()
    src_dir = os.path.join(cwd, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    snapshot: Dict[str, Any] = {
        "version": 1,
        "schema": "profileforge-api-lock-v1",
        "modules": {},
    }

    for mod_name in TARGET_MODULES:
        snapshot["modules"][mod_name] = inspect_module(mod_name)

    return snapshot


def compare_snapshots(current: Dict[str, Any], locked: Dict[str, Any]) -> List[str]:
    diffs: List[str] = []

    curr_mods = current.get("modules", {})
    lock_mods = locked.get("modules", {})

    for mod_name, lock_mod_data in lock_mods.items():
        if mod_name not in curr_mods:
            diffs.append(f"[REMOVED MODULE] Module '{mod_name}' is missing.")
            continue

        curr_mod_data = curr_mods[mod_name]

        # Check classes
        lock_classes = lock_mod_data.get("classes", {})
        curr_classes = curr_mod_data.get("classes", {})

        for cls_name, lock_cls in lock_classes.items():
            if cls_name not in curr_classes:
                diffs.append(
                    f"[REMOVED CLASS] Class '{cls_name}' in module '{mod_name}' was removed."
                )
                continue

            curr_cls = curr_classes[cls_name]

            # Check fields for dataclasses
            lock_fields = lock_cls.get("fields", {})
            curr_fields = curr_cls.get("fields", {})
            for f_name, lock_f in lock_fields.items():
                if f_name not in curr_fields:
                    diffs.append(
                        f"[REMOVED FIELD] Field '{f_name}' in class '{cls_name}' was removed."
                    )
                elif curr_fields[f_name]["type"] != lock_f["type"]:
                    diffs.append(
                        f"[ALTERED FIELD TYPE] Field '{f_name}' in class '{cls_name}' changed type from '{lock_f['type']}' to '{curr_fields[f_name]['type']}'."
                    )

            # Check methods
            lock_methods = lock_cls.get("methods", {})
            curr_methods = curr_cls.get("methods", {})
            for m_name, lock_m in lock_methods.items():
                if m_name not in curr_methods:
                    diffs.append(
                        f"[REMOVED METHOD] Method '{cls_name}.{m_name}' was removed."
                    )
                    continue

                curr_m = curr_methods[m_name]
                if lock_m.get("parameters") != curr_m.get("parameters"):
                    diffs.append(
                        f"[ALTERED SIGNATURE] Method '{cls_name}.{m_name}' parameters changed:\n"
                        f"    Expected: {lock_m.get('parameters')}\n"
                        f"    Actual:   {curr_m.get('parameters')}"
                    )
                if lock_m.get("return_annotation") != curr_m.get("return_annotation"):
                    diffs.append(
                        f"[ALTERED RETURN TYPE] Method '{cls_name}.{m_name}' return type changed from '{lock_m.get('return_annotation')}' to '{curr_m.get('return_annotation')}'."
                    )

        # Check functions
        lock_funcs = lock_mod_data.get("functions", {})
        curr_funcs = curr_mod_data.get("functions", {})
        for fn_name, lock_fn in lock_funcs.items():
            if fn_name not in curr_funcs:
                diffs.append(
                    f"[REMOVED FUNCTION] Function '{fn_name}' in module '{mod_name}' was removed."
                )
                continue

            curr_fn = curr_funcs[fn_name]
            if lock_fn.get("parameters") != curr_fn.get("parameters"):
                diffs.append(
                    f"[ALTERED SIGNATURE] Function '{mod_name}.{fn_name}' parameters changed:\n"
                    f"    Expected: {lock_fn.get('parameters')}\n"
                    f"    Actual:   {curr_fn.get('parameters')}"
                )
            if lock_fn.get("return_annotation") != curr_fn.get("return_annotation"):
                diffs.append(
                    f"[ALTERED RETURN TYPE] Function '{mod_name}.{fn_name}' return type changed from '{lock_fn.get('return_annotation')}' to '{curr_fn.get('return_annotation')}'."
                )

        # Check constants
        lock_consts = lock_mod_data.get("constants", {})
        curr_consts = curr_mod_data.get("constants", {})
        for c_name, lock_c in lock_consts.items():
            if c_name not in curr_consts:
                diffs.append(
                    f"[REMOVED CONSTANT] Constant '{c_name}' in module '{mod_name}' was removed."
                )

    # Check for newly added symbols not reflected in lock file
    for mod_name, curr_mod_data in curr_mods.items():
        if mod_name not in lock_mods:
            diffs.append(
                f"[NEW UNLOCKED MODULE] Module '{mod_name}' is not recorded in api.lock.json."
            )
            continue
        lock_mod_data = lock_mods[mod_name]
        for cls_name in curr_mod_data.get("classes", {}):
            if cls_name not in lock_mod_data.get("classes", {}):
                diffs.append(
                    f"[NEW UNLOCKED CLASS] Class '{cls_name}' in module '{mod_name}' is not in api.lock.json."
                )
        for fn_name in curr_mod_data.get("functions", {}):
            if fn_name not in lock_mod_data.get("functions", {}):
                diffs.append(
                    f"[NEW UNLOCKED FUNCTION] Function '{fn_name}' in module '{mod_name}' is not in api.lock.json."
                )

    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ProfileForge API Snapshot Lock & Verification"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Generate or update the api.lock.json snapshot file.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the current codebase against api.lock.json.",
    )
    parser.add_argument(
        "--lock-file",
        type=Path,
        default=DEFAULT_LOCK_FILE,
        help="Path to the api.lock.json file (default: api.lock.json).",
    )

    args = parser.parse_args()

    if not args.update and not args.check:
        parser.print_help()
        return 1

    lock_path = args.lock_file

    if args.update:
        print(f"Generating API snapshot lock to {lock_path}...")
        snapshot = generate_snapshot()
        with open(lock_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"[OK] Successfully wrote {lock_path}")
        return 0

    if args.check:
        if not lock_path.exists():
            print(
                f"[ERROR] Lock file '{lock_path}' not found. Run 'python tools/api_lock.py --update' to create it.",
                file=sys.stderr,
            )
            return 1

        print(f"Checking API signatures against {lock_path}...")
        with open(lock_path, "r", encoding="utf-8") as f:
            locked_snapshot = json.load(f)

        current_snapshot = generate_snapshot()
        diffs = compare_snapshots(current_snapshot, locked_snapshot)

        if diffs:
            print(
                f"\n[FAIL] Detected {len(diffs)} API contract discrepancies:",
                file=sys.stderr,
            )
            for diff in diffs:
                print(f"  * {diff}", file=sys.stderr)
            print(
                "\nAPI breaking changes require an approved RFC. If this change was approved, run 'python tools/api_lock.py --update' and commit the updated api.lock.json.",
                file=sys.stderr,
            )
            return 1

        print("[OK] API Lock Check Passed: Public API matches api.lock.json cleanly.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
