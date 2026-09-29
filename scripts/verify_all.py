"""Run all chapters offline (default) or live. Emits digest per chapter + suite summary.
Usage: python scripts/verify_all.py --offline | --live
Best practice: temp=0, seed-fixed, version-pinned, JSON artifacts with digests (Docker SBX pattern)."""
import subprocess, sys, json, hashlib, time
from pathlib import Path
MODES = {"--offline", "--live"}
CHAPTERS = ["experiments/ch04_text/run.py", "experiments/ch05_sql/run.py",
            "experiments/ch06_vision/run.py", "experiments/ch07_audio/run.py",
            "experiments/ch09_cost/run.py", "experiments/ch10_agents/run.py"]
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in MODES else "--offline"
    results = {"mode": mode, "ts": time.time(), "chapters": {}}
    for ch in CHAPTERS:
        t0 = time.time()
        p = subprocess.run([sys.executable, ch], capture_output=True, text=True, cwd=".")
        results["chapters"][ch] = {"exit": p.returncode, "secs": round(time.time() - t0, 2),
                                   "stdout_tail": p.stdout[-2000:], "stderr_tail": p.stderr[-2000:]}
        print(f"[{ch}] exit={p.returncode} {results['chapters'][ch]['secs']}s")
        if p.returncode != 0:
            print(p.stdout[-3000:]); print(p.stderr[-3000:])
    results["digest"] = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:16]
    Path("results").mkdir(exist_ok=True)
    Path("results/suite.json").write_text(json.dumps(results, indent=2))
    fails = [k for k, v in results["chapters"].items() if v["exit"] != 0]
    print("SUITE_DIGEST", results["digest"], "FAILS", fails)
    sys.exit(1 if fails else 0)
if __name__ == "__main__":
    main()
