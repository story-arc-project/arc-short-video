"""Beat 5 — Use / Export (13.5–17.5s).

A horizontal tab strip appears inside the same browser frame. Tabs activate
in sequence, each revealing a tiny mock preview card matching the export
type (이력서 / 자기소개서 / 포트폴리오).
"""
from __future__ import annotations

from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    RIGHT,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    Transform,
    UP,
    VGroup,
)

from components.badge import Badge
from components.browser_chrome import BrowserFrame
from components.decor import caption_underline
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


def _skeleton_line(width: float, height: float = 0.10,
                   color: str = theme.GRAY_100, opacity: float = 1.0) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=height / 2,
        width=max(0.4, width),
        height=height,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=0,
    )


def _resume_preview(card: RoundedRectangle, inset_x: float, top_y: float,
                    avail_w: float) -> VGroup:
    inner = VGroup()
    left_x = card.get_left()[0] + inset_x

    name = Text(content.RESUME_NAME, font=heading_font(),
                weight=theme.WEIGHT_BOLD, color=theme.GRAY_950, font_size=22)
    if name.width > avail_w:
        name.scale(avail_w / name.width)
    name.move_to([left_x + name.width / 2, top_y - name.height / 2, 0])
    inner.add(name)

    sub = Text(content.RESUME_SUBTITLE, font=body_font(),
               color=theme.GRAY_500, font_size=13)
    if sub.width > avail_w:
        sub.scale(avail_w / sub.width)
    sub.next_to(name, DOWN, buff=0.10).align_to(name, LEFT)
    inner.add(sub)

    divider = _skeleton_line(avail_w, height=0.04,
                             color=theme.GRAY_200, opacity=1.0)
    divider.next_to(sub, DOWN, buff=0.18).align_to(name, LEFT)
    divider.shift(RIGHT * (divider.width / 2))
    divider.move_to([left_x + avail_w / 2, divider.get_center()[1], 0])
    inner.add(divider)

    section_widths = [[1.6, 2.1], [1.9, 2.0, 1.4], [1.3, 1.7]]
    cursor_y = divider.get_bottom()[1] - 0.18
    for label, widths in zip(content.RESUME_SECTIONS, section_widths):
        head = Text(label, font=heading_font(), weight=theme.WEIGHT_SEMIBOLD,
                    color=theme.BRAND_DARK, font_size=14)
        head.move_to([left_x + head.width / 2, cursor_y - head.height / 2, 0])
        inner.add(head)
        cursor_y = head.get_bottom()[1] - 0.10
        for w in widths:
            line = _skeleton_line(min(w, avail_w))
            line.move_to([left_x + line.width / 2, cursor_y - line.height / 2, 0])
            inner.add(line)
            cursor_y = line.get_bottom()[1] - 0.10
        cursor_y -= 0.08
    return inner


def _cover_preview(card: RoundedRectangle, inset_x: float, top_y: float,
                   avail_w: float) -> VGroup:
    inner = VGroup()
    left_x = card.get_left()[0] + inset_x

    title = Text(content.COVER_TITLE, font=heading_font(),
                 weight=theme.WEIGHT_BOLD, color=theme.GRAY_950, font_size=22)
    if title.width > avail_w:
        title.scale(avail_w / title.width)
    title.move_to([left_x + title.width / 2, top_y - title.height / 2, 0])
    inner.add(title)

    underline = _skeleton_line(0.6, height=0.05, color=theme.BRAND, opacity=1.0)
    underline.move_to([
        left_x + underline.width / 2,
        title.get_bottom()[1] - 0.10 - underline.height / 2,
        0,
    ])
    inner.add(underline)

    cursor_y = underline.get_bottom()[1] - 0.20
    paragraph_widths = [
        avail_w - 0.05, avail_w - 0.20, avail_w - 0.10, avail_w - 0.45,
    ]
    for w in paragraph_widths:
        line = _skeleton_line(w)
        line.move_to([left_x + line.width / 2, cursor_y - line.height / 2, 0])
        inner.add(line)
        cursor_y = line.get_bottom()[1] - 0.13

    cursor_y -= 0.06
    highlight = Text(content.COVER_HIGHLIGHT, font=body_font(),
                     weight=theme.WEIGHT_SEMIBOLD,
                     color=theme.BRAND_DARK, font_size=13)
    if highlight.width > avail_w:
        highlight.scale(avail_w / highlight.width)
    highlight_bg = RoundedRectangle(
        corner_radius=0.08,
        width=highlight.width + 0.20,
        height=highlight.height + 0.14,
        fill_color=theme.BRAND_LIGHT,
        fill_opacity=1.0,
        stroke_width=0,
    )
    highlight_bg.move_to([
        left_x + highlight_bg.width / 2,
        cursor_y - highlight_bg.height / 2,
        0,
    ])
    highlight.move_to(highlight_bg.get_center())
    inner.add(highlight_bg, highlight)
    cursor_y = highlight_bg.get_bottom()[1] - 0.18

    tail_widths = [avail_w - 0.10, avail_w - 0.30, avail_w - 0.50]
    for w in tail_widths:
        line = _skeleton_line(w)
        line.move_to([left_x + line.width / 2, cursor_y - line.height / 2, 0])
        inner.add(line)
        cursor_y = line.get_bottom()[1] - 0.13

    return inner


