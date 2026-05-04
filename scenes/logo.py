"""Beat 2 — Logo reveal (2.5–4.5s).

The scattered cards from the hook collapse into the center and the ARC
wordmark draws on top, with the tagline fading in below.
"""
from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    Write,
)

from components.fonts import body_font, fit_to_width, heading_font
from config import content, theme, timing


def play(scene: Scene) -> None:
    duration = timing.duration(timing.LOGO)

    wordmark = Text(
        content.BRAND_NAME,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.BRAND,
        font_size=110,
    )
    wordmark.move_to([0, 0.4, 0])

    tagline = Text(
        content.LOGO_LINE,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_700,
        font_size=28,
    )
    fit_to_width(tagline, 4.0)
    tagline.move_to([0, -1.2, 0])

    cards = getattr(scene, "_hook_cards", None)
    used = 0.0
    if cards is not None:
        scene.play(FadeOut(cards, scale=0.4), run_time=0.45)
        used += 0.45

    scene.play(Write(wordmark), run_time=0.85)
    used += 0.85
    scene.play(FadeIn(tagline, shift=DOWN * 0.1), run_time=0.4)
    used += 0.4
    scene.wait(0.2)
    used += 0.2

    setattr(scene, "_logo_wordmark", wordmark)
    setattr(scene, "_logo_tagline", tagline)

    if duration > used:
        scene.wait(duration - used)
