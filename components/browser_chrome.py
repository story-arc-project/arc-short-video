"""macOS-style window chrome that frames the product mockup beats."""
from __future__ import annotations

from manim import Circle, LEFT, RIGHT, Rectangle, RoundedRectangle, Text, VGroup

from components.fonts import body_font
from config import theme


class BrowserFrame(VGroup):
    """A rounded white card with a chrome header containing 3 traffic-light dots
    and a fake URL bar. Children can be parented inside via :meth:`body_box`."""

    HEADER_HEIGHT = 0.55
    DOT_RADIUS = 0.07

    def __init__(
        self,
        width: float = 3.7,
        height: float = 5.0,
        url: str = "story-arc.org",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        outer = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=height,
            fill_color=theme.WHITE,
            fill_opacity=1.0,
            stroke_color=theme.GRAY_200,
            stroke_width=theme.CARD_BORDER_W,
        )
        self.add(outer)
        self.outer = outer

        header = Rectangle(
            width=width,
            height=self.HEADER_HEIGHT,
            fill_color=theme.GRAY_50,
            fill_opacity=1.0,
            stroke_width=0,
        )
        header.move_to(
            [
                outer.get_center()[0],
                outer.get_top()[1] - self.HEADER_HEIGHT / 2,
                0,
            ]
        )
        self.add(header)
        self.header = header

        # Traffic lights (red / yellow / green)
        dots = VGroup()
        for color in ("#ff5f57", "#febc2e", "#28c840"):
            dot = Circle(
                radius=self.DOT_RADIUS,
                color=color,
                fill_color=color,
                fill_opacity=1.0,
                stroke_width=0,
            )
            dots.add(dot)
        dots.arrange(RIGHT, buff=0.08)
        dots.move_to(
            [
                header.get_left()[0] + 0.22 + dots.width / 2,
                header.get_center()[1],
                0,
            ]
        )
        self.add(dots)

        # Fake URL bar pill
        url_bar_w = width * 0.55
        url_bar = RoundedRectangle(
            corner_radius=0.12,
            width=url_bar_w,
            height=self.HEADER_HEIGHT - 0.18,
            fill_color=theme.WHITE,
            fill_opacity=1.0,
            stroke_color=theme.GRAY_200,
            stroke_width=1.0,
        )
        url_bar.move_to(header.get_center())
        self.add(url_bar)
        url_text = Text(
            url,
            font=body_font(),
            color=theme.GRAY_500,
            font_size=15,
        )
        url_text.move_to(url_bar.get_center())
        self.add(url_text)
        self.url_text = url_text

        self._body_top = header.get_bottom()[1]
        self._body_bottom = outer.get_bottom()[1]
        self._body_left = outer.get_left()[0]
        self._body_right = outer.get_right()[0]

    def body_center(self) -> list[float]:
        return [
            (self._body_left + self._body_right) / 2,
            (self._body_top + self._body_bottom) / 2,
            0.0,
        ]

    def body_size(self) -> tuple[float, float]:
        return (
            self._body_right - self._body_left,
            self._body_top - self._body_bottom,
        )

    def body_top_left(self) -> list[float]:
        return [self._body_left, self._body_top, 0.0]
