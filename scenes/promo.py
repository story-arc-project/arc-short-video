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

from manim import Scene, config

from config import theme
from scenes import analyze, hook, logo, outro, record, use

config.background_color = theme.WHITE


class ARCPromo(Scene):
    def construct(self) -> None:
        hook.play(self)
        logo.play(self)
        record.play(self)
        analyze.play(self)
        use.play(self)
        outro.play(self)
