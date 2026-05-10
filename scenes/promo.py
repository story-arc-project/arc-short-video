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

from manim import RoundedRectangle, Scene, VGroup, config

from config import theme
from scenes import analyze, hook, logo, outro, record, use

config.background_color = theme.GRAY_50


def _backdrop() -> VGroup:
    """Soft brand-tinted blobs anchored just outside the safe area corners."""
    blob_lt = RoundedRectangle(
        corner_radius=2.0,
        width=4.0,
        height=4.0,
        fill_color=theme.BRAND_LIGHT,
        fill_opacity=0.55,
        stroke_width=0,
    ).move_to([-2.6, 3.6, 0])
    blob_rb = RoundedRectangle(
        corner_radius=2.2,
        width=4.4,
        height=4.4,
        fill_color=theme.GRADIENT_END,
        fill_opacity=0.30,
        stroke_width=0,
    ).move_to([2.4, -3.6, 0])
    backdrop = VGroup(blob_lt, blob_rb)
    backdrop.set_z_index(-10)
    return backdrop


class ARCPromo(Scene):
    def construct(self) -> None:
        self.add(_backdrop())
        hook.play(self)
        logo.play(self)
        record.play(self)
        analyze.play(self)
        use.play(self)
        outro.play(self)
