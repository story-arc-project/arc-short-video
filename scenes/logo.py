"""Beat 2 — Logo reveal (2.1–4.0s).

The scattered cards from the hook collapse into the center and the ARC
wordmark draws on top with an arc curve and gradient, with the tagline
fading in below.
"""
from __future__ import annotations

from manim import (
    Arc,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    PI,
    Scene,
    Text,
    UP,
    VGroup,
)

from components.fonts import KText, body_font, fit_to_width, heading_font
from config import content, theme, timing


def play(scene: Scene) -> None:
    duration = timing.duration(timing.LOGO)

    wordmark = KText(
        content.BRAND_NAME,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.BRAND,
        font_size=88,
    )
    wordmark.set_color_by_gradient(theme.LOGO_GRAD_START, theme.LOGO_GRAD_END)

    arc_line = Arc(
        radius=wordmark.width * theme.LOGO_ARC_RADIUS_RATIO,
        start_angle=PI / 2 + theme.LOGO_ARC_START_OFFSET,
        angle=-theme.LOGO_ARC_ANGLE,
        stroke_color=theme.LOGO_GRAD_START,
        stroke_width=5,
    )
    arc_line.next_to(wordmark, UP, buff=0.18)

    logo_group = VGroup(arc_line, wordmark)
    logo_group.move_to([0, 0.5, 0])

    tagline = KText(
        content.LOGO_LINE,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_700,
        font_size=22,
    )
    fit_to_width(tagline, 4.0)
    tagline.next_to(logo_group, DOWN, buff=0.5)

    cards = getattr(scene, "_hook_cards", None)
    used = 0.0
    if cards is not None:
        scene.play(FadeOut(cards, scale=0.4), run_time=0.30)
        used += 0.30

    # Arc draws left→right, then wordmark fades in below it.
    scene.play(Create(arc_line), run_time=0.45)
    used += 0.45
    scene.play(FadeIn(wordmark, scale=1.05), run_time=0.35)
    used += 0.35
    scene.play(FadeIn(tagline, shift=DOWN * 0.1), run_time=0.25)
    used += 0.25

    setattr(scene, "_logo_wordmark", logo_group)
    setattr(scene, "_logo_tagline", tagline)

    if duration > used:
        scene.wait(duration - used)
