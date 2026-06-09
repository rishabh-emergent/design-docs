#!/usr/bin/env python3
"""
Pilot results summarizer. Reads Stage 1 + judge outputs, emits a human-readable
markdown report + a one-line verdict.

Pilot verdict rule (simplified from main report — Stage 2 not run):
- exa_winrate = #pairs where winner=exa / (#non-skipped pairs)
- pplx_winrate = same for perplexity
- Decision:
    exa_winrate >= 0.60 AND no integration has exa correctness_and_freshness <= 2 → SHIP_EXA_LEAN
    pplx_winrate >= 0.60 AND no integration has pplx correctness_and_freshness <= 2 → STAY_PERPLEXITY_LEAN
    abs(exa_winrate - pplx_winrate) < 0.20 AND TIE rate >= 0.30 → MIXED_RUN_FULL_EVAL
    otherwise → MIXED_RUN_FULL_EVAL (default to caution)
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
JUDGE = ROOT / "judge_results"


def main():
    run_summary = json.loads((RESULTS / "_run_summary.json").read_text())
    agg = json.loads((JUDGE / "_aggregate.json").read_text())

    n_pairs = len(agg["pairs"]) - agg["winner_counts"]["skipped"]
    winners = agg["winner_counts"]
    exa_winrate = winners["exa"] / n_pairs if n_pairs else 0
    pplx_winrate = winners["perplexity"] / n_pairs if n_pairs else 0
    tie_rate = winners["TIE"] / n_pairs if n_pairs else 0

    # Verdict
    any_exa_broken = any(p.get("exa_scores", {}).get("correctness_and_freshness", 5) <= 2
                          for p in agg["pairs"] if not p.get("skipped"))
    any_pplx_broken = any(p.get("pplx_scores", {}).get("correctness_and_freshness", 5) <= 2
                           for p in agg["pairs"] if not p.get("skipped"))
    if exa_winrate >= 0.60 and not any_exa_broken:
        verdict = "SHIP_EXA_LEAN"
    elif pplx_winrate >= 0.60 and not any_pplx_broken:
        verdict = "STAY_PERPLEXITY_LEAN"
    else:
        verdict = "MIXED_RUN_FULL_EVAL"

    out = []
    out.append("# Exa vs Perplexity — Pilot Results")
    out.append("")
    out.append("## TL;DR")
    out.append("")
    out.append(f"- **Verdict: `{verdict}`**")
    out.append(f"- Sample: {n_pairs} integrations (paired Exa + Perplexity playbooks)")
    out.append(f"- Win rates: Exa = **{exa_winrate:.0%}**, Perplexity = **{pplx_winrate:.0%}**, Tie = **{tie_rate:.0%}**")
    out.append(f"- Wall-clock: {run_summary['elapsed_s']:.0f}s ({run_summary['elapsed_s']/60:.1f} min)")
    out.append(f"- Cost: Exa = ${run_summary['by_provider']['exa']['total_cost_dollars']:.2f}, Perplexity ≈ ${0.30 * n_pairs:.2f} (estimated)")
    out.append("")

    out.append("## Stage 1 — Generation stats")
    out.append("")
    out.append("| Provider | OK count | Avg latency (s) | Avg playbook chars |")
    out.append("|---|---|---|---|")
    for prov in ("exa", "perplexity"):
        s = run_summary["by_provider"][prov]
        out.append(f"| {prov} | {s['ok']}/{run_summary['n_integrations']} | {s['avg_latency_s']:.1f} | {int(s['avg_chars'])} |")
    out.append("")

    out.append("## Stage 1 — Judge (Claude Opus 4.7, absolute Shape A)")
    out.append("")
    out.append("### Per-dimension averages (1-5 scale)")
    out.append("")
    out.append("| Dimension | Exa avg | Perplexity avg | Δ (Exa − Pplx) |")
    out.append("|---|---|---|---|")
    for d in ["correctness_and_freshness", "executability", "completeness", "citation_anchoring"]:
        ev = agg["dim_averages"]["exa"][d]
        pv = agg["dim_averages"]["perplexity"][d]
        delta = round(ev - pv, 2) if (ev is not None and pv is not None) else "n/a"
        out.append(f"| {d} | {ev} | {pv} | {delta} |")
    out.append("")

    out.append("### Per-integration pairwise")
    out.append("")
    out.append("| ID | Integration | Exa scores (C&F/EX/CP/CT) | Pplx scores | Winner | Tie rule | Both broken? |")
    out.append("|---|---|---|---|---|---|---|")
    for p in agg["pairs"]:
        if p.get("skipped"):
            out.append(f"| {p['integration']} | (skipped: {p.get('reason','?')}) | — | — | — | — | — |")
            continue
        es = p["exa_scores"]
        ps = p["pplx_scores"]
        es_str = f"{es['correctness_and_freshness']}/{es['executability']}/{es['completeness']}/{es['citation_anchoring']}"
        ps_str = f"{ps['correctness_and_freshness']}/{ps['executability']}/{ps['completeness']}/{ps['citation_anchoring']}"
        out.append(f"| {p['integration']} | {p['name']} | {es_str} | {ps_str} | **{p['winner_provider']}** | {p['verdict']['tie_rule']} | {p['verdict']['both_broken']} |")
    out.append("")

    out.append("## Verdict math")
    out.append("")
    out.append(f"- Exa wins: {winners['exa']}/{n_pairs} = {exa_winrate:.0%}")
    out.append(f"- Perplexity wins: {winners['perplexity']}/{n_pairs} = {pplx_winrate:.0%}")
    out.append(f"- Ties: {winners['TIE']}/{n_pairs} = {tie_rate:.0%}")
    out.append(f"- Any Exa playbook with correctness ≤ 2: {any_exa_broken}")
    out.append(f"- Any Perplexity playbook with correctness ≤ 2: {any_pplx_broken}")
    out.append("")
    out.append("**Decision rule applied:**")
    if verdict == "SHIP_EXA_LEAN":
        out.append("Exa winrate ≥ 60% AND no broken Exa playbooks → lean toward shipping Exa. Run full 28-integration eval to confirm.")
    elif verdict == "STAY_PERPLEXITY_LEAN":
        out.append("Perplexity winrate ≥ 60% AND no broken Perplexity playbooks → lean toward keeping Perplexity. Full eval optional.")
    else:
        out.append("Inconclusive signal at pilot scale → expand to full 28-integration eval before deciding.")
    out.append("")
    out.append("## Pilot caveats")
    out.append("")
    out.append("- Single judge model (Opus 4.7) — full eval should use Opus + GPT-5 ensemble.")
    out.append("- `docs_unavailable=true` — judge applied LONG-TAIL HANDLING (internal-consistency-only scoring) instead of comparing to fetched official docs. Full eval pre-fetches docs per integration.")
    out.append("- No position swap (each playbook judged once absolute, pairwise computed locally). Position bias not measured at pilot scale.")
    out.append("- Stage 2 (end-to-end smoke tests on real APIs) not run. Verdict score formula `0.7*stage2 + 0.3*stage1` not computable; pilot uses stage1 only as directional signal.")
    out.append("")

    report = "\n".join(out)
    (ROOT / "PILOT_REPORT.md").write_text(report)
    print(report)
    print(f"\nWritten to {ROOT / 'PILOT_REPORT.md'}")


if __name__ == "__main__":
    main()
