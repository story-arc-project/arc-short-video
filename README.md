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

The workflow authenticates to Drive with a **service account** — no OAuth
popup, no browser dance, suitable for headless / remote setup. It needs two
GitHub repository secrets:

| Secret | Value |
|---|---|
| `GDRIVE_SERVICE_ACCOUNT_JSON` | The full JSON key file for a Google Cloud service account that has Editor access to the destination Drive folder. |
| `RCLONE_DRIVE_FOLDER_ID`      | The Drive folder ID where renders should land (the part after `/folders/` in the folder's URL). |

### One-time service account setup (~10 min, web only — no OAuth popup)

1. **Go to Google Cloud Console** → https://console.cloud.google.com and sign in
   with the Google account that owns the destination Drive.

2. **Create or select a project.** Top bar → project dropdown → New project.
   Any name (e.g. `arc-promo-video`).

3. **Enable the Drive API** for that project.
   Search bar → "Google Drive API" → Enable.

4. **Create the service account.**
   Sidebar → IAM & Admin → Service Accounts → Create service account.
   - Name: `arc-promo-uploader` (anything works)
   - Skip optional steps (no roles needed — Drive permissions come from
     folder sharing in step 7, not from GCP IAM).
   - Done.

5. **Create a JSON key.** Click the service account → Keys tab → Add key →
   Create new key → JSON → Create. A `*.json` file downloads automatically.
   Open it; you'll see fields like `"client_email"` and `"private_key"`.

6. **Note the service account email.** It looks like
   `arc-promo-uploader@<project-id>.iam.gserviceaccount.com` — visible inside
   the JSON file (`client_email` field) and on the SA list page.

7. **Share the destination Drive folder with that email.** Open Drive in your
   browser, create or pick a folder, right-click → Share, paste the SA email,
   role: **Editor**, send. (Uncheck "Notify people" — the SA isn't a person.)

8. **Grab the folder ID** from the URL while you're there:
   `https://drive.google.com/drive/folders/<THIS_PART>`.

9. **Add the two GitHub Secrets** at
   https://github.com/story-arc-project/arc-short-video/settings/secrets/actions
   → New repository secret:
   - `GDRIVE_SERVICE_ACCOUNT_JSON` = paste the **entire contents** of the
     downloaded JSON file (multiline is fine).
   - `RCLONE_DRIVE_FOLDER_ID`      = the folder ID from step 8.

That's it — the next push runs the workflow and an mp4 named
`ARCPromo-<timestamp>-<commitsha>.mp4` shows up in your Drive folder.

### Triggering manually

You can also trigger a render without pushing: GitHub → Actions tab →
"Render & upload promo video" → Run workflow. There's a quality dropdown
(high / medium / low) for faster previews.

### Caveats of the service-account approach

- **Files are owned by the service account, not by you.** They live inside
  your shared folder and you can view, download, copy, or move them anywhere
  in your Drive. If you ever delete the service account or revoke its
  Editor permission, the files become inaccessible — so avoid both unless
  you've already copied the mp4s elsewhere.
- **Storage doesn't count against your personal Drive quota** — the SA has
  its own free 15 GB pool.
- **No quota-share with Workspace shared drives** unless you put the SA on
  a Shared Drive instead of a regular folder, which is the cleaner long-term
  setup if you have a Workspace.
