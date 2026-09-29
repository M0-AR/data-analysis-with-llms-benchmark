# Demo pipeline (verified 2026-07–09 pattern)

## What GitHub renders
- GIF (`![alt](assets/demo.gif)`) autoplays + loops everywhere. Target **5–15s, 600–800px, 10–15fps, 1–5MB, max 10MB**.
- MP4: **only** via drag-drop upload in web editor/issue → hosted player. `<video>`/`<iframe>` are stripped — never commit raw MP4 to repo history.
- YouTube: clickable thumbnail `[![title](https://img.youtube.com/vi/ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=ID)`.

## Record (2-min loop)
```bash
bash scripts/record_demo.sh   # runs suite, captures terminal GIF via ffmpeg/peek, optimizes with gifsicle
# manual fallback: QuickTime/ShareX 15s → ezgif/ffmpeg → gifsicle --colors 128 --scale 0.8
ffmpeg -i demo.mp4 -vf "fps=12,scale=800:-1" -gifflags +transdiff assets/demo.gif
gifsicle -O3 --colors 128 assets/demo.gif -o assets/demo.gif
ls -lh assets/demo.gif  # must be <5MB
```

## Screenshot (Playwright MCP, verified 2026-09-29)
```js
await page.goto('https://github.com/RichardLitt/standard-readme');
await page.screenshot({ path: 'assets/standard-readme-reference.png' });
```
Snapshot (200–400 tok) for interaction, screenshot for visual proof. Saved copy: `assets/standard-readme-reference.png` (276KB).

## Embed order (first screenful)
1. badges → 2. CEO abstract → 3. GIF hero → 4. MP4/YouTube link → 5. features. Alt text doubles as SEO + a11y. Never put secrets in frames; loop cleanly; lead with payoff in 3s.
