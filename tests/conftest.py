from pathlib import Path

import pytest

from profileforge.core.models import (
    ColorTokens,
    EffectsTokens,
    MotionTokens,
    RadiusTokens,
    ShadowTokens,
    SpacingTokens,
    Theme,
    TypographyTokens,
)


@pytest.fixture
def snapshot_dir():
    return Path(__file__).parent / "snapshots"


@pytest.fixture
def mock_theme():
    return Theme(
        name="test-theme",
        mode="modern",
        colors=ColorTokens(
            primary="#58A6FF",
            secondary="#1F6FEB",
            background="#0D1117",
            surface="#161B22",
            border="#30363D",
            text="#C9D1D9",
            muted="#8B949E",
            success="#238636",
            warning="#D29922",
            info="#58A6FF",
            accent="#F78166",
        ),
        typography=TypographyTokens(
            font_family="Inter, system-ui, sans-serif",
            heading=16,
            body=14,
            small=12,
        ),
        spacing=SpacingTokens(
            xs=4,
            sm=8,
            md=16,
            lg=24,
            xl=32,
        ),
        radius=RadiusTokens(
            card=10,
            progress=4,
            badge=12,
        ),
        shadows=ShadowTokens(
            none="none",
            low="0 1px 3px rgba(0,0,0,0.12)",
            medium="0 4px 6px rgba(0,0,0,0.16)",
            high="0 10px 24px rgba(0,0,0,0.24)",
        ),
        motion=MotionTokens(
            duration_fast=150,
            duration_normal=250,
            duration_slow=400,
            easing="ease-in-out",
        ),
        effects=EffectsTokens(
            glow="none",
            shadow="none",
            glass="none",
        ),
    )
