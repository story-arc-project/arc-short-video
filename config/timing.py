"""Per-beat (start_time, duration) in seconds. Total must equal TOTAL.

Every scene module reads its duration from here, so retiming the video means
adjusting numbers in this one file. ``assert`` below catches mismatches at
import time so a typo can't silently produce a 22-second video.
"""

# (start_seconds, duration_seconds)
HOOK    = (0.0,  2.5)
LOGO    = (2.5,  2.0)
RECORD  = (4.5,  4.5)
ANALYZE = (9.0,  4.5)
USE     = (13.5, 4.0)
OUTRO   = (17.5, 2.5)

TOTAL = 20.0

BEATS = (HOOK, LOGO, RECORD, ANALYZE, USE, OUTRO)


def _validate() -> None:
    cursor = 0.0
    for start, dur in BEATS:
        assert abs(start - cursor) < 1e-6, (
            f"Beat starting at {start}s does not abut previous end {cursor}s"
        )
        cursor += dur
    assert abs(cursor - TOTAL) < 1e-6, (
        f"Beat durations sum to {cursor}s, expected {TOTAL}s"
    )


_validate()


def duration(beat: tuple[float, float]) -> float:
    return beat[1]
