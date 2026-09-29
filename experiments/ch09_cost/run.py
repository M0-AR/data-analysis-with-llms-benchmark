"""Ch09 verification: cost×quality Pareto math from book scenario.
10k reviews/day × 100 tok = 1M tok/day = 365M/yr.
GPT-4 $0.06/1k → $21,900/yr. GPT-3.5 $0.0005/1k → $182.5/yr (~120x).
Tuning (logit_bias + max_tokens=1) 60%→70%; +1 sample →80% at ~2x tokens but still ~60x cheaper than GPT-4.
Fine-tune: 6x per-token but shorter prompt (2085 vs 2228 tok/10)."""
import json, time, hashlib
from pathlib import Path
OUT = Path("results/ch09.json")
def pareto():
    tok_yr = 365_000_000
    gpt4 = tok_yr / 1000 * 0.06
    g35 = tok_yr / 1000 * 0.0005
    return {
        "tokens_per_year": tok_yr,
        "gpt4_usd_yr": round(gpt4, 2),
        "gpt35_usd_yr": round(g35, 2),
        "ratio": round(gpt4 / g35, 1),
        "ladder": [
            {"config": "untuned gpt-3.5", "acc": 0.60, "tok_10": 2228},
            {"config": "+logit_bias+max1", "acc": 0.70, "tok_10": 2228},
            {"config": "+1-shot", "acc": 0.80, "tok_10": 4078},
            {"config": "gpt-4 zero-shot tuned", "acc": 0.80, "tok_10": 2228, "cost_mult": 120},
            {"config": "fine-tuned gpt-3.5 short prompt", "acc": 0.70, "tok_10": 2085, "cost_mult": 6},
        ],
        "rule": "always log tokens+latency+$; stratify by difficulty; CoT helps Hard+10.9/Extra-Hard+7.7 only"}
if __name__ == "__main__":
    res = {"chapter": "ch09", "ts": time.time(), **pareto()}
    res["digest"] = hashlib.sha256(json.dumps(res, sort_keys=True).encode()).hexdigest()[:16]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))
