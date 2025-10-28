#!/usr/bin/env python3
"""
run_demo.py
Runs the APV concept demo and creates figures + results.json
"""
import json, os, sys
from apv_simulation import run_demo_save
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

def main():
    print("Running APV concept demo (simulation)...")
    results = run_demo_save(OUT_DIR / "results.json")
    print("Results saved to results.json")

    # Plot baseline vs APV bar chart (three metrics)
    labels = ["Response Toxicity (lower better)", "Factual Consistency", "Alignment Stability"]
    baseline = results["tables"]["table1"]["baseline"]
    apv = results["tables"]["table1"]["apv"]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, baseline, width, label='Baseline')
    ax.bar(x + width/2, apv, width, label='APV')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha='right')
    ax.set_title("Baseline vs APV (simulated / reproduced from paper)")
    ax.legend()
    plt.tight_layout()
    fig.savefig(FIG_DIR / "baseline_vs_apv.png")
    print("Saved figure:", FIG_DIR / "baseline_vs_apv.png")

    cycles = results["tables"]["table2"]["cycles"]
    gains = results["tables"]["table2"]["avg_immunization_gain_percent"]
    fig2, ax2 = plt.subplots()
    ax2.plot(cycles, gains, marker='o')
    ax2.set_xlabel("Immunization Cycle")
    ax2.set_ylabel("Avg Immunization Gain (%)")
    ax2.set_title("Immunization Gains per Cycle (simulated)")
    ax2.grid(True)
    fig2.savefig(FIG_DIR / "cycle_gains.png")
    print("Saved figure:", FIG_DIR / "cycle_gains.png")

    print("\\nSummary (from results.json):")
    print(json.dumps({
        "baseline": results["baseline"],
        "final_apv": results["final_apv"],
        "relative_gains_percent": results["tables"]["table1"]["relative_gain_percent"]
    }, indent=2))

if __name__ == "__main__":
    main()
