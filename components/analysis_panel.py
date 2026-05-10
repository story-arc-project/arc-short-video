"""Individual-experience analysis panel for the analyze beat.

Layout (top to bottom inside the browser body):

    ┌──────────────────────────────────────────┐
    │ [인턴십] AI 헬스케어 스타트업 PM 인턴 2024.07 │  ← header (ExperienceCard)
    ├──────────────────────────────────────────┤
    │ 강점                                       │
    │ [기획] [협업] [리더십]                       │
    │                                            │
    │ 배운 점                                    │
    │ • 사용자 인터뷰 12건 수행                    │
    │ • 데이터 기반 의사결정                       │
    │                                            │
    │ 추천 키워드                                  │
    │ [PM] [헬스케어] [스타트업]                    │
    └──────────────────────────────────────────┘

Each section is exposed as a public attribute (``header``, ``strengths``,
``learnings``, ``keywords``) so the scene can stagger their reveal with
``LaggedStart``.
"""
from __future__ import annotations

from manim import DOWN, Dot, LEFT, RIGHT, Text, VGroup

from components.badge import Badge
from components.card import ExperienceCard
from components.fonts import body_font, fit_to_width, heading_font
from config import theme


def _section_heading(label: str, font_size: float = 19) -> Text:
    return Text(
        label,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.GRAY_950,
        font_size=font_size,
    )


def _chip_row(labels: list[str], variant: str, font_size: float, max_width: float) -> VGroup:
    chips = VGroup(*[Badge(l, variant=variant, font_size=font_size) for l in labels])
    chips.arrange(RIGHT, buff=0.12)
    if chips.width > max_width:
        chips.scale(max_width / chips.width)
    return chips


def _bullet_line(text: str, font_size: float, max_width: float) -> VGroup:
    dot = Dot(radius=0.045, color=theme.BRAND)
    label = Text(
        text,
        font=body_font(),
        color=theme.GRAY_700,
        font_size=font_size,
    )
    label_max = max_width - dot.width - 0.16
    if label.width > label_max:
        label.scale(label_max / label.width)
    label.next_to(dot, RIGHT, buff=0.14)
    return VGroup(dot, label)


class AnalysisPanel(VGroup):
    """Single-experience AI analysis panel."""

    def __init__(
        self,
        experience: tuple[str, str, str],
        strengths: list[str],
        learnings: list[str],
        keywords: list[str],
        strengths_label: str = "강점",
        learnings_label: str = "배운 점",
        keywords_label: str = "추천 키워드",
        width: float = 3.3,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        category, title, date = experience

        # 1. Header card — reuse ExperienceCard for visual consistency with
        #    the archive page the user just came from.
        self.header = ExperienceCard(
            category=category,
            title=title,
            date=date,
            width=width,
            height=0.78,
            title_font_size=17,
            date_font_size=14,
        )

        # 2. 강점 section: heading + brand chips.
        self.strengths = VGroup(
            _section_heading(strengths_label),
            _chip_row(strengths, variant="brand", font_size=15, max_width=width),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)

        # 3. 배운 점 section: heading + bullet list.
        learnings_lines = VGroup(
            *[_bullet_line(l, font_size=15, max_width=width) for l in learnings]
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        self.learnings = VGroup(
            _section_heading(learnings_label),
            learnings_lines,
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

        # 4. 추천 키워드 section: heading + gray chips.
        self.keywords = VGroup(
            _section_heading(keywords_label),
            _chip_row(keywords, variant="gray", font_size=15, max_width=width),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)

        body = VGroup(self.strengths, self.learnings, self.keywords).arrange(
            DOWN, buff=0.32, aligned_edge=LEFT,
        )

        stack = VGroup(self.header, body).arrange(DOWN, buff=0.30)
        # Defensive width fit so a longer translation can never overflow.
        fit_to_width(stack, width + 0.05)
        self.add(stack)
        self.stack = stack
