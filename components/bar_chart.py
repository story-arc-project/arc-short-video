"""Horizontal bar chart for the analyze beat.

Layout per row, all centered around the chart's local origin:

    [keyword label]    [bar track that fills L→R]    [N%]

A single ValueTracker drives every bar, so the entire chart fills with one
``self.play(progress.animate.set_value(1))`` call. We compute each row's
absolute y position up front and bake it into the always_redraw closures —
``VGroup.arrange()`` doesn't reposition always-redraw mobjects, since their
points are reconstructed every frame.

We deliberately avoid ``DecimalNumber`` because it routes through LaTeX,
which we don't ship as a dependency.
"""
from __future__ import annotations

from manim import (
    RoundedRectangle,
    VGroup,
    ValueTracker,
    always_redraw,
)

from components.fonts import KText, body_font
from config import theme


class KeywordBars(VGroup):
    def __init__(
        self,
        items: list[tuple[str, int]],
        width: float = 3.2,
        row_height: float = 0.32,
        row_gap: float = 0.16,
        label_width: float = 1.05,
        percent_width: float = 0.55,
        font_size: float = 18,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.progress = ValueTracker(0.0)

        bar_track_width = width - label_width - percent_width
        max_value = max(v for _, v in items) if items else 100
        n = len(items)

        # Pre-compute each row's center-y so we can bake it into closures.
        total_h = n * row_height + (n - 1) * row_gap
        top_y = total_h / 2 - row_height / 2

        x_label = -width / 2 + 0.05 + label_width / 2 - 0.18
        x_track = -width / 2 + label_width + bar_track_width / 2 - 0.05

        for i, (keyword, value) in enumerate(items):
            cy = top_y - i * (row_height + row_gap)
            target_fraction = value / max_value

            label = KText(
                keyword,
                font=body_font(),
                color=theme.GRAY_950,
                font_size=font_size,
                weight=theme.WEIGHT_SEMIBOLD,
            )
            # Auto-shrink long keywords (e.g. 커뮤니케이션) to fit the label column.
            max_label_w = label_width - 0.05
            if label.width > max_label_w:
                label.scale(max_label_w / label.width)
            label.move_to([x_label, cy, 0])
            self.add(label)

            track = RoundedRectangle(
                corner_radius=row_height * 0.5 / 2,
                width=bar_track_width,
                height=row_height * 0.7,
                fill_color=theme.GRAY_100,
                fill_opacity=1.0,
                stroke_width=0,
            )
            track.move_to([x_track, cy, 0])
            self.add(track)
            self.add(self._make_fill(track, target_fraction, self.progress))

            self.add(self._make_percent(value, self.progress, track, 0.08, font_size))

    @staticmethod
    def _make_fill(track: RoundedRectangle, target_fraction: float, tracker: ValueTracker):
        track_h = track.height   # invariant under translation — safe to bake
        track_w = track.width

        def builder():
            track_left_x = track.get_left()[0]   # live: follows VGroup.move_to()
            track_y = track.get_center()[1]       # live
            f = tracker.get_value() * target_fraction
            if f < 0.005:
                stub = RoundedRectangle(
                    corner_radius=0, width=0.001, height=0.001,
                    fill_opacity=0, stroke_width=0,
                )
                stub.move_to([track_left_x, track_y, 0])
                return stub
            w = max(track_h, track_w * f)
            bar = RoundedRectangle(
                corner_radius=track_h / 2,
                width=w,
                height=track_h,
                fill_color=theme.BRAND,
                fill_opacity=1.0,
                stroke_width=0,
            )
            bar.move_to([track_left_x + w / 2, track_y, 0])
            return bar
        return always_redraw(builder)

    @staticmethod
    def _make_percent(value: int, tracker: ValueTracker, track: RoundedRectangle,
                      right_gap: float, font_size: float):
        def builder():
            v = round(tracker.get_value() * value)
            label = KText(
                f"{v}%",
                font=body_font(),
                weight=theme.WEIGHT_SEMIBOLD,
                color=theme.GRAY_700,
                font_size=font_size - 1,
            )
            x = track.get_right()[0] + right_gap + label.width / 2   # live
            y = track.get_center()[1]                                  # live
            label.move_to([x, y, 0])
            return label
        return always_redraw(builder)
