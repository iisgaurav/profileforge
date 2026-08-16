import pytest

from profileforge.components.layout import Column, Inline, Stack, Wrap
from profileforge.components.style import Style
from profileforge.components.widgets import Badge, Icon, Text
from profileforge.core.models import Size
from profileforge.render.layout import LayoutEngine
from profileforge.render.measurer import ApproximateTextMeasurer


@pytest.fixture
def measurer():
    return ApproximateTextMeasurer()


# -------------------------------------------------------------------
# INTRINSIC MEASUREMENT TESTS (Simulating Intrinsic Snapshots)
# -------------------------------------------------------------------

def test_intrinsic_text_empty(measurer):
    text = Text("")
    size = text.intrinsic_size(measurer)
    assert size == Size(width=0, height=18)

def test_intrinsic_text_typography_roles(measurer):
    assert Text("A", style=None).intrinsic_size(measurer) == Size(width=16, height=18)
    
    # Simulate setting font_size to typography roles via style if that was supported, 
    # but currently component.style.font_size takes the raw value or string.
    # Text sets fs_style = component.style.font_size, defaults to 14.
    text_heading = Text("Heading")
    text_heading.style.font_size = "heading"
    assert text_heading.intrinsic_size(measurer) == Size(width=107, height=32)

    text_title = Text("Title")
    text_title.style.font_size = "title"
    assert text_title.intrinsic_size(measurer) == Size(width=104, height=43)
    
    text_caption = Text("Caption")
    text_caption.style.font_size = "caption"
    assert text_caption.intrinsic_size(measurer) == Size(width=60, height=17)

def test_intrinsic_text_multiline(measurer):
    # Approximation heuristic doesn't perfectly handle newlines, but we test the interface
    text = Text("Line 1\nLine 2")
    size = text.intrinsic_size(measurer)
    assert size.width > 0
    assert size.height > 0

def test_intrinsic_text_unicode_emoji(measurer):
    text = Text("🔥🔥🔥")
    size = text.intrinsic_size(measurer)
    assert size.width == 60
    assert size.height == 18

def test_intrinsic_badge_long_text(measurer):
    badge = Badge("A very long badge text that might wrap or push boundaries")
    size = badge.intrinsic_size(measurer)
    assert size.width > 100
    assert size.height == 26

def test_intrinsic_badge_without_border(measurer):
    # Intrinsic geometry doesn't currently differ based on border, but test interface stability
    badge = Badge("Standard")
    size = badge.intrinsic_size(measurer)
    assert size.width > 70
    assert size.height == 26


def test_column_keeps_badges_intrinsic_width():
    column = Column(children=[Badge("Python")], style=Style(width="fill"))
    node = LayoutEngine.calculate(column, parent_w=400)
    assert node.width == 400
    assert node.children[0].width < 100


def test_fixed_height_column_centers_its_content():
    column = Column(
        children=[Badge("Available")],
        style=Style(width="fill", height="fill", justify="center"),
    )
    node = LayoutEngine.calculate(column, parent_w=400, parent_h=100)
    assert node.children[0].y == pytest.approx(37)


def test_inline_centers_shorter_text_against_badge():
    inline = Inline(
        children=[Text("Gold"), Badge("Legendary")],
        style=Style(align="center"),
    )
    node = LayoutEngine.calculate(inline)
    assert node.children[0].y > node.y


# -------------------------------------------------------------------
# INLINE LAYOUT TESTS
# -------------------------------------------------------------------

def test_inline_empty():
    inline = Inline(children=[])
    node = LayoutEngine.calculate(inline)
    assert node.width == 0
    assert node.height == 0

def test_inline_zero_width_children():
    inline = Inline(children=[Text("")])
    node = LayoutEngine.calculate(inline)
    assert node.width == 0
    assert node.height == 18

def test_inline_mixed_sizes():
    inline = Inline(children=[
        Icon("test.svg"),
        Badge("test")
    ])
    node = LayoutEngine.calculate(inline)
    assert len(node.children) == 2
    # Icon is 16x16, Badge is intrinsic width x 26
    assert node.height == 26
    assert node.children[0].height == 16
    assert node.children[1].height == 26
    assert node.children[1].x > node.children[0].x

def test_inline_nested_inline():
    inline = Inline(children=[
        Inline(children=[Icon("icon1")]),
        Inline(children=[Icon("icon2")])
    ])
    node = LayoutEngine.calculate(inline)
    assert node.height == 16
    assert node.width > 16

def test_inline_nested_wrap_stack():
    inline = Inline(children=[
        Wrap(children=[Icon("a"), Icon("b")]),
        Stack(children=[Icon("c")])
    ])
    node = LayoutEngine.calculate(inline)
    assert node.height >= 16
    assert node.width > 0

def test_inline_justify_center():
    inline = Inline(children=[Icon("a"), Icon("b")])
    inline.style.justify = "center"
    inline.style.width = 100
    # Forces layout engine to apply centering
    node = LayoutEngine.calculate(inline, parent_w=100)
    # The first icon's x should be > 0 since it is centered in 100px parent
    assert node.children[0].x > 0

def test_inline_justify_space_between():
    inline = Inline(children=[Icon("a"), Icon("b")])
    inline.style.justify = "space-between"
    inline.style.width = 100
    node = LayoutEngine.calculate(inline, parent_w=100)
    assert node.children[0].x == 0
    assert node.children[1].x > 50  # Pushed to the right edge
