"""All on-screen Korean copy, sample data, and URLs for the promo video.

This is the single editing surface for non-developers. Change a string here
and rerun ``bash render.sh`` — the scenes pick everything up automatically.
"""

# ----- Branding --------------------------------------------------------------
BRAND_NAME = "ARC"
TAGLINE    = "흩어진 경험을 연결해 당신만의 가능성을 그리다"
URL        = "story-arc.org"

# ----- Per-beat captions -----------------------------------------------------
HOOK_LINE     = "흩어진 경험들"
LOGO_LINE     = TAGLINE
RECORD_LINE   = "18개 경험 유형을 가이드라인과 함께"
ANALYZE_LINE  = "AI가 강점·역량·진로를 분석"
USE_LINE      = "레쥬메·포트폴리오로 즉시 변환"
OUTRO_LINE    = TAGLINE

# ----- Hook beat: floating fragment cards ------------------------------------
# (category_label, date_label) — six fragments drift across the screen.
HOOK_CARDS = [
    ("인턴십",   "2024.07"),
    ("공모전",   "2024.05"),
    ("동아리",   "2023.11"),
    ("프로젝트", "2024.03"),
    ("수업",     "2023.09"),
    ("대외활동", "2024.01"),
]

# ----- Record beat: archive screen items -------------------------------------
# (category_badge, title, date) — items appear from top to bottom.
RECORD_HEADER_TABS = ["전체", "인턴십", "공모전", "동아리", "수업"]
RECORD_ITEMS = [
    ("인턴십",   "AI 헬스케어 스타트업 PM 인턴",   "2024.07"),
    ("공모전",   "2024 캡스톤 디자인 대상",         "2024.05"),
    ("동아리",   "와플스튜디오 21.5기 프론트엔드",  "2023.11"),
]
RECORD_ADD_BUTTON = "+ 새 경험 기록하기"

# ----- Analyze beat: individual experience analysis --------------------------
# The user clicks one experience from the archive; the analyze beat shows the
# AI breakdown for that single experience (강점 / 배운 점 / 추천 키워드).
ANALYZE_TITLE         = "경험 분석"
ANALYZE_EXPERIENCE    = ("인턴십", "AI 헬스케어 스타트업 PM 인턴", "2024.07")
ANALYZE_STRENGTHS_LABEL  = "강점"
ANALYZE_LEARNINGS_LABEL  = "배운 점"
ANALYZE_KEYWORDS_LABEL   = "추천 키워드"
ANALYZE_STRENGTHS     = ["기획", "협업", "리더십"]
ANALYZE_LEARNINGS     = [
    "사용자 인터뷰 12건 수행",
    "데이터 기반 의사결정",
]
ANALYZE_RECO_KEYWORDS = ["PM", "헬스케어", "스타트업"]

# Legacy comprehensive keyword chart — no longer wired into any beat, kept for
# possible reuse in a future "전체 분석" panel.
ANALYZE_KEYWORDS = [
    ("기획",          92),
    ("개발",          88),
    ("협업",          85),
    ("커뮤니케이션",  83),
    ("리더십",        80),
    ("분석",          77),
    ("디자인",        71),
]

# ----- Use beat: export tabs -------------------------------------------------
EXPORT_TITLE = "내보내기"
EXPORT_TABS  = ["이력서", "자기소개서", "포트폴리오", "전자명함"]
EXPORT_AI_LABEL = "AI 작성됨"
