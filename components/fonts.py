"""Resolve a usable Korean font on the host system.

manim's ``Text`` mobject delegates rendering to Pango, which silently falls
back to a default font when the requested family isn't installed. We want
predictable typography, so we probe ``fc-list`` once and pick the first font
from the configured preference list that actually exists on the box.
"""
from __future__ import annotations

import functools
import shutil
import subprocess

from config import theme


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
        if candidate in families:
            return candidate
        # fc-list reports both "Noto Sans CJK KR" and language-tagged variants;
        # accept any family that case-insensitively contains the candidate.
        for fam in families:
            if candidate.lower() in fam.lower():
                return fam
    # As a last resort, hand the preferred name to Pango and let it fall back.
    return preferred
