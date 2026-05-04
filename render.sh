#!/usr/bin/env bash
# Render the 20-second ARC promo video at 9:16 vertical.
#
#   bash render.sh           # high quality (1080x1920, 60fps) — final output
#   bash render.sh -qm       # medium    (720x1280, 30fps) — quick preview
#   bash render.sh -ql       # low       (540x960, 15fps)  — fastest, drafts
#   bash render.sh -ql -p    # low + open player after render
#
# Manim's built-in quality flags hard-code 16:9 resolutions, so we translate
# them here to vertical equivalents via explicit -r and --frame_rate.
set -euo pipefail
cd "$(dirname "$0")"

MANIM_BIN="manim"
if [[ -x ".venv/bin/manim" ]]; then
  MANIM_BIN=".venv/bin/manim"
fi

quality_args=("-r" "1080,1920" "--frame_rate" "60")  # default: high
forward=()
for arg in "$@"; do
  case "$arg" in
    -ql|--quality=l|--quality=low)
      quality_args=("-r" "540,960" "--frame_rate" "15")
      ;;
    -qm|--quality=m|--quality=medium)
      quality_args=("-r" "720,1280" "--frame_rate" "30")
      ;;
    -qh|--quality=h|--quality=high)
      quality_args=("-r" "1080,1920" "--frame_rate" "60")
      ;;
    -qk|--quality=k|--quality=fourk)
      quality_args=("-r" "2160,3840" "--frame_rate" "60")
      ;;
    *)
      forward+=("$arg")
      ;;
  esac
done

exec "$MANIM_BIN" "${quality_args[@]}" "${forward[@]}" scenes/promo.py ARCPromo
