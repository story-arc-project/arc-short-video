"""Beat 4 — Analyze (9.0–13.5s).

The browser frame stays put while its body content swaps to an individual
experience analysis: header card, 강점 chips, 배운 점 bullets, 추천 키워드 chips.
Sections reveal staggered so the viewer reads them in order.
"""
from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    Scene,
    Text,
    UP,
)

from components.analysis_panel import AnalysisPanel
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
        frame = BrowserFrame(width=3.7, height=6.0, url="story-arc.org/archive")
        frame.move_to([0, 0.25, 0])
        scene.play(FadeIn(frame), run_time=0.4)
        used += 0.4
    # When the frame already exists from the record beat, leave the URL bar
    # alone — it reads "story-arc.org" everywhere, which is fine for a promo.

    body_w, _ = frame.body_size()

    title = Text(
        content.ANALYZE_TITLE,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.GRAY_950,
        font_size=24,
    )
    title.move_to([
        frame.outer.get_center()[0],
        frame.body_top_left()[1] - 0.32,
        0,
    ])

    panel = AnalysisPanel(
        experience=content.ANALYZE_EXPERIENCE,
        strengths=content.ANALYZE_STRENGTHS,
        learnings=content.ANALYZE_LEARNINGS,
        keywords=content.ANALYZE_RECO_KEYWORDS,
        strengths_label=content.ANALYZE_STRENGTHS_LABEL,
        learnings_label=content.ANALYZE_LEARNINGS_LABEL,
        keywords_label=content.ANALYZE_KEYWORDS_LABEL,
        width=body_w - 0.3,
    )
    panel_top_y = title.get_bottom()[1] - 0.18
    panel.move_to([
        frame.outer.get_center()[0],
        panel_top_y - panel.height / 2,
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

    # Header + title appear together so the viewer immediately sees which
    # experience is being analyzed.
    scene.play(
        FadeIn(title, shift=UP * 0.1),
        FadeIn(panel.header, shift=UP * 0.1),
        run_time=0.45,
    )
    used += 0.45

    # Stagger the three section reveals across the bulk of the beat.
    scene.play(
        LaggedStart(
            FadeIn(panel.strengths, shift=UP * 0.12),
            FadeIn(panel.learnings, shift=UP * 0.12),
            FadeIn(panel.keywords,  shift=UP * 0.12),
            lag_ratio=0.35,
            run_time=1.7,
        )
    )
    used += 1.7

    scene.play(FadeIn(caption, shift=UP * 0.15), run_time=0.4)
    used += 0.4

    setattr(scene, "_analyze_inside", panel)
    setattr(scene, "_analyze_title", title)
    setattr(scene, "_analyze_caption", caption)
    setattr(scene, "_analyze_frame", frame)

    if duration > used:
        scene.wait(duration - used)
