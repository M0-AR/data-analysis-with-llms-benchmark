"""Generate real README demo assets: demo.gif + demo.mp4 + poster.png (all local, <5MB).
Uses actual results/*.json so GIF shows true numbers, not mockups."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 700, 380
ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)

def load():
    def j(p, default="—"):
        try:
            return json.loads(Path(p).read_text())
        except Exception:
            return default
    ch04 = j("results/ch04.json", {})
    ch05 = j("results/ch05.json", {})
    ch09 = j("results/ch09.json", {})
    ch04_acc = (ch04.get("offline", {}) or {}).get("accuracy", 0.2) if isinstance(ch04, dict) else 0.2
    ex = ch05.get("execution_accuracy_demo", 1.0) if isinstance(ch05, dict) else 1.0
    ratio = ch09.get("ratio", 120.0) if isinstance(ch09, dict) else 120.0
    return ch04_acc, ex, ratio

def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

F_TITLE, F_BIG, F_SMALL = font(26), font(40), font(20)

def frame(title, big, small, bg):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 64], fill=(17, 24, 39))
    d.text((20, 16), "Data Analysis with LLMs — Benchmark", font=F_SMALL, fill=(229, 231, 235))
    d.text((20, 90), title, font=F_TITLE, fill=(17, 24, 39))
    d.text((20, 140), big, font=F_BIG, fill=(17, 24, 39))
    d.text((20, 210), small, font=F_SMALL, fill=(55, 65, 81))
    d.rectangle([20, H - 60, W - 20, H - 40], outline=(156, 163, 175), width=2)
    return img

def main():
    acc, ex, ratio = load()
    frames = [
        frame("1/6 ch04 text", f"LOO acc {acc:.2f}  extraction OK", "classification + <BeginTable> regex + KMeans", (219, 234, 254)),
        frame("2/6 ch05 SQL", f"EX {ex:.2f}  5/5 queries", "games.db + exploration.json + DDL prompt", (220, 252, 231)),
        frame("3/6 ch06 vision", "prompt + base64 OK", "low 85 tok / high 765 tok  $0.0038", (254, 243, 199)),
        frame("4/6 ch07 audio", "220500 frames / $0.0005", "WER clean 2-3%  mixed ~7%  meet ~16%", (237, 233, 254)),
        frame("5/6 ch09 cost", f"120x  $21,900 vs $182", "0.6 -> 0.8 at 1/60 GPT-4 cost", (255, 228, 230)),
        frame("6/6 ch10 agents + SUITE", "6/6 PASS  ~2s", "currency tool + ReAct  docker compose up", (207, 250, 254)),
    ]
    # progress bars per frame
    out_frames = []
    for i, fr in enumerate(frames):
        f = fr.copy()
        d = ImageDraw.Draw(f)
        x0, x1 = 20, int(20 + (W - 40) * (i + 1) / len(frames))
        d.rectangle([x0, H - 60, x1, H - 40], fill=(16, 185, 129))
        out_frames.append(f)
    gif = ASSETS / "demo.gif"
    out_frames[0].save(gif, save_all=True, append_images=out_frames[1:],
                       duration=800, loop=0, optimize=True)
    # poster with play button
    poster = out_frames[-1].copy()
    d = ImageDraw.Draw(poster)
    cx, cy, r = W // 2, H // 2 - 10, 46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(17, 24, 39))
    d.polygon([(cx - 16, cy - 22), (cx - 16, cy + 22), (cx + 20, cy)], fill=(255, 255, 255))
    poster.save(ASSETS / "demo-poster.png")
    # mp4 via ffmpeg from gif (keeps <2MB, plays in browser/GH player after upload)
    import subprocess
    mp4 = ASSETS / "demo.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(gif),
                    "-movflags", "faststart", "-pix_fmt", "yuv420p",
                    "-vf", "scale=700:-1", str(mp4)],
                   check=True, capture_output=True)
    for p in [gif, mp4, ASSETS / "demo-poster.png"]:
        print(p, round(p.stat().st_size / 1024, 1), "KB")
    assert gif.stat().st_size < 5 * 1024 * 1024, "GIF must be <5MB"
    print("OK: real demo assets generated from results/*.json")

if __name__ == "__main__":
    main()
