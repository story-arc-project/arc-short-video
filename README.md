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
sudo apt-get install -y libpango1.0-dev libcairo2-dev pkg-config ffmpeg fonts-noto-cjk
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

The font helper falls back to Noto Sans CJK KR (the Korean glyph variant
`fonts-noto-cjk` ships with) if Pretendard isn't installed. To use Pretendard
instead, install the OTF files at OS level — the helper picks them up
automatically next render.


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
├── components/
│   ├── fonts.py               # Korean font resolver + width-fit helper
│   ├── badge.py               # pill badge (brand / gray / success variants)
│   ├── card.py                # ExperienceCard = badge + title + date row
│   ├── browser_chrome.py      # macOS window chrome around mockup beats
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
| Analyze | 9.0 – 13.5s  | Keyword analysis chart — seven horizontal bars fill left-to-right with percent counters. |
| Use     | 13.5 – 17.5s | Export tab strip cycles through 이력서 → 자기소개서 → 포트폴리오 → 전자명함, swapping in a mock preview each time. |
| Outro   | 17.5 – 20.0s | ARC wordmark + tagline + `story-arc.org`. |


## Verifying the output

```bash
ffprobe -v error -show_entries stream=width,height,duration -of default=nw=1 \
  media/videos/ARCPromo.mp4
# Expected: width=1080  height=1920  duration ≈ 19.98s (60fps frame rounding)
```


## CI: auto-render and upload to Google Drive

The `.github/workflows/render.yml` action renders the video on every push and
uploads the mp4 to a Google Drive folder you control. It also keeps a copy as
a 30-day GitHub Actions artifact, so even if the Drive upload fails you can
still grab the video from the workflow run page.

The workflow needs two GitHub repository secrets:

| Secret | Value |
|---|---|
| `RCLONE_CONFIG`           | The full text of your `rclone.conf` (after running `rclone config` locally and authorizing Google Drive). |
| `RCLONE_DRIVE_FOLDER_ID`  | The Drive folder ID where renders should land (the part after `/folders/` in the folder's URL). |

### One-time local setup

1. **Install rclone** on your laptop:
   - macOS: `brew install rclone`
   - Linux: `curl https://rclone.org/install.sh | sudo bash`
   - Windows: download from https://rclone.org/downloads/

2. **Create a remote named exactly `gdrive`** (the workflow refers to it by
   that name). Run `rclone config` and follow the prompts:
   ```
   n) New remote                       → n
   name>                                → gdrive
   Storage>                             → drive            (Google Drive)
   client_id>                           → (leave blank)
   client_secret>                       → (leave blank)
   scope>                               → 1                (full access)
   service_account_file>                → (leave blank)
   Edit advanced config?                → n
   Use auto config?                     → y                (opens browser)
   ```
   Authorize the Google account in the browser tab that opens, then back in
   the terminal answer `n` to "Configure this as a Shared Drive?" and `y` to
   keep the configuration.

3. **Copy the rclone config text:**
   ```bash
   cat ~/.config/rclone/rclone.conf      # macOS / Linux
   # or, on Windows:
   type %APPDATA%\rclone\rclone.conf
   ```
   The output looks like:
   ```ini
   [gdrive]
   type = drive
   scope = drive
   token = {"access_token":"...","refresh_token":"...","expiry":"..."}
   team_drive =
   ```
   Copy the entire block.

4. **Pick or create a destination folder in Google Drive** and grab its ID
   from the URL: `https://drive.google.com/drive/folders/<THIS_PART>`.

5. **Add the two secrets** at GitHub → repo → Settings → Secrets and variables
   → Actions → New repository secret:
   - `RCLONE_CONFIG`           = the text from step 3
   - `RCLONE_DRIVE_FOLDER_ID`  = the ID from step 4

That's it — the next push runs the workflow and an mp4 named
`ARCPromo-<timestamp>-<commitsha>.mp4` shows up in your Drive folder.

### Triggering manually

You can also trigger a render without pushing: GitHub → Actions tab →
"Render & upload promo video" → Run workflow. There's a quality dropdown
(high / medium / low) for faster previews.

### If the OAuth token expires

Google's refresh tokens are usually long-lived but can be revoked. If a
workflow run fails at the upload step with a 401/403, just rerun
`rclone config reconnect gdrive:` locally, copy the new `rclone.conf`, and
update the `RCLONE_CONFIG` secret.
