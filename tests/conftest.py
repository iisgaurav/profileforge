from pathlib import Path

import pytest


@pytest.fixture
def snapshot_dir():
    return Path(__file__).parent / "snapshots"


@pytest.fixture
def mock_theme():
    from profileforge.core.models import Theme

    return Theme(
        name="test-theme",
        background="#000000",
        primary="#FF0000",
        secondary="#00FF00",
        text="#FFFFFF",
        text_muted="#888888",
        border="#333333",
        progress_bg="#111111",
    )
