"""Small decorative helpers shared across beats."""
from __future__ import annotations

from manim import Arc, PI, RIGHT, RoundedRectangle, Text, VGroup

from config import theme


def feature_label_badge(text: str) -> VGroup:
    """Pill badge with a small flat arc icon + label text (ARC branding style)."""
    from components.fonts import KText, body_font

    arc_icon = Arc(
        radius=0.095,
        start_angle=PI / 2 - theme.LOGO_ARC_START_OFFSET,
        angle=theme.LOGO_ARC_ANGLE,
        stroke_color=theme.BRAND_DARK,
        stroke_width=1.8,
    )
    label = KText(
        text,
        font=body_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.BRAND_DARK,
        font_size=14,
    )
    content = VGroup(arc_icon, label).arrange(RIGHT, buff=0.07)
    h_pad, v_pad = 0.13, 0.07
    pill_h = content.height + v_pad * 2
    pill = RoundedRectangle(
        corner_radius=pill_h / 2,
        width=content.width + h_pad * 2,
        height=pill_h,
        fill_color=theme.WHITE,
        fill_opacity=1.0,
        stroke_color=theme.BRAND,
        stroke_width=1.2,
    )
    content.move_to(pill.get_center())
    return VGroup(pill, content)


def caption_underline(
    caption: Text,
    width_ratio: float = 0.42,
    color: str = theme.BRAND,
    height: float = 0.06,
    gap: float = 0.16,
) -> RoundedRectangle:
    """A short brand-colored bar centered under a caption."""
    bar = RoundedRectangle(
        corner_radius=height / 2,
        width=max(0.6, caption.width * width_ratio),
        height=height,
        fill_color=color,
        fill_opacity=1.0,
        stroke_width=0,
    )
    bar.move_to([
        caption.get_center()[0],
        caption.get_bottom()[1] - gap,
        0,
    ])
    return bar
