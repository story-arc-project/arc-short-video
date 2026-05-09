"""All on-screen Korean copy, sample data, and URLs for the promo video.

This is the single editing surface for non-developers. Change a string here
and rerun ``bash render.sh`` — the scenes pick everything up automatically.
"""

# ----- Branding --------------------------------------------------------------
BRAND_NAME = "ARC"
TAGLINE    = "기록한 경험을 AI가 커리어 서사로 바꿔줍니다"
URL        = "story-arc.org"

# ----- Per-beat captions -----------------------------------------------------
HOOK_LINE     = "열심히 살았는데\n쓸 말이 없다면?"
LOGO_LINE     = TAGLINE
RECORD_LINE   = "인턴·공모전·동아리 경험을 쉽게 기록"
ANALYZE_LINE  = "내 경험에서 강점과 키워드를 추출"
USE_LINE      = "이력서·자소서·포트폴리오로 변환"
OUTRO_LINE    = "지금 내 경험을 기록해보세요"

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
RECORD_FOOTER     = "이번 학기 3개 · 누적 12개"

# ----- Analyze beat: individual experience analysis --------------------------
# The user clicks one experience from the archive; the analyze beat shows the
# AI breakdown for that single experience (강점 / 배운 점 / 추천 키워드).
ANALYZE_TITLE         = "경험 분석"
ANALYZE_EXPERIENCE    = ("인턴십", "AI 헬스케어 스타트업 PM 인턴", "2024.07")
ANALYZE_STRENGTHS_LABEL  = "강점"
ANALYZE_LEARNINGS_LABEL  = "배운 점"
ANALYZE_KEYWORDS_LABEL   = "추천 키워드"
ANALYZE_STRENGTHS     = ["문제 정의", "협업", "실행력"]
ANALYZE_LEARNINGS     = [
    "사용자 인터뷰로 문제를 구체화",
    "데이터 기반으로 우선순위 결정",
]
ANALYZE_RECO_KEYWORDS = ["문제해결", "사용자 리서치", "기획 역량"]

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
EXPORT_TABS  = ["이력서", "자기소개서", "포트폴리오"]
EXPORT_AI_LABEL = "AI 작성됨"

# Mock content shown inside each export preview tab.
RESUME_NAME      = "김아크"
RESUME_SUBTITLE  = "프로덕트 매니저 지망 · 컴퓨터공학과"
RESUME_SECTIONS  = ["경력", "프로젝트", "스킬"]

COVER_TITLE      = "성장 경험"
COVER_HIGHLIGHT  = "사용자 인터뷰로 문제를 재정의했습니다."

PORTFOLIO_TITLE     = "Selected Works"
PORTFOLIO_CAPTIONS  = ["헬스케어 PM 인턴", "캡스톤 대상", "프론트엔드 동아리", "사용자 리서치"]
