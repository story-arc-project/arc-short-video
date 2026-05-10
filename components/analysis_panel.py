"""Individual-experience analysis panel — based on actual arc-frontend analysis page.

Layout (top to bottom inside the browser body):

    ┌──────────────────────────────────────────┐
    │ AI 헬스케어 스타트업 PM 인턴  [인턴십]     │  ← title + category badge
    ├──────────────────────────────────────────┤
    │ 한눈에 보기                               │  ← section heading
    │ ┌──────────────────────────────────────┐ │
    │ │ 6개월간 PM으로 로드맵을 수립하고...  │ │  ← overview card (gray bg)
    │ └──────────────────────────────────────┘ │
    ├──────────────────────────────────────────┤
    │ 심층 분석                                 │  ← section heading
    │ 강점                                      │
    │ • 문제를 정량적으로 정의하고 개선한 경험  │
    │ • 사용자 리서치 기반 의사결정 역량        │
    │ • 기획–개발 협업 및 일정 조율 능력       │
    │ 적합한 직무                               │
    │ [PM] [서비스 기획자] [UX 리서처]         │
    └──────────────────────────────────────────┘

Each major section is a public attribute (``header``, ``overview``,
``deep``) so the scene can stagger their reveal with LaggedStart.
"""
from __future__ import annotations

from manim import DOWN, Dot, LEFT, RIGHT, RoundedRectangle, Text, VGroup

from components.badge import Badge
from components.fonts import body_font, fit_to_width, heading_font
from config import theme


def _section_heading(label: str, font_size: float = 16) -> Text:
    return Text(
        label,
        font=heading_font(),
        weight=theme.WEIGHT_BOLD,
        color=theme.GRAY_950,
        font_size=font_size,
    )


def _subsection_label(label: str, font_size: float = 14) -> Text:
    return Text(
        label,
        font=heading_font(),
        weight=theme.WEIGHT_SEMIBOLD,
        color=theme.GRAY_700,
        font_size=font_size,
    )


def _bullet_line(text: str, font_size: float, max_width: float) -> VGroup:
    dot = Dot(radius=0.04, color=theme.BRAND)
    label = Text(text, font=body_font(), color=theme.GRAY_700, font_size=font_size)
    label_max = max_width - dot.width - 0.14
    if label.width > label_max:
        label.scale(label_max / label.width)
    label.next_to(dot, RIGHT, buff=0.12)
    return VGroup(dot, label)


def _chip_row(labels: list[str], font_size: float, max_width: float) -> VGroup:
    chips = VGroup(*[Badge(l, variant="gray", font_size=font_size,
                           h_padding=0.10, v_padding=0.04) for l in labels])
    chips.arrange(RIGHT, buff=0.10)
    if chips.width > max_width:
        chips.scale(max_width / chips.width)
    return chips


class AnalysisPanel(VGroup):
    """Single-experience AI analysis panel matching the actual analysis result page."""

    def __init__(
        self,
        experience_title: str,
        experience_badge: str,
        overview: str,
        strengths: list[str],
        roles: list[str],
        strengths_label: str = "강점",
        roles_label: str = "적합한 직무",
        width: float = 3.3,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        # ── Header: title text + category badge ──────────────────────────────
        title_mob = Text(
            experience_title,
            font=heading_font(),
            weight=theme.WEIGHT_BOLD,
            color=theme.GRAY_950,
            font_size=14,
        )
        cat_badge = Badge(experience_badge, variant="brand", font_size=11,
                          h_padding=0.10, v_padding=0.04)
        header_row = VGroup(title_mob, cat_badge).arrange(RIGHT, buff=0.12)
        if header_row.width > width:
            header_row.scale(width / header_row.width)
        self.header = header_row

        # ── Section 1: 한눈에 보기 (overview card) ───────────────────────────
        overview_heading = _section_heading("한눈에 보기")

        # Overview text inside a light-gray rounded card
        overview_text = Text(
            overview,
            font=body_font(),
            color=theme.GRAY_700,
            font_size=12,
        )
        if overview_text.width > width - 0.28:
            overview_text.scale((width - 0.28) / overview_text.width)

        overview_card = RoundedRectangle(
            corner_radius=0.10,
            width=width,
            height=overview_text.height + 0.26,
            fill_color=theme.GRAY_100,
            fill_opacity=1.0,
            stroke_width=0,
        )
        overview_text.move_to(overview_card.get_center())

        self.overview = VGroup(
            overview_heading,
            VGroup(overview_card, overview_text),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

        # ── Section 2: 심층 분석 (strengths + roles) ─────────────────────────
        deep_heading = _section_heading("심층 분석")

        strengths_label_mob = _subsection_label(strengths_label)
        bullets = VGroup(*[
            _bullet_line(s, font_size=12, max_width=width)
            for s in strengths
        ]).arrange(DOWN, buff=0.09, aligned_edge=LEFT)
        strengths_block = VGroup(strengths_label_mob, bullets).arrange(
            DOWN, buff=0.10, aligned_edge=LEFT
        )

        roles_label_mob = _subsection_label(roles_label)
        roles_chips = _chip_row(roles, font_size=12, max_width=width)
        roles_block = VGroup(roles_label_mob, roles_chips).arrange(
            DOWN, buff=0.10, aligned_edge=LEFT
        )

        self.deep = VGroup(
            deep_heading,
            strengths_block,
            roles_block,
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)

        body = VGroup(self.overview, self.deep).arrange(
            DOWN, buff=0.20, aligned_edge=LEFT
        )
        stack = VGroup(self.header, body).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        fit_to_width(stack, width + 0.05)
        self.add(stack)
        self.stack = stack
