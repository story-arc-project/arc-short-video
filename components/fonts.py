"""Resolve a usable Korean font on the host system.

manim's ``Text`` mobject delegates rendering to Pango, which silently falls
back to a default font when the requested family isn't installed. We want
predictable typography across macOS (Apple SD Gothic Neo), local Linux, and
GitHub Actions CI, so this module:

1. On import, registers every ``.otf`` / ``.ttf`` shipped under ``fonts/`` with
   manimpango. Pretendard is bundled there as a guaranteed fallback that
   visually mirrors Apple SD Gothic Neo.
2. Resolves the configured family name through ``fc-list`` (system fonts) and
   our ``_REGISTERED_FAMILIES`` set (bundled fonts), preferring the user's
   primary, then Pretendard, then any remaining fallbacks.

``manimpango.register_font`` calls made AFTER a ``Text`` is constructed are
silently ignored, so we run registration at module top level and ensure
``components/__init__.py`` imports this module first.
"""
from __future__ import annotations

import functools
import shutil
import subprocess
from pathlib import Path

import manimpango

from config import theme

_FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

# Map OTF filename stems to the Pango family name the file actually exposes.
# Each Pretendard weight is its own file but they all advertise the same
# family ("Pretendard"); Pango picks the right weight via the ``weight``
# argument on Text(...). We track the registered families in a set so the
# resolver can hand the name to Pango even when fc-list doesn't see it.
_REGISTERED_FAMILIES: set[str] = set()


def _register_bundled_fonts() -> None:
    if not _FONTS_DIR.is_dir():
        return
    for path in sorted(_FONTS_DIR.iterdir()):
        if path.suffix.lower() not in (".otf", ".ttf"):
            continue
        try:
            manimpango.register_font(str(path))
        except Exception:
            # Registration is best-effort: a corrupted bundled file should not
            # crash rendering. The fallback chain still yields a readable
            # Korean glyph.
            continue
        # Filename stem like "Pretendard-SemiBold" → family "Pretendard".
        family = path.stem.split("-", 1)[0]
        _REGISTERED_FAMILIES.add(family)


_register_bundled_fonts()


@functools.lru_cache(maxsize=1)
def _installed_families() -> frozenset[str]:
    if shutil.which("fc-list") is None:
        return frozenset()
    try:
        out = subprocess.check_output(
            ["fc-list", ":lang=ko", "family"], text=True, timeout=5,
        )
    except (subprocess.SubprocessError, OSError):
        return frozenset()
    families: set[str] = set()
    for line in out.splitlines():
        for name in line.split(","):
            name = name.strip()
            if name:
                families.add(name)
    return frozenset(families)


@functools.lru_cache(maxsize=1)
def heading_font() -> str:
    """Return the best-available font name for Korean headings."""
    return _resolve(theme.FONT_HEADING)


@functools.lru_cache(maxsize=1)
def body_font() -> str:
    """Return the best-available font name for Korean body text."""
    return _resolve(theme.FONT_BODY)


def fit_to_width(mob, max_width: float):
    """Scale `mob` down (only) so its width <= max_width. Returns the mob."""
    if mob.width > max_width:
        mob.scale(max_width / mob.width)
    return mob


def _resolve(preferred: str) -> str:
    families = _installed_families()
    for candidate in (preferred, *theme.FONT_FALLBACKS):
        # Bundled fonts are guaranteed available even when fc-list lags
        # behind the runtime registration.
        if candidate in _REGISTERED_FAMILIES:
            return candidate
        if candidate in families:
            return candidate
        # fc-list reports both "Noto Sans CJK KR" and language-tagged variants;
        # accept any family that case-insensitively contains the candidate.
        for fam in families:
            if candidate.lower() in fam.lower():
                return fam
    # As a last resort, hand the preferred name to Pango and let it fall back.
    return preferred
