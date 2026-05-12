"""Visual tokens mirrored from arc-frontend.

Edit any value here to restyle the whole video — no scene code changes needed.
"""

# ----- Brand palette ---------------------------------------------------------
BRAND          = "#fb8408"   # Primary orange
BRAND_LIGHT    = "#fff3e6"   # Soft tint used for badge backgrounds
BRAND_DARK     = "#d46a00"   # Badge text / pressed state
GRADIENT_END   = "#ffc940"   # End stop for the orange→yellow gradient

# ----- Toss-style grayscale --------------------------------------------------
GRAY_950       = "#191f28"   # Body / heading text
GRAY_700       = "#4e5968"
GRAY_500       = "#8b95a1"   # Captions
GRAY_200       = "#e5e8eb"   # Borders
GRAY_100       = "#f2f4f6"   # Card chrome / muted surfaces
GRAY_50        = "#f9fafb"   # Page background
WHITE          = "#ffffff"

# ----- Status ----------------------------------------------------------------
SUCCESS        = "#03b26c"
WARNING        = "#fe9800"
ERROR          = "#f04452"
INFO           = "#3182f6"

# ----- Typography ------------------------------------------------------------
# On macOS, Apple SD Gothic Neo is preferred (system font, no install needed).
# On Linux / CI, Pretendard (bundled under fonts/, SIL OFL) is used instead.
# Resolution order: system font → bundled Pretendard → Noto CJK.
import platform as _platform
FONT_HEADING   = "Apple SD Gothic Neo" if _platform.system() == "Darwin" else "Pretendard"
FONT_BODY      = "Apple SD Gothic Neo" if _platform.system() == "Darwin" else "Pretendard"
FONT_FALLBACKS = ("Pretendard", "Noto Sans CJK KR", "Noto Sans KR")

WEIGHT_REGULAR  = "NORMAL"
WEIGHT_SEMIBOLD = "SEMIBOLD"
WEIGHT_BOLD     = "BOLD"

# ----- Geometry --------------------------------------------------------------
# manim works in scene units, not pixels. The vertical scene we render is
# 9 units tall × 5.0625 units wide (1080×1920 at 16:9 aspect via config).
CARD_RADIUS    = 0.18
CARD_BORDER_W  = 1.4
SAFE_MARGIN_X  = 0.45    # horizontal scene-unit margin for any text
SAFE_MARGIN_Y  = 0.65    # top/bottom safe area (mobile UI overlays)
