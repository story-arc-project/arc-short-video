"""Beat 5 — Use / Export (13.5–17.5s).

A horizontal tab strip appears inside the same browser frame. Tabs activate
in sequence, each revealing a tiny mock preview card to its right of style
matching the export type.
"""
from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    RIGHT,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    UP,
    VGroup,
)

from components.badge import Badge
from components.browser_chrome import BrowserFrame
from components.fonts import body_font, fit_to_width, heading_font
from config import content, theme, timing


def _make_tab(label: str, active: bool) -> VGroup:
    fg = theme.WHITE if active else theme.GRAY_700
    bg = theme.BRAND if active else theme.GRAY_100
    text = Text(label, font=body_font(), color=fg, weight=theme.WEIGHT_SEMIBOLD,
                font_size=17)
    pad_h, pad_v = 0.18, 0.10
    pill = RoundedRectangle(
        corner_radius=0.12,
        width=text.width + pad_h * 2,
        height=text.height + pad_v * 2,
        fill_color=bg,
        fill_opacity=1.0,
        stroke_width=0,
    )
    text.move_to(pill.get_center())
    return VGroup(pill, text)


def _mock_preview(kind: str, width: float, height: float) -> VGroup:
    """Tiny card mocking each export artefact — resume / cover letter / etc."""
    card = RoundedRectangle(
        corner_radius=0.14,
        width=width,
        height=height,
        fill_color=theme.WHITE,
        fill_opacity=1.0,
        stroke_color=theme.GRAY_200,
        stroke_width=theme.CARD_BORDER_W,
    )
    inner = VGroup()

    ai_badge = Badge(content.EXPORT_AI_LABEL, variant="brand", font_size=14)
    ai_badge.move_to(
        [card.get_right()[0] - 0.22 - ai_badge.width / 2,
         card.get_top()[1] - 0.22 - ai_badge.height / 2,
         0]
    )
    inner.add(ai_badge)

    # Skeleton lines.
    if kind == "이력서":
        line_widths = [1.6, 2.4, 2.0, 2.3, 1.8, 2.1, 1.5]
    elif kind == "자기소개서":
        line_widths = [2.5, 2.4, 2.5, 2.3, 2.4, 2.0, 1.6]
    elif kind == "포트폴리오":
        line_widths = [2.5, 1.4, 1.4, 2.4, 1.4, 1.4]
    else:  # 전자명함
        line_widths = [1.0, 1.6, 1.2]

    y = card.get_top()[1] - 0.7
    for w in line_widths:
        line = RoundedRectangle(
            corner_radius=0.05,
            width=min(w, width - 0.5),
            height=0.12,
            fill_color=theme.GRAY_100,
            fill_opacity=1.0,
            stroke_width=0,
        )
        line.move_to([card.get_left()[0] + 0.25 + line.width / 2, y, 0])
        inner.add(line)
        y -= 0.22

    if kind == "포트폴리오":
        # Add a couple of "image" placeholders.
        for i in range(2):
            block = RoundedRectangle(
                corner_radius=0.08,
                width=0.9,
                height=0.6,
                fill_color=theme.BRAND_LIGHT,
                fill_opacity=1.0,
                stroke_width=0,
            )
            block.move_to(
                [card.get_left()[0] + 0.55 + i * 1.05,
                 card.get_bottom()[1] + 0.55,
                 0]
            )
            inner.add(block)
    if kind == "전자명함":
        # Centered avatar dot + ARC mark.
        avatar = RoundedRectangle(
            corner_radius=0.25, width=0.5, height=0.5,
            fill_color=theme.BRAND, fill_opacity=1.0, stroke_width=0,
        )
        avatar.move_to([card.get_center()[0], card.get_center()[1] + 0.2, 0])
        inner.add(avatar)

    return VGroup(card, inner)


def play(scene: Scene) -> None:
    duration = timing.duration(timing.USE)

    frame: BrowserFrame | None = getattr(scene, "_analyze_frame", None)
    title = getattr(scene, "_analyze_title", None)
    inside = getattr(scene, "_analyze_inside", None)
    prev_caption = getattr(scene, "_analyze_caption", None)

    used = 0.0
    fades = []
    if title is not None:
        fades.append(FadeOut(title, shift=DOWN * 0.1))
    if inside is not None:
        fades.append(FadeOut(inside, shift=DOWN * 0.15))
    if prev_caption is not None:
        fades.append(FadeOut(prev_caption, shift=DOWN * 0.1))
    if fades:
        scene.play(*fades, run_time=0.3)
        used += 0.3

    if frame is None:
        frame = BrowserFrame(width=3.7, height=6.0, url="story-arc.org/export")
        frame.move_to([0, 0.25, 0])
        scene.play(FadeIn(frame), run_time=0.3)
        used += 0.3

    # Build initial tab strip with the first tab active. Auto-scale the
    # whole strip down so the four tabs fit inside the frame body width.
    body_w_for_tabs, _ = frame.body_size()
    tabs = VGroup()
    for i, name in enumerate(content.EXPORT_TABS):
        tabs.add(_make_tab(name, active=(i == 0)))
    tabs.arrange(RIGHT, buff=0.12)
    fit_to_width(tabs, body_w_for_tabs - 0.3)
    tabs.move_to([
        frame.outer.get_center()[0],
        frame.body_top_left()[1] - 0.5,
        0,
    ])

    body_w, body_h = frame.body_size()
    preview_w = body_w - 0.4
    preview_h = body_h - 1.6
    preview_y = frame.body_top_left()[1] - 0.7 - preview_h / 2

    preview = _mock_preview(content.EXPORT_TABS[0], preview_w, preview_h)
    preview.move_to([frame.outer.get_center()[0], preview_y, 0])

    caption = Text(
        content.USE_LINE,
        font=heading_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_950,
        font_size=30,
    )
    fit_to_width(caption, 4.0)
    caption.move_to([0, -3.55, 0])

    scene.play(
        FadeIn(tabs, shift=UP * 0.1),
        FadeIn(preview, shift=UP * 0.1),
        FadeIn(caption, shift=UP * 0.15),
        run_time=0.5,
    )
    used += 0.5

    # Cycle through the rest of the tabs, swapping the preview each time.
    remaining = duration - used - 0.05
    cycle_count = len(content.EXPORT_TABS) - 1  # we already showed tab 0
    per_tab = max(0.4, remaining / max(1, cycle_count))

    for i in range(1, len(content.EXPORT_TABS)):
        new_tabs = VGroup()
        for j, name in enumerate(content.EXPORT_TABS):
            new_tabs.add(_make_tab(name, active=(j == i)))
        new_tabs.arrange(RIGHT, buff=0.12)
        fit_to_width(new_tabs, body_w_for_tabs - 0.3)
        new_tabs.move_to(tabs.get_center())

        new_preview = _mock_preview(content.EXPORT_TABS[i], preview_w, preview_h)
        new_preview.move_to(preview.get_center())

        scene.play(
            tabs.animate.become(new_tabs),
            FadeOut(preview, shift=DOWN * 0.1),
            FadeIn(new_preview, shift=UP * 0.1),
            run_time=per_tab,
        )
        preview = new_preview
        used += per_tab

    setattr(scene, "_use_frame", frame)
    setattr(scene, "_use_tabs", tabs)
    setattr(scene, "_use_preview", preview)
    setattr(scene, "_use_caption", caption)

    if duration > used:
        scene.wait(duration - used)
