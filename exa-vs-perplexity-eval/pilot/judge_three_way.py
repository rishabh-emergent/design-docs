#!/usr/bin/env python3
"""
Three-way judge:
  - Perplexity sonar-deep-research
  - Exa /research/v1 (exa-research-pro)
  - Exa /search + Claude Haiku 4.5 synthesis

Reads existing per-playbook scores from judge_results/ where present (incremental);
only sends NEW playbooks (exa_search_haiku) to the judge. Then computes pairwise
winners for all C(3,2) = 3 head-to-head comparisons and a 3-way ranking.
"""
import concurrent.futures as cf
import json
import subprocess
import time
import urllib.request
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from judge import JUDGE_SYSTEM_PROMPT, judge_one_playbook, pairwise_winner

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
JUDGE = ROOT / "judge_results"
JUDGE.mkdir(exist_ok=True)

PROVIDERS = ["exa", "perplexity", "exa_search_haiku", "gemini_31"]
PROVIDER_DISPLAY = {
    "exa": "exa_research",
    "perplexity": "perplexity",
    "exa_search_haiku": "exa_search+haiku",
    "gemini_31": "gemini_3.1+grounding",
}


def load_score(iid, provider):
    """Return judge score dict if cached on disk."""
    fp = JUDGE / f"{iid}-{provider}.json"
    if fp.exists():
        return json.loads(fp.read_text())
    return None


