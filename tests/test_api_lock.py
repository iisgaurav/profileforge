import json
import subprocess
import sys
from pathlib import Path

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.api_lock import compare_snapshots, generate_snapshot  # noqa: E402


def test_generate_snapshot():
    snapshot = generate_snapshot()
    assert snapshot["version"] == 1
    assert "modules" in snapshot
    modules = snapshot["modules"]
    assert "profileforge.components" in modules
    assert "profileforge.core.models" in modules
    assert "profileforge.widgets.base" in modules
    assert "profileforge.themes" in modules
    assert "profileforge.render" in modules


def test_api_lock_clean_comparison():
    current = generate_snapshot()
    diffs = compare_snapshots(current, current)
    assert diffs == []


def test_api_lock_detects_removed_class():
    current = generate_snapshot()
    locked = json.loads(json.dumps(current))
    locked["modules"]["profileforge.components"]["classes"]["NonExistentClass"] = {
        "doc": "Fake class",
        "bases": [],
        "is_dataclass": False,
        "fields": {},
        "methods": {},
        "attributes": {},
    }
    diffs = compare_snapshots(current, locked)
    assert any("[REMOVED CLASS]" in d for d in diffs)


def test_api_lock_detects_altered_signature():
    current = generate_snapshot()
    locked = json.loads(json.dumps(current))
    # Alter parameters of a method
    mod = locked["modules"]["profileforge.components"]
    if "Card" in mod["classes"]:
        mod["classes"]["Card"]["methods"]["__init__"]["parameters"].append(
            {
                "name": "extra_param",
                "kind": "POSITIONAL_OR_KEYWORD",
                "default": "<empty>",
                "annotation": "str",
            }
        )
    diffs = compare_snapshots(current, locked)
    assert any("[ALTERED SIGNATURE]" in d for d in diffs)


def test_api_lock_cli_check():
    lock_file = Path("api.lock.json")
    assert lock_file.exists(), "api.lock.json must exist"

    res = subprocess.run(
        [sys.executable, "tools/api_lock.py", "--check"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Check failed with output:\n{res.stdout}\n{res.stderr}"
