# Zero-to-Hero Methodology (2026-2027 voted best practices)

## 0. Principle: no file without verification
Every claim below was verified by ≥2 independent search channels (see SOURCES.md voting table).
Searxng was down (documented); fallback DuckDuckGo-lite + free-search covered it.

## 1. Tables-first for facts (+40.29%)
Source: Talking with Tables (arXiv 2412.17189). Attention analysis: tables focus model.
Rule: for factual retrieval/summation, convert text→table first, keep schema stable under sparsity.
Our test: ch05 compares table vs JSON vs text on same facts; expect table wins + fewest tokens.

## 2. Text-to-SQL: report EX+EM+VES, stratified, dual-scored
Sources: Spider2.0 (21.3%), BIRD-Interact (8.67/17%), annotation-error paper (52.8/62.8%, rank ±9), Agentic-SQL taxonomy.
Rules:
- Metrics: EX primary, EM strict, VES efficiency, difficulty bands (Easy/Med/Hard/Extra).
- Dual score original vs corrected sample (audit 50).
- Log tokens/latency/$ per query (autonomy costs 10x).
- CoT only for Hard+ (Qwen3-8B Hard 70.19→81.09).

## 3. Walk-before-run artifact
Source: 2608.16045. Every DB run emits results/exploration.json {tables, columns, roles, keys, relations, profiling} BEFORE solving. Human checkpoint.

## 4. Multimodal: summary-embedding + docstore
Source: WickedSmartData 2026-08-19 + MMMU/BenchLM. Index summaries, store originals (MultiVectorRetriever). Validate: sum-check, magnitude, re-extract, uncertainty. Export PNG hi-res, verify legend colors first.

## 5. Evaluation: hybrid tier
Source: Zylos 2026, Databricks, llm-eval-hub. Auto metrics → LLM-judge (2 orderings avg, length-norm) → human on flags. LLM-judge 80-90% agreement, 500-5000x cheaper. Version model+prompt+temp=0, Wilson CIs.

## 6. Audio: WER by condition
Source: codesota/vexascribe 2026. Report clean/mixed/meeting separately. Whisper $0.006/min.

## 7. Reproducibility = Docker + digests + CI gates
Source: Docker SBX kit (2026-09-02), r0b0bench, llm-d-benchmark, LLM-Readiness-Harness. YAML eval def, executor abstraction (local vs sbx), JSON artifact {cmd,stdout,stderr,exit,time,digest}. `docker compose up` reproduces suite.json. Claims→artifacts CSV for paper.

## 8. Cost ladder (book Ch.9 verified math)
365M tok/yr: GPT-4 $21,900 vs GPT-3.5 $182.5 (120x). Ladder: untuned 60% → tuned 70% → 1-shot 80% (~2x tok, still 60x cheaper than GPT-4) → fine-tune 70% shorter prompt but 6x/token. Always Pareto-plot acc vs $.
