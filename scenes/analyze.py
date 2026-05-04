"""Beat 4 — Analyze (9.0–13.5s).

The browser frame stays put while its body content swaps to a keyword
analysis chart. Bars fill left-to-right and percentages count up.
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

from components.bar_chart import KeywordBars
from components.browser_chrome import BrowserFrame
from components.fonts import fit_to_width, heading_font
from config import content, theme, timing


def play(scene: Scene) -> None:
    duration = timing.duration(timing.ANALYZE)

    frame: BrowserFrame | None = getattr(scene, "_record_frame", None)
    inside = getattr(scene, "_record_inside", None)
    prev_caption = getattr(scene, "_record_caption", None)

    used = 0.0
    if inside is not None:
        scene.play(FadeOut(inside, shift=DOWN * 0.15), run_time=0.35)
        used += 0.35
    if prev_caption is not None:
        scene.play(FadeOut(prev_caption, shift=DOWN * 0.1), run_time=0.2)
        used += 0.2

    if frame is None:
        # Defensive: render a fresh frame if record beat is skipped.
        frame = BrowserFrame(width=3.7, height=6.0, url="story-arc.org/analyze")
        frame.move_to([0, 0.25, 0])
        scene.play(FadeIn(frame), run_time=0.4)
        used += 0.4
    # When the frame already exists from the record beat, leave the URL bar
    # alone — it reads "story-arc.org" everywhere, which is fine for a promo.

    title = Text(
        content.ANALYZE_TITLE,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.GRAY_950,
        font_size=28,
    )
    title.move_to([
        frame.outer.get_center()[0],
        frame.body_top_left()[1] - 0.45,
        0,
    ])

    chart = KeywordBars(content.ANALYZE_KEYWORDS, width=3.2)
    chart.move_to([
        frame.outer.get_center()[0],
        frame.body_top_left()[1] - 2.6,
        0,
    ])

    caption = Text(
        content.ANALYZE_LINE,
        font=heading_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_950,
        font_size=30,
    )
    fit_to_width(caption, 4.0)
    caption.move_to([0, -3.55, 0])

    scene.play(FadeIn(title, shift=UP * 0.1), FadeIn(chart, shift=UP * 0.1), run_time=0.45)
    used += 0.45

    scene.play(chart.progress.animate.set_value(1.0), run_time=2.0)
    used += 2.0

    scene.play(FadeIn(caption, shift=UP * 0.15), run_time=0.4)
    used += 0.4

    setattr(scene, "_analyze_inside", chart)
    setattr(scene, "_analyze_title", title)
    setattr(scene, "_analyze_caption", caption)
    setattr(scene, "_analyze_frame", frame)

    if duration > used:
        scene.wait(duration - used)
