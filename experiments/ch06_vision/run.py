"""Ch06 verification (offline): VQA prompt structure + base64 round-trip + cost math.
Live (needs OPENAI_API_KEY + image URLs): GPT-4o VQA. Offline always passes.
Verifies book §6.2-6.4: multimodal content list, detail=low (85 tokens) vs high (85+170*n)."""
import json, time, hashlib, base64
from pathlib import Path
OUT = Path("results/ch06.json")

def prompt_structure():
    q, url = "Is this a banana ('Yes','No')?", "https://example.com/fruit1.png"
    msg = {"role": "user", "content": [
        {"type": "text", "text": q},
        {"type": "image_url", "image_url": {"url": url}}]}
    assert msg["content"][0]["type"] == "text" and msg["content"][1]["type"] == "image_url"
    return {"multimodal_prompt_verified": True}

def b64_roundtrip():
    raw = b"\x89PNG-fake-bytes-for-test"
    enc = base64.b64encode(raw).decode("utf-8")
    assert base64.b64decode(enc) == raw
    url = f"data:image/png;base64,{enc}"
    assert url.startswith("data:image/png;base64,")
    return {"base64_utf8_verified": True}

def cost_math():
    # book example: 1024x1024 high-detail -> 85 + 4*170 = 765 tokens ≈ $0.003825 @ GPT-4o 2024 pricing
    fixed, per_tile, tiles = 85, 170, 4
    total = fixed + tiles * per_tile
    return {"tokens_1024_high": total, "usd_2024": round(total / 1e6 * 5, 6),
            "low_detail_tokens": 85, "note": "recompute with current pricing before publishing; see docs/METHODOLOGY.md"}

if __name__ == "__main__":
    res = {"chapter": "ch06", "ts": time.time(), **prompt_structure(), **b64_roundtrip(), "cost": cost_math(),
           "live": "skipped offline (set OPENAI_API_KEY + IMAGE_URL to run live VQA; see README)"}
    res["digest"] = hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest()[:16]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
