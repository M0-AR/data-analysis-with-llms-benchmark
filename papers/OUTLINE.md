# PhD-Paper Outline — From Trummer Verification to Novel Contribution

**Working title:** Beyond Single-Turn Accuracy: Reproducible Benchmarking of LLM Data Analysis Across Modalities with Cost-Aware Data Exploration

## 1. Novel angles (hidden patterns → RQs)
- RQ1 Tables-as-Input: does +40% hold for extraction+aggregation jointly? (ch04+ch05 joint)
- RQ2 Exploration dividend: how much does explicit exploration.json lift EX on messy workbooks? (ablate artifact)
- RQ3 Annotation fragility: rank stability under correction on our mini-suite (Spearman).
- RQ4 Modality routing: when does summary-embedding beat direct-embed per query type?
- RQ5 Cost frontier: cheapest config reaching 80% on each modality (Pareto + ITS curve for agents).

## 2. Claim→Artifact map (fill hashes after `verify_all.py`)
| Claim | Artifact | Hash |
|---|---|---|
| Tables beat text/JSON on facts | results/ch05.json | _ |
| Exploration improves EX | results/exploration.json + suite.json | _ |
| Ranks flip under correction | papers/correction_audit.csv | _ |
| 1-shot 80% at 1/60 GPT-4 cost | results/ch09.json | _ |
| WER clean 2-3 / meet 16 | results/ch07.json | _ |

## 3. Live-data checklist (public, downloadable)
- [ ] IMDB sample 500 (HF) → ch04 live accuracy
- [ ] Spider dev 200 + BIRD Mini-Dev 100 → ch05 EX/EM/VES stratified
- [ ] ChartQA 100 + MMMU-dev 50 → ch06
- [ ] LibriSpeech 10 clips → ch07 WER
- [ ] Cost log → ch09 Pareto figure
- [ ] Agent ITS (1..8 turns) → ch10 curve

## 4. Threats & mitigations
Contamination (use LiveSQLBench-style fresh split), judge bias (dual order + human 5%), non-determinism (temp=0, 3 seeds), pricing drift (date-stamp $).

## 5. Target venues
VLDB (text-to-SQL robustness), ACL Findings (multimodal tables), MLSys (cost-aware repro bench). Start as workshop + arXiv with frozen `results/` + Docker tag.
