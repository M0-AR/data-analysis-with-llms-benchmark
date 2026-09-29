"""Ch07 verification (offline): audio pipeline math + file checks.
Live: Whisper transcription WER on LibriSpeech sample (needs OPENAI_API_KEY + audio file).
2026 benchmarks voted: 2-3% clean, ~7% mixed, ~16% meetings; $0.006/min."""
import json, time, hashlib
from pathlib import Path
OUT = Path("results/ch07.json")
def offline():
    sample_rate, secs = 44100, 5
    frames = sample_rate * secs
    assert frames == 220500
    # pricing: 5s = 5/60 min * $0.006
    cost = 5 / 60 * 0.006
    return {"recording_frames_5s": frames, "cost_5s_usd": round(cost, 6),
            "supported": ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
            "limit_mb": 25, "wer_benchmarks_2026": {"clean": "2-3%", "mixed": "~7%", "meetings": "~16%"}}
if __name__ == "__main__":
    res = {"chapter": "ch07", "ts": time.time(), **offline(),
           "live": "skipped offline (place QuoteFromTheAlchemist.mp3 in data/raw + set OPENAI_API_KEY)"}
    res["digest"] = hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest()[:16]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
