# ARC 20-Second Promo Video

A 20-second vertical (9:16, 1080x1920) promotional short for the ARC project,
rendered entirely from Python with [Manim Community Edition][manim-ce] in the
spirit of [3Blue1Brown's][3b1b] code-driven videos.

The whole video — copy, brand colors, beat lengths, sample data — is driven
by three small config files. Edit the config, rerun the render script, ship
the new mp4. No video editor needed.

[manim-ce]: https://docs.manim.community/
[3b1b]: https://github.com/3b1b/manim


## Setup

Requires Python 3.10+, ffmpeg, libcairo, and libpango (Manim's runtime deps).
On Ubuntu/Debian:

```bash
sudo apt-get install -y libpango1.0-dev libcairo2-dev pkg-config ffmpeg
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Korean typography ships with the repo: `fonts/` contains Pretendard
(SIL OFL 1.1) which `components/fonts.py` registers with Pango at import.
On macOS the renderer prefers the system **Apple SD Gothic Neo** (Apple
산돌고딕) automatically and uses bundled Pretendard everywhere else, so
output looks identical across local dev and CI.


## Render

```bash
bash render.sh           # final 1080x1920 @ 60fps  → media/videos/ARCPromo.mp4
bash render.sh -qm       # quick preview 720x1280 @ 30fps
bash render.sh -ql       # fastest draft 540x960 @ 15fps
bash render.sh -ql -p    # draft + auto-open in player
```

Manim's built-in `-ql / -qm / -qh / -qk` flags hard-code 16:9 resolutions, so
`render.sh` translates them to vertical equivalents via explicit `-r` and
`--frame_rate` flags. Pass any other manim flag through and it will be
forwarded.


## What you'll usually edit

| File | What's in it |
|---|---|
| `config/content.py` | **All** Korean copy, sample experiences, keyword names + values, export tabs, URL. Non-developers should only need this file. |
| `config/theme.py`   | Brand colors (`BRAND = #fb8408` matches arc-frontend), gray scale, font names, card geometry. |
| `config/timing.py`  | Per-beat `(start_seconds, duration_seconds)`. The module asserts the six beats sum to exactly `TOTAL = 20.0` at import time, so a typo can't slip through. |

Want a different brand color? Change `theme.BRAND`. Want to retitle the
analyze chart? Change `content.ANALYZE_TITLE`. Want a 25-second cut? Update
`timing.TOTAL` and redistribute the six beats.


## Project layout

```
arc-short-video/
├── render.sh                  # one-line render entrypoint
├── manim.cfg                  # default 1080x1920 @ 60fps, off-white bg
├── requirements.txt
├── config/
│   ├── theme.py               # color + font tokens (mirrored from arc-frontend)
│   ├── content.py             # every on-screen string + sample dataset
│   └── timing.py              # per-beat seconds, validated at import
├── fonts/                     # bundled Pretendard OTFs (SIL OFL fallback)
├── components/
│   ├── fonts.py               # registers bundled fonts + Korean font resolver
│   ├── badge.py               # pill badge (brand / gray / success variants)
│   ├── card.py                # ExperienceCard = badge + title + date row
│   ├── browser_chrome.py      # macOS window chrome around mockup beats
│   ├── analysis_panel.py      # individual experience analysis (header + sections)
│   └── bar_chart.py           # animated horizontal bars + percent counters
└── scenes/
    ├── promo.py               # ARCPromo(Scene) — calls each beat in order
    ├── hook.py                # 0.0–2.5s : scattered fragment cards
    ├── logo.py                # 2.5–4.5s : "ARC" + tagline reveal
    ├── record.py              # 4.5–9.0s : archive screen mockup
    ├── analyze.py             # 9.0–13.5s: keyword analysis chart
    ├── use.py                 # 13.5–17.5s: export-tab mockup cycling
    └── outro.py               # 17.5–20.0s: final ARC + URL hold
```


## 20-second timeline

| Beat | Window | Showcases |
|---|---|---|
| Hook    | 0.0 – 2.5s   | "흩어진 경험들" — six fragment cards drift in. |
| Logo    | 2.5 – 4.5s   | Cards collapse → ARC wordmark + tagline. |
| Record  | 4.5 – 9.0s   | Browser mockup of the archive screen with category chips, three experience cards, and the `+ 새 경험 기록하기` CTA. |
| Analyze | 9.0 – 13.5s  | Individual experience analysis — header card for one experience, then 강점 chips, 배운 점 bullets, and 추천 키워드 chips reveal in sequence. |
| Use     | 13.5 – 17.5s | Export tab strip cycles through 이력서 → 자기소개서 → 포트폴리오 → 전자명함, swapping in a mock preview each time. |
| Outro   | 17.5 – 20.0s | ARC wordmark + tagline + `story-arc.org`. |


## Verifying the output

```bash
ffprobe -v error -show_entries stream=width,height,duration -of default=nw=1 \
  media/videos/ARCPromo.mp4
# Expected: width=1080  height=1920  duration ≈ 19.98s (60fps frame rounding)
```


## CI: auto-render and publish to GitHub Releases

The `.github/workflows/render.yml` action renders the video on every push and
publishes the mp4 to a **rolling GitHub Release** named `latest-render`.
A copy is also kept as a 30-day workflow artifact for short-term recovery.

**No secrets, no third-party setup.** The workflow uses the built-in
`GITHUB_TOKEN`, so you (or anyone with repo read access) can grab the latest
mp4 from one stable URL — no Google Drive, no service accounts, no OAuth.

### Where to download

After the workflow runs, the mp4 lives at:

```
https://github.com/story-arc-project/arc-short-video/releases/tag/latest-render
```

Each push **replaces** that release with a fresh asset named
`ARCPromo-<UTC-timestamp>-<commitsha>.mp4`, so the URL above always points to
the most recent build. Older renders are not retained on the release (use the
30-day workflow artifacts or re-render from history if you need an older
version).

### Triggering manually

GitHub → Actions tab → **"Render & publish promo video"** → Run workflow.
There's a quality dropdown (high / medium / low) for faster previews.

### Why a rolling release instead of one-per-commit?

A new release per push would flood the Releases page during iteration. A
single rolling tag keeps the "latest video" URL stable and clutter-free.
If you want to immortalize a specific version, push a normal git tag — that
won't be touched by this workflow.
