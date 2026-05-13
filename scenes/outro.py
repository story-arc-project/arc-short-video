"""Beat 6 — Outro (17.5–20.0s).

Browser frame collapses, ARC wordmark (gradient + arc curve) + tagline + URL
fade in for the final hold.
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
    VGroup,
    UP,
)

from components.fonts import KText, body_font, fit_to_width, heading_font
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

    wordmark = KText(
        content.BRAND_NAME,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.BRAND,
        font_size=100,
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
    logo_group.move_to([0, 1.2, 0])

    tagline = KText(
        content.OUTRO_LINE,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_700,
        font_size=22,
    )
    fit_to_width(tagline, 4.0)
    tagline.next_to(logo_group, DOWN, buff=0.55)

    url = KText(
        content.URL,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.BRAND_DARK,
        font_size=26,
    )
    url.next_to(tagline, DOWN, buff=0.28)

    scene.play(Create(arc_line), run_time=0.45)
    used += 0.45
    scene.play(FadeIn(wordmark, scale=1.05), run_time=0.35)
    used += 0.35
    scene.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.30)
    used += 0.30
    scene.play(FadeIn(url, shift=UP * 0.15), run_time=0.30)
    used += 0.30

    if duration > used:
        scene.wait(duration - used)
