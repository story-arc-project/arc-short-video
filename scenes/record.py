"""Beat 3 — Record (4.5–9.0s).

Browser chrome appears, category tabs slide in, three experience cards
stack from top to bottom, ending with the dashed "+ 새 경험 기록하기" CTA.
"""
from __future__ import annotations

from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LaggedStart,
    LEFT,
    RIGHT,
    Rectangle,
    RoundedRectangle,
    Scene,
    Text,
    UP,
    VGroup,
    Write,
)

from components.badge import Badge
from components.browser_chrome import BrowserFrame
from components.card import RichExperienceCard
from components.decor import caption_underline
from components.fonts import body_font, fit_to_width, heading_font
from config import content, theme, timing


def _dashed_cta(text: str, width: float, height: float = 0.52) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=height,
        fill_color=theme.BRAND_LIGHT,
        fill_opacity=0.5,
        stroke_color=theme.BRAND,
        stroke_width=1.6,
    )
    label = Text(
        text,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.BRAND_DARK,
        font_size=14,
    )
    label.move_to(box.get_center())
    return VGroup(box, label)


def play(scene: Scene) -> None:
    duration = timing.duration(timing.RECORD)

    # Drop the residual logo from the previous beat.
    wordmark = getattr(scene, "_logo_wordmark", None)
    tagline = getattr(scene, "_logo_tagline", None)
    drop = []
    if wordmark is not None:
        drop.append(FadeOut(wordmark, scale=0.85))
    if tagline is not None:
        drop.append(FadeOut(tagline, shift=DOWN * 0.15))

    frame = BrowserFrame(width=3.7, height=6.0, url="story-arc.org/archive")
    frame.move_to([0, 0.25, 0])

    # Category tab chips inside the frame header area. We size tabs to fit
    # within the frame body width so none clip past the rounded edge.
    body_w, _ = frame.body_size()
    tabs = VGroup()
    for i, name in enumerate(content.RECORD_HEADER_TABS):
        variant = "brand" if i == 1 else "gray"
        tabs.add(Badge(name, variant=variant, font_size=12,
                       h_padding=0.10, v_padding=0.05))
    tabs.arrange(RIGHT, buff=0.06)
    if tabs.width > body_w - 0.4:
        tabs.scale((body_w - 0.4) / tabs.width)
    body_top_y = frame.body_top_left()[1]
    # Anchor by the strip's actual top edge so the row never clips above the
    # browser body, regardless of font metrics or future copy changes.
    tab_center_y = body_top_y - tabs.height / 2 - 0.06
    tabs.move_to([
        frame.outer.get_center()[0],
        tab_center_y,
        0,
    ])

    # Three experience cards — rich 4-row layout matching actual app.
    cards = VGroup()
    for category, title, summary, tags, date in content.RECORD_ITEMS:
        cards.add(
            RichExperienceCard(
                category=category,
                title=title,
                summary=summary,
                tags=tags,
                date=date,
                width=3.3,
                height=1.15,
            )
        )
    cards.arrange(DOWN, buff=0.16)
    tabs_bottom_y = tabs.get_bottom()[1]
    stack_top_y = tabs_bottom_y - 0.26
    cards.move_to([
        frame.outer.get_center()[0],
        stack_top_y - cards.height / 2,
        0,
    ])

    cta = _dashed_cta(content.RECORD_ADD_BUTTON, width=3.3)
    cta.next_to(cards, DOWN, buff=0.32)

    footer = Text(
        content.RECORD_FOOTER,
        font=body_font(),
        color=theme.GRAY_500,
        font_size=14,
    )
    footer.next_to(cta, DOWN, buff=0.28)

    caption = Text(
        content.RECORD_LINE,
        font=heading_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_950,
        font_size=30,
    )
    fit_to_width(caption, 4.0)
    caption.move_to([0, -3.2, 0])
    underline = caption_underline(caption)

    used = 0.0
    intro_anims = drop + [FadeIn(frame, shift=UP * 0.2)]
    scene.play(*intro_anims, run_time=0.55)
    used += 0.55

    scene.play(FadeIn(tabs, shift=UP * 0.1), run_time=0.4)
    used += 0.4

    scene.play(
        LaggedStart(
            *[FadeIn(c, shift=UP * 0.2) for c in cards],
            lag_ratio=0.35,
            run_time=1.6,
        )
    )
    used += 1.6

    scene.play(
        FadeIn(cta, shift=UP * 0.15),
        FadeIn(footer, shift=UP * 0.1),
        run_time=0.4,
    )
    used += 0.4

    scene.play(
        FadeIn(caption, shift=UP * 0.15),
        Create(underline),
        run_time=0.4,
    )
    used += 0.4

    setattr(scene, "_record_frame", frame)
    setattr(scene, "_record_inside", VGroup(tabs, cards, cta, footer))
    setattr(scene, "_record_caption", VGroup(caption, underline))

    if duration > used:
        scene.wait(duration - used)
