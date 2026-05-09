"""Small decorative helpers shared across beats."""
from __future__ import annotations

from manim import RoundedRectangle, Text

from config import theme


def caption_underline(
    caption: Text,
    width_ratio: float = 0.42,
    color: str = theme.BRAND,
    height: float = 0.06,
    gap: float = 0.16,
) -> RoundedRectangle:
    """A short brand-colored bar centered under a caption."""
    bar = RoundedRectangle(
        corner_radius=height / 2,
        width=max(0.6, caption.width * width_ratio),
        height=height,
        fill_color=color,
        fill_opacity=1.0,
        stroke_width=0,
    )
    bar.move_to([
        caption.get_center()[0],
        caption.get_bottom()[1] - gap,
        0,
    ])
    return bar
