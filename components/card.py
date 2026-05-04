"""Re-usable surfaces matching arc-frontend's card style."""
from __future__ import annotations

from manim import LEFT, RIGHT, RoundedRectangle, Text, VGroup

from components.badge import Badge
from components.fonts import body_font, heading_font
from config import theme


class Card(VGroup):
    """Plain rounded surface with a subtle border."""

    def __init__(
        self,
        width: float,
        height: float,
        fill_color: str = theme.WHITE,
        stroke_color: str = theme.GRAY_200,
        radius: float = theme.CARD_RADIUS,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.surface = RoundedRectangle(
            corner_radius=radius,
            width=width,
            height=height,
            fill_color=fill_color,
            fill_opacity=1.0,
            stroke_color=stroke_color,
            stroke_width=theme.CARD_BORDER_W,
        )
        self.add(self.surface)


class ExperienceCard(VGroup):
    """Badge + title + date row, used in the hook and record beats.

    Layout (single row, left to right):
        [ badge ][  title (gray-950, semibold)  ]            [ date ]
    """

    def __init__(
        self,
        category: str,
        title: str | None = None,
        date: str = "",
        width: float = 3.6,
        height: float = 0.85,
        title_font_size: float = 21,
        date_font_size: float = 17,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.card = Card(width=width, height=height)
        self.surface = self.card.surface
        self.add(self.card)

        inset = 0.20
        left_x = self.surface.get_left()[0] + inset
        right_x = self.surface.get_right()[0] - inset
        cy = self.surface.get_center()[1]

        self.badge = Badge(category, variant="brand", font_size=18)
        self.badge.move_to([left_x + self.badge.width / 2, cy, 0])
        self.add(self.badge)

        if date:
            self.date_mob = Text(
                date,
                font=body_font(),
                color=theme.GRAY_500,
                font_size=date_font_size,
            )
            self.date_mob.move_to([right_x - self.date_mob.width / 2, cy, 0])
            self.add(self.date_mob)
        else:
            self.date_mob = None

        if title:
            title_left = self.badge.get_right()[0] + 0.18
            title_right = (
                self.date_mob.get_left()[0] - 0.18 if self.date_mob else right_x
            )
            available = max(0.5, title_right - title_left)
            self.title_mob = Text(
                title,
                font=heading_font(),
                weight=theme.WEIGHT_SEMIBOLD,
                color=theme.GRAY_950,
                font_size=title_font_size,
            )
            if self.title_mob.width > available:
                self.title_mob.scale(available / self.title_mob.width)
            self.title_mob.move_to([title_left + self.title_mob.width / 2, cy, 0])
            self.add(self.title_mob)
        else:
            self.title_mob = None
