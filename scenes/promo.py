"""Top-level 20-second promo. Renders ARCPromo with `bash render.sh`.

Each beat lives in its own ``scenes/<beat>.py`` module that exports a
single ``play(scene)`` function. Reordering or muting a beat is a one-line
edit below.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow `manim scenes/promo.py ARCPromo` to import sibling packages even
# though manim invokes the file directly rather than the package.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from manim import PI, Rectangle, Scene, VGroup, config

from config import theme
from scenes import analyze, hook, logo, outro, record, use

config.background_color = theme.BRAND_LIGHT


def _backdrop() -> VGroup:
    """Diagonal orange gradient — deep brand orange to soft cream."""
    rect = Rectangle(
        width=config.frame_width * 1.7,
        height=config.frame_height * 1.7,
        stroke_width=0,
    )
    rect.set_color_by_gradient(theme.BRAND_DARK, theme.BRAND, theme.BRAND_LIGHT)
    rect.rotate(PI / 4)
    rect.set_z_index(-10)
    return rect


class ARCPromo(Scene):
    def construct(self) -> None:
        self.add(_backdrop())
        hook.play(self)
        logo.play(self)
        record.play(self)
        analyze.play(self)
        use.play(self)
        outro.play(self)
