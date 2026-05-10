"""Beat 5 — Use / Export (13.2–17.5s).

A horizontal tab strip appears inside the same browser frame. Tabs activate
in sequence, each revealing a mock preview matching the actual app:
  이력서 → 자기소개서 → 포트폴리오.

Resume preview closely mirrors the actual ResumePreview.tsx layout.
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
                font_size=14)
    pad_h, pad_v = 0.14, 0.07
    pill = RoundedRectangle(
        corner_radius=0.10,
        width=text.width + pad_h * 2,
        height=text.height + pad_v * 2,
        fill_color=bg,
        fill_opacity=1.0,
        stroke_width=0,
    )
    text.move_to(pill.get_center())
    return VGroup(pill, text)


def _skeleton_line(width: float, height: float = 0.09,
                   color: str = theme.GRAY_100, opacity: float = 1.0) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=height / 2,
        width=max(0.3, width),
        height=height,
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=0,
    )


def _section_head(label: str, left_x: float, cursor_y: float,
                  font_size: float = 12) -> tuple[Text, float]:
    head = Text(label, font=heading_font(), weight=theme.WEIGHT_SEMIBOLD,
                color=theme.BRAND_DARK, font_size=font_size)
    head.move_to([left_x + head.width / 2, cursor_y - head.height / 2, 0])
    return head, head.get_bottom()[1] - 0.09


def _resume_preview(card: RoundedRectangle, inset_x: float, top_y: float,
                    avail_w: float) -> VGroup:
    """Resume preview matching actual ResumePreview.tsx layout."""
    inner = VGroup()
    left_x = card.get_left()[0] + inset_x

    # ── Name ─────────────────────────────────────────────────────────────────
    name = Text(content.RESUME_NAME, font=heading_font(),
                weight=theme.WEIGHT_BOLD, color=theme.GRAY_950, font_size=20)
    if name.width > avail_w:
        name.scale(avail_w / name.width)
    name.move_to([left_x + name.width / 2, top_y - name.height / 2, 0])
    inner.add(name)

    # ── Name EN + DOB row ─────────────────────────────────────────────────────
    name_en = Text(content.RESUME_NAME_EN, font=body_font(),
                   color=theme.GRAY_500, font_size=10)
    dob = Text(f"생년월일 {content.RESUME_DOB}", font=body_font(),
               color=theme.GRAY_500, font_size=10)
    name_en.move_to([left_x + name_en.width / 2,
                     name.get_bottom()[1] - 0.07 - name_en.height / 2, 0])
    dob.move_to([card.get_right()[0] - inset_x - dob.width / 2,
                 name_en.get_center()[1], 0])
    inner.add(name_en, dob)

    # ── Email ─────────────────────────────────────────────────────────────────
    email = Text(content.RESUME_EMAIL, font=body_font(),
                 color=theme.GRAY_500, font_size=10)
    if email.width > avail_w:
        email.scale(avail_w / email.width)
    email.move_to([left_x + email.width / 2,
                   name_en.get_bottom()[1] - 0.06 - email.height / 2, 0])
    inner.add(email)

    # ── Divider ───────────────────────────────────────────────────────────────
    div = _skeleton_line(avail_w, height=0.03, color=theme.GRAY_200)
    div.move_to([left_x + avail_w / 2,
                 email.get_bottom()[1] - 0.12 - div.height / 2, 0])
    inner.add(div)

    cursor_y = div.get_bottom()[1] - 0.12

    # ── 자기소개 section ──────────────────────────────────────────────────────
    head, cursor_y = _section_head("자기소개", left_x, cursor_y)
    inner.add(head)
    for w in [avail_w - 0.05, avail_w - 0.25]:
        ln = _skeleton_line(w)
        ln.move_to([left_x + ln.width / 2, cursor_y - ln.height / 2, 0])
        inner.add(ln)
        cursor_y = ln.get_bottom()[1] - 0.08
    cursor_y -= 0.06

    # ── 학력 section ──────────────────────────────────────────────────────────
    head, cursor_y = _section_head("학력", left_x, cursor_y)
    inner.add(head)

    school = Text(content.RESUME_SCHOOL, font=heading_font(),
                  weight=theme.WEIGHT_SEMIBOLD, color=theme.GRAY_950, font_size=11)
    school_date = Text("2021.03 – 2026.02", font=body_font(),
                       color=theme.GRAY_500, font_size=10)
    school.move_to([left_x + school.width / 2, cursor_y - school.height / 2, 0])
    school_date.move_to([card.get_right()[0] - inset_x - school_date.width / 2,
                         cursor_y - school_date.height / 2, 0])
    inner.add(school, school_date)
    cursor_y = school.get_bottom()[1] - 0.06

    detail = Text("컴퓨터소프트웨어학부 · 학사", font=body_font(),
                  color=theme.GRAY_500, font_size=10)
    if detail.width > avail_w:
        detail.scale(avail_w / detail.width)
    detail.move_to([left_x + detail.width / 2, cursor_y - detail.height / 2, 0])
    inner.add(detail)
    cursor_y = detail.get_bottom()[1] - 0.12

    # ── 경력 section ──────────────────────────────────────────────────────────
    head, cursor_y = _section_head("경력", left_x, cursor_y)
    inner.add(head)

    company = Text(content.RESUME_COMPANY, font=heading_font(),
                   weight=theme.WEIGHT_SEMIBOLD, color=theme.GRAY_950, font_size=11)
    comp_date = Text(content.RESUME_COMPANY_DATE, font=body_font(),
                     color=theme.GRAY_500, font_size=10)
    if company.width + comp_date.width + 0.1 > avail_w:
        company.scale((avail_w * 0.6) / company.width)
    company.move_to([left_x + company.width / 2, cursor_y - company.height / 2, 0])
    comp_date.move_to([card.get_right()[0] - inset_x - comp_date.width / 2,
                       cursor_y - comp_date.height / 2, 0])
    inner.add(company, comp_date)
    cursor_y = company.get_bottom()[1] - 0.05

    role = Text(content.RESUME_COMPANY_ROLE, font=body_font(),
                color=theme.GRAY_500, font_size=10)
    if role.width > avail_w:
        role.scale(avail_w / role.width)
    role.move_to([left_x + role.width / 2, cursor_y - role.height / 2, 0])
    inner.add(role)
    cursor_y = role.get_bottom()[1] - 0.08

    for bullet_text in content.RESUME_BULLETS:
        dot = Text("•", font=body_font(), color=theme.BRAND, font_size=10)
        btext = Text(bullet_text, font=body_font(), color=theme.GRAY_700, font_size=10)
        btext_max = avail_w - dot.width - 0.08
        if btext.width > btext_max:
            btext.scale(btext_max / btext.width)
        dot.move_to([left_x + dot.width / 2, cursor_y - dot.height / 2, 0])
        btext.move_to([left_x + dot.width + 0.08 + btext.width / 2,
                       cursor_y - btext.height / 2, 0])
        inner.add(dot, btext)
        cursor_y = btext.get_bottom()[1] - 0.07

    return inner


def _cover_preview(card: RoundedRectangle, inset_x: float, top_y: float,
                   avail_w: float) -> VGroup:
    """Cover letter preview with two named sections."""
    inner = VGroup()
    left_x = card.get_left()[0] + inset_x
    cursor_y = top_y

    # Section 1: 지원 동기
    head, cursor_y = _section_head(content.COVER_SECTION1, left_x, cursor_y, font_size=13)
    inner.add(head)
    for w in [avail_w - 0.05, avail_w - 0.18]:
        ln = _skeleton_line(w)
        ln.move_to([left_x + ln.width / 2, cursor_y - ln.height / 2, 0])
        inner.add(ln)
        cursor_y = ln.get_bottom()[1] - 0.09

    # Highlight sentence
    hl_text = Text(content.COVER_HIGHLIGHT, font=body_font(),
                   weight=theme.WEIGHT_SEMIBOLD, color=theme.BRAND_DARK, font_size=11)
    if hl_text.width > avail_w:
        hl_text.scale(avail_w / hl_text.width)
    hl_bg = RoundedRectangle(
        corner_radius=0.07,
        width=hl_text.width + 0.16,
        height=hl_text.height + 0.12,
        fill_color=theme.BRAND_LIGHT,
        fill_opacity=1.0,
        stroke_width=0,
    )
    cursor_y -= 0.06
    hl_bg.move_to([left_x + hl_bg.width / 2, cursor_y - hl_bg.height / 2, 0])
    hl_text.move_to(hl_bg.get_center())
    inner.add(hl_bg, hl_text)
    cursor_y = hl_bg.get_bottom()[1] - 0.10

    ln = _skeleton_line(avail_w - 0.30)
    ln.move_to([left_x + ln.width / 2, cursor_y - ln.height / 2, 0])
    inner.add(ln)
    cursor_y = ln.get_bottom()[1] - 0.16

    # Section 2: 성장 경험
    head2, cursor_y = _section_head(content.COVER_SECTION2, left_x, cursor_y, font_size=13)
    inner.add(head2)
    for w in [avail_w - 0.08, avail_w - 0.22]:
        ln = _skeleton_line(w)
        ln.move_to([left_x + ln.width / 2, cursor_y - ln.height / 2, 0])
        inner.add(ln)
        cursor_y = ln.get_bottom()[1] - 0.09

    return inner


def _portfolio_preview(card: RoundedRectangle, inset_x: float, top_y: float,
                       avail_w: float, avail_h: float) -> VGroup:
    inner = VGroup()
    left_x = card.get_left()[0] + inset_x

    title = Text(content.PORTFOLIO_TITLE, font=heading_font(),
                 weight=theme.WEIGHT_BOLD, color=theme.GRAY_950, font_size=16)
    if title.width > avail_w:
        title.scale(avail_w / title.width)
    title.move_to([left_x + title.width / 2, top_y - title.height / 2, 0])
    inner.add(title)

    grid_top_y = title.get_bottom()[1] - 0.18
    cols = 2
    rows = 2
    gap = 0.14
    tile_w = (avail_w - gap * (cols - 1)) / cols
    tile_h = min(0.85, (avail_h - 1.2) / rows - gap)

    captions = list(content.PORTFOLIO_CAPTIONS) + [""] * (rows * cols)
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            cx = left_x + tile_w / 2 + c * (tile_w + gap)
            cy = grid_top_y - tile_h / 2 - r * (tile_h + gap + 0.16)
            tile = RoundedRectangle(
                corner_radius=0.10,
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
                corner_radius=0.04,
                width=tile_w * 0.55,
                height=0.08,
                fill_color=theme.BRAND,
                fill_opacity=0.55,
                stroke_width=0,
            )
            inner_dot.move_to([cx, cy + 0.06, 0])
            inner.add(inner_dot)

            cap_text = captions[idx]
            if cap_text:
                cap = Text(cap_text, font=body_font(),
                           color=theme.GRAY_700, font_size=10)
                if cap.width > tile_w - 0.05:
                    cap.scale((tile_w - 0.05) / cap.width)
                cap.move_to([cx, tile.get_bottom()[1] - 0.08 - cap.height / 2, 0])
                inner.add(cap)
    return inner


def _mock_preview(kind: str, width: float, height: float) -> VGroup:
    """Mock card for each export artefact — resume / cover letter / portfolio."""
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

    type_badge = Badge(kind, variant="brand", font_size=11,
                       h_padding=0.10, v_padding=0.04)
    type_badge.move_to([
        card.get_left()[0] + 0.20 + type_badge.width / 2,
        card.get_top()[1] - 0.20 - type_badge.height / 2,
        0,
    ])
    inner.add(type_badge)

    ai_badge = Badge(content.EXPORT_AI_LABEL, variant="brand", font_size=11,
                     h_padding=0.10, v_padding=0.04)
    ai_badge.move_to([
        card.get_right()[0] - 0.20 - ai_badge.width / 2,
        card.get_top()[1] - 0.20 - ai_badge.height / 2,
        0,
    ])
    inner.add(ai_badge)

    inset_x = 0.22
    top_y = type_badge.get_bottom()[1] - 0.18
    avail_w = width - inset_x * 2
    avail_h = top_y - card.get_bottom()[1] - 0.18

    if kind == "이력서":
        body = _resume_preview(card, inset_x, top_y, avail_w)
    elif kind == "자기소개서":
        body = _cover_preview(card, inset_x, top_y, avail_w)
    else:
        body = _portfolio_preview(card, inset_x, top_y, avail_w, avail_h)
    inner.add(body)

    return VGroup(card, inner)


def play(scene: Scene) -> None:
    duration = timing.duration(timing.USE)

    frame: BrowserFrame | None = getattr(scene, "_analyze_frame", None)
    inside = getattr(scene, "_analyze_inside", None)
    prev_caption = getattr(scene, "_analyze_caption", None)

    used = 0.0
    fades = []
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
        new_url = frame.make_url_text("story-arc.org/export")
        url_anim = Transform(frame.url_text, new_url)
        if fades:
            scene.play(*fades, url_anim, run_time=0.35)
            used += 0.35
        else:
            scene.play(url_anim, run_time=0.3)
            used += 0.3

    body_w_for_tabs, _ = frame.body_size()
    tabs = VGroup()
    for i, name in enumerate(content.EXPORT_TABS):
        tabs.add(_make_tab(name, active=(i == 0)))
    tabs.arrange(RIGHT, buff=0.10)
    fit_to_width(tabs, body_w_for_tabs - 0.3)
    tabs.move_to([
        frame.outer.get_center()[0],
        frame.body_top_left()[1] - 0.38,
        0,
    ])

    body_w, body_h = frame.body_size()
    tabs_bottom_y = tabs.get_bottom()[1]
    preview_top_y = tabs_bottom_y - 0.26
    preview_bottom_y = frame.body_top_left()[1] - body_h + 0.30
    preview_h = max(2.4, preview_top_y - preview_bottom_y)
    preview_w = body_w - 0.36
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
    caption.move_to([0, -3.2, 0])
    underline = caption_underline(caption)

    scene.play(
        FadeIn(tabs, shift=UP * 0.1),
        FadeIn(preview, shift=UP * 0.1),
        FadeIn(caption, shift=UP * 0.15),
        Create(underline),
        run_time=0.5,
    )
    used += 0.5

    remaining = duration - used - 0.05
    cycle_count = len(content.EXPORT_TABS) - 1
    per_tab = max(0.4, remaining / max(1, cycle_count))

    for i in range(1, len(content.EXPORT_TABS)):
        new_tabs = VGroup()
        for j, name in enumerate(content.EXPORT_TABS):
            new_tabs.add(_make_tab(name, active=(j == i)))
        new_tabs.arrange(RIGHT, buff=0.10)
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