def _portfolio_preview(card: RoundedRectangle, inset_x: float, top_y: float,
                       avail_w: float, avail_h: float) -> VGroup:
    inner = VGroup()
    left_x = card.get_left()[0] + inset_x

    title = Text(content.PORTFOLIO_TITLE, font=heading_font(),
                 weight=theme.WEIGHT_BOLD, color=theme.GRAY_950, font_size=20)
    if title.width > avail_w:
        title.scale(avail_w / title.width)
    title.move_to([left_x + title.width / 2, top_y - title.height / 2, 0])
    inner.add(title)

    grid_top_y = title.get_bottom()[1] - 0.22
    cols = 2
    rows = 2
    gap = 0.16
    tile_w = (avail_w - gap * (cols - 1)) / cols
    tile_h = min(0.95, (avail_h - 1.4) / rows - gap)

    captions = list(content.PORTFOLIO_CAPTIONS) + [""] * (rows * cols)
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            cx = left_x + tile_w / 2 + c * (tile_w + gap)
            cy = grid_top_y - tile_h / 2 - r * (tile_h + gap + 0.18)
            tile = RoundedRectangle(
                corner_radius=0.12,
                width=tile_w,
                height=tile_h,
                fill_color=theme.BRAND_LIGHT,
                fill_opacity=1.0,
                stroke_color=theme.BRAND,
                stroke_width=1.0,
            )
            tile.move_to([cx, cy, 0])
            inner.add(tile)

            inner_dot = RoundedRectangle(
                corner_radius=0.05,
                width=tile_w * 0.55,
                height=0.10,
                fill_color=theme.BRAND,
                fill_opacity=0.55,
                stroke_width=0,
            )
            inner_dot.move_to([cx, cy + 0.08, 0])
            inner.add(inner_dot)

            cap_text = captions[idx]
            if cap_text:
                cap = Text(cap_text, font=body_font(),
                           color=theme.GRAY_700, font_size=12)
                if cap.width > tile_w - 0.05:
                    cap.scale((tile_w - 0.05) / cap.width)
                cap.move_to([
                    cx,
                    tile.get_bottom()[1] - 0.09 - cap.height / 2,
                    0,
                ])
                inner.add(cap)
    return inner


def _mock_preview(kind: str, width: float, height: float) -> VGroup:
    """Mock card matching each export artefact — resume / cover letter / portfolio."""
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

    type_badge = Badge(kind, variant="brand", font_size=12,
                       h_padding=0.10, v_padding=0.05)
    type_badge.move_to([
        card.get_left()[0] + 0.22 + type_badge.width / 2,
        card.get_top()[1] - 0.22 - type_badge.height / 2,
        0,
    ])
    inner.add(type_badge)

    ai_badge = Badge(content.EXPORT_AI_LABEL, variant="brand", font_size=12,
                     h_padding=0.10, v_padding=0.05)
    ai_badge.move_to([
        card.get_right()[0] - 0.22 - ai_badge.width / 2,
        card.get_top()[1] - 0.22 - ai_badge.height / 2,
        0,
    ])
    inner.add(ai_badge)

    inset_x = 0.26
    top_y = type_badge.get_bottom()[1] - 0.22
    avail_w = width - inset_x * 2
    avail_h = top_y - card.get_bottom()[1] - 0.20

    if kind == "이력서":
        body = _resume_preview(card, inset_x, top_y, avail_w)
    elif kind == "자기소개서":
        body = _cover_preview(card, inset_x, top_y, avail_w)
    else:  # 포트폴리오 (and any unrecognized kind)
        body = _portfolio_preview(card, inset_x, top_y, avail_w, avail_h)
    inner.add(body)

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

    if frame is None:
        frame = BrowserFrame(width=3.7, height=6.0, url="story-arc.org/export")
        frame.move_to([0, 0.25, 0])
        if fades:
            scene.play(*fades, run_time=0.3)
            used += 0.3
        scene.play(FadeIn(frame), run_time=0.3)
        used += 0.3
    else:
        # Swap the URL to the export deep link as the analyze view exits.
        new_url = frame.make_url_text("story-arc.org/export")
        url_anim = Transform(frame.url_text, new_url)
        if fades:
            scene.play(*fades, url_anim, run_time=0.35)
            used += 0.35
        else:
            scene.play(url_anim, run_time=0.3)
            used += 0.3

    # Tab strip — give it a small breathing room above the preview card.
    body_w_for_tabs, _ = frame.body_size()
    tabs = VGroup()
    for i, name in enumerate(content.EXPORT_TABS):
        tabs.add(_make_tab(name, active=(i == 0)))
    tabs.arrange(RIGHT, buff=0.12)
    fit_to_width(tabs, body_w_for_tabs - 0.3)
    tabs.move_to([
        frame.outer.get_center()[0],
        frame.body_top_left()[1] - 0.42,
        0,
    ])

    body_w, body_h = frame.body_size()
    tabs_bottom_y = tabs.get_bottom()[1]
    preview_top_y = tabs_bottom_y - 0.30
    preview_bottom_y = frame.body_top_left()[1] - body_h + 0.35
    preview_h = max(2.4, preview_top_y - preview_bottom_y)
    preview_w = body_w - 0.4
    preview_y = preview_top_y - preview_h / 2

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
    underline = caption_underline(caption)

    scene.play(
        FadeIn(tabs, shift=UP * 0.1),
        FadeIn(preview, shift=UP * 0.1),
        FadeIn(caption, shift=UP * 0.15),
        Create(underline),
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
    setattr(scene, "_use_caption", VGroup(caption, underline))

    if duration > used:
        scene.wait(duration - used)