def main():
    # Discover what's missing
    pairs = []
    for f in sorted(RESULTS.glob("I*.json")):
        data = json.loads(f.read_text())
        integ = data["integration"]
        playbooks = {}
        for prov in PROVIDERS:
            block = data.get(prov, {})
            if block.get("ok"):
                playbooks[prov] = block.get("content", "")
        pairs.append({"integration": integ, "playbooks": playbooks})

    # Build judge tasks for any (integration, provider) without a cached score
    judge_tasks = []
    for p in pairs:
        for prov, text in p["playbooks"].items():
            if not load_score(p["integration"]["id"], prov):
                judge_tasks.append((p["integration"], prov, text))

    print(f"Judging {len(judge_tasks)} new playbooks (Shape A absolute, incremental)...")
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {
            ex.submit(judge_one_playbook, t[0], t[1], t[2]): (t[0]["id"], t[1])
            for t in judge_tasks
        }
        for fut in cf.as_completed(futs):
            iid, provider = futs[fut]
            r = fut.result()
            (JUDGE / f"{iid}-{provider}.json").write_text(json.dumps(r, indent=2))
            scores = r.get("scores", {})
            line = (
                f"C&F={scores.get('correctness_and_freshness')} EX={scores.get('executability')} "
                f"CP={scores.get('completeness')} CT={scores.get('citation_anchoring')} "
                f"({r.get('_judge_latency_s',0):.1f}s)"
                if scores else f"ERROR: {r.get('error','?')[:80]}"
            )
            print(f"  {iid}/{provider}: {line}", flush=True)

    # Build complete scores grid
    grid = {}  # grid[iid][provider] = scores dict
    for p in pairs:
        iid = p["integration"]["id"]
        grid[iid] = {"integration": p["integration"]}
        for prov in PROVIDERS:
            j = load_score(iid, prov)
            if j and j.get("scores"):
                grid[iid][prov] = j["scores"]

    # All C(4,2) = 6 pairwise comparisons
    dims = ["correctness_and_freshness", "executability", "completeness", "citation_anchoring"]
    comparisons = [
        ("exa", "perplexity"),
        ("exa_search_haiku", "perplexity"),
        ("gemini_31", "perplexity"),
        ("exa_search_haiku", "exa"),
        ("gemini_31", "exa"),
        ("gemini_31", "exa_search_haiku"),
    ]

    pairwise_results = {f"{a}_vs_{b}": {"wins_A": 0, "wins_B": 0, "TIE": 0, "skipped": 0, "details": []} for a, b in comparisons}

    for iid, row in grid.items():
        for a, b in comparisons:
            key = f"{a}_vs_{b}"
            if a not in row or b not in row:
                pairwise_results[key]["skipped"] += 1
                pairwise_results[key]["details"].append({"integration": iid, "skipped": True})
                continue
            v = pairwise_winner(row[a], row[b])
            if v["winner"] == "A":
                pairwise_results[key]["wins_A"] += 1
                w = a
            elif v["winner"] == "B":
                pairwise_results[key]["wins_B"] += 1
                w = b
            else:
                pairwise_results[key]["TIE"] += 1
                w = "TIE"
            pairwise_results[key]["details"].append({
                "integration": iid,
                "name": row["integration"]["name"],
                "a_scores": row[a],
                "b_scores": row[b],
                "winner": w,
                "verdict": v,
            })

    # Per-dimension averages by provider
    dim_avgs = {prov: {d: [] for d in dims} for prov in PROVIDERS}
    for iid, row in grid.items():
        for prov in PROVIDERS:
            if prov in row:
                for d in dims:
                    dim_avgs[prov][d].append(row[prov][d])
    dim_avg_out = {prov: {d: round(sum(v) / len(v), 2) if v else None for d, v in dims_map.items()}
                   for prov, dims_map in dim_avgs.items()}
    counts = {prov: sum(1 for iid in grid if prov in grid[iid]) for prov in PROVIDERS}

    # Cost summary per provider
    cost_summary = {}
    char_summary = {}
    latency_summary = {}
    for f in sorted(RESULTS.glob("I*.json")):
        data = json.loads(f.read_text())
        exa = data.get("exa", {})
        pplx = data.get("perplexity", {})
        esh = data.get("exa_search_haiku", {})
        gem = data.get("gemini_31", {})
        cost_summary.setdefault("exa", []).append(exa.get("cost_dollars") or 0)
        cost_summary.setdefault("perplexity", []).append(
            (pplx.get("usage", {}) or {}).get("cost", {}).get("total_cost", 0)
        )
        cost_summary.setdefault("exa_search_haiku", []).append(
            (esh.get("cost_breakdown") or {}).get("total_dollars", 0) if esh.get("ok") else 0
        )
        cost_summary.setdefault("gemini_31", []).append(
            (gem.get("cost_breakdown") or {}).get("total_dollars", 0) if gem.get("ok") else 0
        )
        for prov, block in (("exa", exa), ("perplexity", pplx), ("exa_search_haiku", esh), ("gemini_31", gem)):
            if block.get("ok"):
                char_summary.setdefault(prov, []).append(len(block.get("content", "")))
                latency_summary.setdefault(prov, []).append(block.get("latency_s", 0))

    aggregate = {
        "n_integrations_total": len(grid),
        "n_scored_by_provider": counts,
        "dim_averages": dim_avg_out,
        "pairwise": {
            k: {
                "wins_A": v["wins_A"],
                "wins_B": v["wins_B"],
                "TIE": v["TIE"],
                "skipped": v["skipped"],
            } for k, v in pairwise_results.items()
        },
        "totals": {
            prov: {
                "total_cost_dollars": round(sum(cost_summary.get(prov, [])), 2),
                "avg_cost_dollars": round(sum(cost_summary.get(prov, [])) / max(1, len(cost_summary.get(prov, []))), 4),
                "avg_chars": int(sum(char_summary.get(prov, [])) / max(1, len(char_summary.get(prov, [])))),
                "avg_latency_s": round(sum(latency_summary.get(prov, [])) / max(1, len(latency_summary.get(prov, []))), 1),
                "ok_count": len(char_summary.get(prov, [])),
            } for prov in PROVIDERS
        },
        "pairwise_details": pairwise_results,
    }
    (JUDGE / "_aggregate_3way.json").write_text(json.dumps(aggregate, indent=2))

    print("\n=== 3-WAY AGGREGATE ===")
    print(json.dumps({k: aggregate[k] for k in ("n_integrations_total","n_scored_by_provider","dim_averages","pairwise","totals")}, indent=2))


if __name__ == "__main__":
    main()
