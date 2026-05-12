"""Re-usable surfaces matching arc-frontend's card style."""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, RoundedRectangle, VGroup

from components.badge import Badge
from components.fonts import KText, body_font, heading_font
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
        badge_font_size: float = 18,
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

        self.badge = Badge(category, variant="brand", font_size=badge_font_size)
        self.badge.move_to([left_x + self.badge.width / 2, cy, 0])
        self.add(self.badge)

        if date:
            self.date_mob = KText(
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
            self.title_mob = KText(
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


class RichExperienceCard(VGroup):
    """4-row experience card matching the actual arc-frontend ExperienceCard.

    Layout (top to bottom inside a rounded card):
        Row 1: [category badge]  [완료 badge]
        Row 2: title (bold)
        Row 3: summary (gray, 1 line)
        Row 4: [tag1] [tag2] [tag3]              date
    """

    def __init__(
        self,
        category: str,
        title: str,
        summary: str,
        tags: list[str],
        date: str,
        width: float = 3.3,
        height: float = 1.30,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        card = Card(width=width, height=height)
        self.add(card)
        surface = card.surface

        inset_x = 0.16
        left_x = surface.get_left()[0] + inset_x
        right_x = surface.get_right()[0] - inset_x
        avail_w = right_x - left_x
        top_y = surface.get_top()[1] - 0.14

        # Row 1: category + status badges
        cat_badge = Badge(category, variant="brand", font_size=11,
                          h_padding=0.10, v_padding=0.04)
        done_badge = Badge("완료", variant="success", font_size=11,
                           h_padding=0.10, v_padding=0.04)
        badge_row = VGroup(cat_badge, done_badge).arrange(RIGHT, buff=0.08)
        badge_row.move_to([left_x + badge_row.width / 2, top_y - badge_row.height / 2, 0])

        # Row 2: title
        title_mob = KText(title, font=heading_font(), weight=theme.WEIGHT_BOLD,
                         color=theme.GRAY_950, font_size=13)
        if title_mob.width > avail_w:
            title_mob.scale(avail_w / title_mob.width)
        title_y = badge_row.get_bottom()[1] - 0.11 - title_mob.height / 2
        title_mob.move_to([left_x + title_mob.width / 2, title_y, 0])

        # Row 3: summary
        summary_mob = KText(summary, font=body_font(), color=theme.GRAY_500,
                           font_size=11)
        if summary_mob.width > avail_w:
            summary_mob.scale(avail_w / summary_mob.width)
        summary_y = title_mob.get_bottom()[1] - 0.09 - summary_mob.height / 2
        summary_mob.move_to([left_x + summary_mob.width / 2, summary_y, 0])

        # Row 4: tags (left) + date (right)
        tag_chips = VGroup(*[
            Badge(t, variant="gray", font_size=10, h_padding=0.08, v_padding=0.03)
            for t in tags[:3]
        ]).arrange(RIGHT, buff=0.06)

        date_mob = KText(date, font=body_font(), color=theme.GRAY_500, font_size=11)
        bottom_y = surface.get_bottom()[1] + 0.14 + max(tag_chips.height, date_mob.height) / 2
        tag_chips.move_to([left_x + tag_chips.width / 2, bottom_y, 0])
        date_mob.move_to([right_x - date_mob.width / 2, bottom_y, 0])

        self.add(badge_row, title_mob, summary_mob, tag_chips, date_mob)
