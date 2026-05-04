"""Beat 1 — Hook (0.0–2.5s).

Six fragment cards drift in from random offsets, conveying scattered
experiences. The caption "흩어진 경험들" appears at the bottom safe area.
"""
from __future__ import annotations

import random

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    Scene,
    Text,
    UP,
    VGroup,
)

from components.card import ExperienceCard
from components.fonts import fit_to_width, heading_font
from config import content, theme, timing

random.seed(0xA1C)  # stable layout for deterministic renders


def play(scene: Scene) -> None:
    duration = timing.duration(timing.HOOK)

    cards = VGroup()
    positions = [
        (-0.95, 2.4), (0.85, 1.65), (-0.95, 0.55),
        (0.85, -0.55), (-0.95, -1.65), (0.85, -2.7),
    ]
    rotations = [-6, 4, -3, 7, -5, 3]
    for (label, date), pos, rot in zip(content.HOOK_CARDS, positions, rotations):
        card = ExperienceCard(category=label, date=date, width=1.85, height=0.62,
                              title_font_size=16, date_font_size=14)
        card.move_to([pos[0], pos[1], 0])
        card.rotate(rot * 0.0174533)
        cards.add(card)

    caption = Text(
        content.HOOK_LINE,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.GRAY_950,
        font_size=44,
    )
    fit_to_width(caption, 4.0)
    caption.move_to([0, -3.55, 0])

    scene.play(
        LaggedStart(
            *[FadeIn(c, shift=UP * 0.18) for c in cards],
            lag_ratio=0.15,
            run_time=1.4,
        )
    )
    scene.play(FadeIn(caption, shift=UP * 0.15), run_time=0.45)
    scene.wait(0.25)

    # Sweep cards into a tight cluster ready for the logo reveal.
    scene.play(
        cards.animate.scale(0.55).move_to([0, 0.6, 0]).set_opacity(0.65),
        FadeOut(caption, shift=DOWN * 0.1),
        run_time=0.4,
    )

    # Hand `cards` off to the next beat via a scene attribute so the logo
    # reveal can dissolve them inline. (Cheaper than re-creating them.)
    setattr(scene, "_hook_cards", cards)

    # Pad to the exact beat budget.
    used = 1.4 + 0.45 + 0.25 + 0.4
    if duration > used:
        scene.wait(duration - used)
