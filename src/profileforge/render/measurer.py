from __future__ import annotations

__layer__ = "Layer 4 — Layout"

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from profileforge.core.models import Size, TypographyRole

if TYPE_CHECKING:
    from profileforge.core.models import TypographyTokens

class IntrinsicMeasurer(ABC):
    """Abstract base class for intrinsic layout measurements."""
    
    @abstractmethod
    def measure_text(
        self,
        text: str,
        typography: Union[int, str, TypographyRole, None],
        font_weight: Union[str, int] = "normal",
        font_family: str | None = None,
    ) -> Size:
        """Measure the intrinsic width and height of a text string."""
        pass


class ApproximateTextMeasurer(IntrinsicMeasurer):
    """
    Default measurer using a heuristic (0.55 width ratio).
    Does not require a browser or external font rendering library.
    """

    def measure_text(
        self,
        text: str,
        typography: Union[int, str, TypographyRole, None],
        font_weight: Union[str, int] = "normal",
        font_family: str | None = None,
    ) -> Size:
        # Base font sizes
        fs_val = 14
        if isinstance(typography, (int, float)):
            fs_val = int(typography)
        elif typography in ("heading", TypographyRole.HEADING):
            fs_val = 24
        elif typography in ("label", TypographyRole.LABEL):
            fs_val = 14
        elif typography in ("small",):
            fs_val = 12
        elif typography in ("caption", TypographyRole.CAPTION):
            # TypographyTokens uses 13px captions by default.  Measuring them at
            # 11px was the source of clipped badge labels in the rendered SVG.
            fs_val = 13
        elif typography in ("value", TypographyRole.VALUE):
            fs_val = 32
        elif typography in ("title", TypographyRole.TITLE):
            fs_val = 32

        # Measure the widest line; SVG renders line breaks vertically rather
        # than extending one continuous text run.
        upper_count = 0
        emoji_count = 0
        normal_count = 0
        widest_line = 0.0
        
        for c in text:
            if c == "\n":
                widest_line = max(widest_line, normal_count * 0.58 + upper_count * 0.75 + emoji_count * 1.3)
                upper_count = emoji_count = normal_count = 0
                continue
            # Simple emoji detection based on high unicode code points
            if ord(c) > 0x2600:
                emoji_count += 1
            elif c.isupper():
                upper_count += 1
            else:
                normal_count += 1
                
        # Emojis are usually square (1.3x font size to account for spacing)
        # Uppercase letters are wider (~0.75)
        # Normal characters (~0.58)
        widest_line = max(widest_line, normal_count * 0.58 + upper_count * 0.75 + emoji_count * 1.3)
        w = widest_line * fs_val
        
        # Semi-bold glyphs are slightly wider, but a large multiplier makes the
        # layout visibly loose compared with browser SVG text rendering.
        is_bold = str(font_weight) in ("bold", "700", "800", "900", "bolder")
        if is_bold:
            w *= 1.05
            
        w = int(w)
        
        # Keep a small safety buffer for font fallback differences, without
        # giving an empty string a phantom width.
        if text:
            w += 6

        # Text is rendered with a 1.35 line-height.  Account for explicit line
        # breaks so vertical rhythm remains stable for user-provided copy.
        line_count = max(1, text.count("\n") + 1)
        h = int(fs_val * 1.35) * line_count
        return Size(width=w, height=h)


class CairoTextMeasurer(IntrinsicMeasurer):
    """Font-metric text measurement backed by Cairo when it is available.

    Cairo is intentionally optional so the CLI remains usable in minimal
    installations.  Callers should acquire a measurer through
    :func:`create_text_measurer`, which falls back to ApproximateTextMeasurer
    only when Cairo or the requested font is unavailable.
    """

    def __init__(self, typography: "TypographyTokens", font_family: str | None = None):
        try:
            import cairo  # type: ignore[import-not-found]
        except ImportError as error:
            raise RuntimeError("pycairo is not installed") from error

        self._cairo = cairo
        self.typography = typography
        self.font_family = font_family or typography.font_family
        self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
        self._context = cairo.Context(self._surface)

    @staticmethod
    def is_available() -> bool:
        try:
            import importlib.util
            return importlib.util.find_spec("cairo") is not None
        except ImportError:
            return False
        return True

    def _font_size(self, typography: Union[int, str, TypographyRole, None]) -> int:
        if isinstance(typography, (int, float)):
            return int(typography)
        role = typography.value if isinstance(typography, TypographyRole) else typography
        return getattr(self.typography, role or "body", self.typography.body)

    def measure_text(
        self,
        text: str,
        typography: Union[int, str, TypographyRole, None],
        font_weight: Union[str, int] = "normal",
        font_family: str | None = None,
    ) -> Size:
        cairo = self._cairo
        font_name = (font_family or self.font_family).split(",")[0].strip(" '\"") or "sans-serif"
        weight = cairo.FONT_WEIGHT_BOLD if str(font_weight) in ("bold", "700", "800", "900", "bolder", "600") else cairo.FONT_WEIGHT_NORMAL
        self._context.select_font_face(font_name, cairo.FONT_SLANT_NORMAL, weight)
        size = self._font_size(typography)
        self._context.set_font_size(size)

        lines = text.split("\n")
        width = max((self._context.text_extents(line).x_advance for line in lines), default=0.0)
        line_height = max(self._context.font_extents().height, size * 1.35)
        return Size(
            width=math.ceil(width),
            height=math.ceil(line_height * max(1, len(lines))),
        )


def create_text_measurer(typography: "TypographyTokens") -> IntrinsicMeasurer:
    """Return the highest-fidelity local text measurer available."""
    if CairoTextMeasurer.is_available():
        try:
            return CairoTextMeasurer(typography)
        except RuntimeError:
            pass
    return ApproximateTextMeasurer()
