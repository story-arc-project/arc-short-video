"""Beat 6 — Outro (17.5–20.0s).

Browser frame collapses, ARC wordmark + tagline + URL fade in for the
final hold.
"""
from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    UP,
)

from components.fonts import body_font, fit_to_width, heading_font
from config import content, theme, timing


def play(scene: Scene) -> None:
    duration = timing.duration(timing.OUTRO)

    fades = []
    for attr in ("_use_frame", "_use_tabs", "_use_preview", "_use_caption"):
        mob = getattr(scene, attr, None)
        if mob is not None:
            fades.append(FadeOut(mob, shift=DOWN * 0.1))

    used = 0.0
    if fades:
        scene.play(*fades, run_time=0.45)
        used += 0.45

    wordmark = Text(
        content.BRAND_NAME,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.BRAND,
        font_size=130,
    )
    wordmark.move_to([0, 0.9, 0])

    tagline = Text(
        content.OUTRO_LINE,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_700,
        font_size=28,
    )
    fit_to_width(tagline, 4.0)
    tagline.move_to([0, -0.6, 0])

    url = Text(
        content.URL,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.BRAND_DARK,
        font_size=34,
    )
    url.move_to([0, -1.6, 0])

    # FadeIn (not Write) so the wordmark is visible from frame 1, avoiding
    # a flicker between the previous beat fading out and Write starting.
    scene.play(
        FadeIn(wordmark, scale=1.15, run_time=0.7),
        FadeIn(tagline, shift=UP * 0.15, run_time=0.55),
    )
    used += 0.7

    scene.play(FadeIn(url, shift=UP * 0.15), run_time=0.45)
    used += 0.45

    if duration > used:
        scene.wait(duration - used)
