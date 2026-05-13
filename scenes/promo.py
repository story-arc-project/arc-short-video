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

import numpy as np

from manim import ImageMobject, Scene, config

from config import theme
from scenes import analyze, hook, logo, outro, record, use

config.background_color = theme.BRAND_LIGHT


def _backdrop() -> ImageMobject:
    """Diagonal cream gradient: #ffb8a0 at upper-left/lower-right, #ffefe6 at center."""
    h, w = config.pixel_height, config.pixel_width
    xs = np.linspace(-1.0, 1.0, w)[np.newaxis, :]
    ys = np.linspace(-1.0, 1.0, h)[:, np.newaxis]
    t = np.clip(np.abs(xs + ys) / 2.0, 0.0, 1.0)[:, :, np.newaxis]
    c_edge = np.array([0xFF, 0xB8, 0xA0], dtype=float)
    c_mid = np.array([0xFF, 0xEF, 0xE6], dtype=float)
    rgb = (c_mid * (1.0 - t) + c_edge * t).astype(np.uint8)
    alpha = np.full((h, w, 1), 255, dtype=np.uint8)
    mob = ImageMobject(np.concatenate([rgb, alpha], axis=2))
    mob.height = config.frame_height
    mob.set_z_index(-10)
    return mob


class ARCPromo(Scene):
    def construct(self) -> None:
        self.add(_backdrop())
        hook.play(self)
        logo.play(self)
        record.play(self)
        analyze.play(self)
        use.play(self)
        outro.play(self)
