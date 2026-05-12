"""All on-screen Korean copy, sample data, and URLs for the promo video.

This is the single editing surface for non-developers. Change a string here
and rerun ``bash render.sh`` — the scenes pick everything up automatically.
"""

# ----- Branding --------------------------------------------------------------
BRAND_NAME = "ARC"
TAGLINE    = "기록한 경험을 AI가 커리어 서사로 바꿔줍니다"
URL        = "story-arc.org"

# ----- Per-beat captions -----------------------------------------------------
HOOK_LINE     = "열심히 살았는데,\n내 경험을 정리하기\n막막하다면?"
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
# (category_badge, title, summary, tags, date) — items appear from top to bottom.
RECORD_HEADER_TABS = ["전체", "인턴십", "공모전", "동아리", "수업"]
RECORD_ITEMS = [
    ("인턴십", "AI 헬스케어 스타트업 PM 인턴",
     "의료 데이터 기반 서비스 기획 및 로드맵 수립",
     ["PM", "헬스케어", "기획"], "2024.07"),
    ("공모전", "2024 캡스톤 디자인 대상",
     "AI 기반 사용자 인터뷰 분석 플랫폼 제작",
     ["수상", "기획", "개발"], "2024.05"),
    ("동아리", "와플스튜디오 21.5기 프론트엔드",
     "React+TypeScript 웹 서비스 구현 및 협업",
     ["개발", "협업", "FE"], "2023.11"),
]
RECORD_ADD_BUTTON = "+ 새 경험 기록하기"
RECORD_FOOTER     = "이번 학기 3개 · 누적 12개"

# ----- Analyze beat: individual experience analysis --------------------------
# Based on actual arc-frontend analysis page structure (개별 분석 결과).
ANALYZE_EXPERIENCE_TITLE = "AI 헬스케어 스타트업 PM 인턴"
ANALYZE_EXPERIENCE_BADGE = "인턴십"
ANALYZE_OVERVIEW = (
    "6개월간 PM으로 서비스 로드맵을 수립하고 기획을 주도한 경험으로,\n"
    "문제 정의와 실행력이 잘 드러납니다."
)
ANALYZE_STRENGTHS_LABEL = "강점"
ANALYZE_ROLES_LABEL     = "적합한 직무"
ANALYZE_STRENGTHS = [
    "문제를 정량적으로 정의하고 개선한 경험",
    "사용자 리서치 기반 의사결정 역량",
    "기획–개발 협업 및 일정 조율 능력",
]
ANALYZE_ROLES = ["PM", "서비스 기획자", "UX 리서처"]
ANALYZE_KEYWORDS_LABEL = "키워드"
ANALYZE_KEYWORDS = [
    ("문제 정의",    92),
    ("의사결정",     85),
    ("기획 리더십",  74),
]

# ----- Use beat: export tabs -------------------------------------------------
EXPORT_TITLE = "내보내기"
EXPORT_TABS  = ["이력서", "자기소개서", "포트폴리오"]
EXPORT_AI_LABEL = "AI 작성됨"

# Resume preview — based on actual app screenshot (레쥬메 에디터 미리보기)
RESUME_NAME         = "김아크"
RESUME_NAME_EN      = "Kim Arc"
RESUME_DOB          = "2002-03-15"
RESUME_EMAIL        = "arc@story-arc.org"
RESUME_INTRO        = (
    "프론트엔드와 PM을 두 축으로 성장해온 학생입니다. "
    "측정 가능한 성과를 만드는 데 집중합니다."
)
RESUME_SCHOOL       = "한양대학교"
RESUME_SCHOOL_DETAIL = "컴퓨터소프트웨어학부 · 학사 · 2021.03 - 2026.02"
RESUME_COMPANY      = "AI 헬스케어 스타트업"
RESUME_COMPANY_DATE = "2024.07 - 2024.12"
RESUME_COMPANY_ROLE = "PM 인턴 · 제품 기획"
RESUME_BULLETS      = [
    "서비스 로드맵 수립 및 기획서 50건+ 작성",
    "사용자 인터뷰 12건 수행, 기능 우선순위 도출",
]
RESUME_PERF         = "주요 기능 전환율 23% 개선"

# Cover letter preview (aspirational — not yet in app)
COVER_SECTION1      = "지원 동기"
COVER_CONTENT1      = (
    "다양한 경험을 통해 문제를 정의하고 해결하는 과정에서\n"
    "사용자 중심의 서비스 개발에 깊이 매력을 느꼈습니다.\n"
    "특히 데이터 기반으로 문제를 정의하고 해결책을\n"
    "도출하는 PM의 역할에 큰 보람을 느꼈습니다."
)
COVER_HIGHLIGHT     = "사용자 인터뷰로 문제를 재정의했습니다."
COVER_SECTION2      = "성장 경험"
COVER_CONTENT2      = (
    "PM 인턴십에서 팀을 이끌며 실제 서비스의 전체 기획\n"
    "과정을 경험한 것이 저의 가장 큰 성장 기반입니다.\n"
    "사용자 인터뷰 12건을 직접 수행하며 문제를 정의하고\n"
    "우선순위를 결정하는 역량을 키울 수 있었습니다."
)

# Portfolio preview
PORTFOLIO_TITLE     = "Selected Works"
PORTFOLIO_CAPTIONS  = ["헬스케어 PM 인턴", "캡스톤 대상", "프론트엔드 동아리", "사용자 리서치"]
