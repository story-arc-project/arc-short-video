"""Pill-shaped badge matching arc-frontend's badge component."""
from __future__ import annotations

from manim import RIGHT, RoundedRectangle, Text, VGroup

from components.fonts import body_font
from config import theme

VARIANTS = {
    "brand":   (theme.BRAND_LIGHT, theme.BRAND_DARK),
    "gray":    (theme.GRAY_100,    theme.GRAY_700),
    "success": ("#e6f7f0",         theme.SUCCESS),
}


class Badge(VGroup):
    def __init__(
        self,
        label: str,
        variant: str = "brand",
        font_size: float = 18,
        h_padding: float = 0.16,
        v_padding: float = 0.07,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        bg_color, fg_color = VARIANTS.get(variant, VARIANTS["brand"])

        text = Text(
            label,
            font=body_font(),
            weight=theme.WEIGHT_SEMIBOLD,
            color=fg_color,
            font_size=font_size,
        )
        pill_height = text.height + v_padding * 2
        pill = RoundedRectangle(
            corner_radius=pill_height / 2,  # true capsule
            width=text.width + h_padding * 2,
            height=pill_height,
            fill_color=bg_color,
            fill_opacity=1.0,
            stroke_width=0,
        )
        text.move_to(pill.get_center())
        self.add(pill, text)
        self.pill = pill
        self.text_mob = text

    def align_left_to(self, x: float):
        shift = x - self.get_left()[0]
        self.shift(RIGHT * shift)
        return self
