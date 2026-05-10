"""Beat 4 — Analyze (8.7–13.2s).

The browser frame stays put while its body content swaps to an individual
experience analysis matching the actual arc-frontend analysis page:
  title + badge | 한눈에 보기 overview card | 심층 분석 (강점 + 적합한 직무).
"""
from __future__ import annotations

from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    Scene,
    Text,
    Transform,
    UP,
    VGroup,
)

from components.analysis_panel import AnalysisPanel
from components.browser_chrome import BrowserFrame
from components.decor import caption_underline
from components.fonts import fit_to_width, heading_font
from config import content, theme, timing


def play(scene: Scene) -> None:
    duration = timing.duration(timing.ANALYZE)

    frame: BrowserFrame | None = getattr(scene, "_record_frame", None)
    inside = getattr(scene, "_record_inside", None)
    prev_caption = getattr(scene, "_record_caption", None)

    used = 0.0
    fade_anims = []
    if inside is not None:
        fade_anims.append(FadeOut(inside, shift=DOWN * 0.15))
    if prev_caption is not None:
        fade_anims.append(FadeOut(prev_caption, shift=DOWN * 0.1))

    if frame is None:
        frame = BrowserFrame(
            width=3.7, height=6.0, url="story-arc.org/analysis",
        )
        frame.move_to([0, 0.25, 0])
        if fade_anims:
            scene.play(*fade_anims, run_time=0.35)
            used += 0.35
        scene.play(FadeIn(frame), run_time=0.4)
        used += 0.4
    else:
        new_url = frame.make_url_text("story-arc.org/analysis")
        url_anim = Transform(frame.url_text, new_url)
        if fade_anims:
            scene.play(*fade_anims, url_anim, run_time=0.35)
        else:
            scene.play(url_anim, run_time=0.3)
        used += 0.35

    body_w, _ = frame.body_size()

    panel = AnalysisPanel(
        experience_title=content.ANALYZE_EXPERIENCE_TITLE,
        experience_badge=content.ANALYZE_EXPERIENCE_BADGE,
        overview=content.ANALYZE_OVERVIEW,
        strengths=content.ANALYZE_STRENGTHS,
        roles=content.ANALYZE_ROLES,
        strengths_label=content.ANALYZE_STRENGTHS_LABEL,
        roles_label=content.ANALYZE_ROLES_LABEL,
        width=body_w - 0.32,
    )
    panel_top_y = frame.body_top_left()[1] - 0.26
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
    caption.move_to([0, -3.2, 0])
    underline = caption_underline(caption)

    scene.play(
        FadeIn(panel.header, shift=UP * 0.1),
        run_time=0.40,
    )
    used += 0.40

    scene.play(
        LaggedStart(
            FadeIn(panel.overview, shift=UP * 0.12),
            FadeIn(panel.deep,     shift=UP * 0.12),
            lag_ratio=0.40,
            run_time=1.8,
        )
    )
    used += 1.8

    scene.play(
        FadeIn(caption, shift=UP * 0.15),
        Create(underline),
        run_time=0.4,
    )
    used += 0.4

    setattr(scene, "_analyze_inside", panel)
    setattr(scene, "_analyze_caption", VGroup(caption, underline))
    setattr(scene, "_analyze_frame", frame)

    if duration > used:
        scene.wait(duration - used)
