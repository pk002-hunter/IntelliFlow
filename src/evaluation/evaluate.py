"""
Benchmark Evaluation, Statistical Testing, and Visualization Pipeline.
Compares Fixed-Time, Actuated, DQN, and PPO traffic controllers.
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from typing import Dict, Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_metrics(metrics_dir: str = "results/metrics") -> Dict[str, pd.DataFrame]:
    """Loads all existing baseline and RL metrics CSVs."""
    controllers = {
        "Fixed-Time (Webster)": "fixed_time_baseline.csv",
        "Sensor-Actuated": "actuated_baseline.csv",
        "DQN Agent": "dqn_baseline.csv",
        "PPO Agent": "ppo_baseline.csv"
    }
    loaded = {}
    for name, filename in controllers.items():
        filepath = os.path.join(metrics_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            loaded[name] = df
            print(f"Loaded {name}: {len(df)} records from {filepath}")
        else:
            print(f"Notice: {name} metrics not found at {filepath}")
    return loaded


def compute_summary_table(data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Computes comparative aggregate statistics across controllers."""
    summary_rows = []
    baseline_queue = None

    # First pass: determine reference baseline queue
    if "Fixed-Time (Webster)" in data_dict:
        baseline_queue = data_dict["Fixed-Time (Webster)"]["halting_vehicles"].mean()

    for name, df in data_dict.items():
        mean_queue = df["halting_vehicles"].mean()
        max_queue = df["halting_vehicles"].max()
        std_queue = df["halting_vehicles"].std()
        mean_speed = df["mean_speed"].mean()
        
        # Improvement relative to fixed-time baseline
        if baseline_queue and baseline_queue > 0:
            queue_reduc_pct = ((baseline_queue - mean_queue) / baseline_queue) * 100.0
        else:
            queue_reduc_pct = 0.0

        row = {
            "Controller": name,
            "Mean Queue (vehs)": round(mean_queue, 2),
            "Std Queue": round(std_queue, 2),
            "Max Queue (vehs)": int(max_queue),
            "Mean Speed (m/s)": round(mean_speed, 2),
            "Mean Speed (km/h)": round(mean_speed * 3.6, 2),
            "Queue Reduction vs Fixed (%)": f"{queue_reduc_pct:+.1f}%"
        }

        if "waiting_time" in df.columns:
            row["Mean Wait Time (s)"] = round(df["waiting_time"].mean(), 2)
        if "co2_emissions" in df.columns:
            row["Total CO2 (kg)"] = round(df["co2_emissions"].sum() / 1e6, 3)

        summary_rows.append(row)

    return pd.DataFrame(summary_rows)


def run_statistical_tests(data_dict: Dict[str, pd.DataFrame]):
    """Performs Mann-Whitney U test and Welch's t-test for statistical significance (p < 0.05)."""
    if "Fixed-Time (Webster)" not in data_dict:
        return

    fixed_queues = data_dict["Fixed-Time (Webster)"]["halting_vehicles"]
    print("\n" + "=" * 60)
    print("  Statistical Hypothesis Significance Testing (vs Fixed-Time)")
    print("=" * 60)

    for name, df in data_dict.items():
        if name == "Fixed-Time (Webster)":
            continue

        target_queues = df["halting_vehicles"]
        # Mann-Whitney non-parametric test
        u_stat, mw_p = stats.mannwhitneyu(target_queues, fixed_queues, alternative="less")
        # Welch's t-test
        t_stat, tt_p = stats.ttest_ind(target_queues, fixed_queues, equal_var=False)

        sig_mw = "[YES] Statistically Significant (p < 0.05)" if mw_p < 0.05 else "[NO] Not Significant (p >= 0.05)"
        print(f"\n[{name}]")
        print(f"  Mann-Whitney U: {u_stat:.1f} | p-value: {mw_p:.4e} -> {sig_mw}")
        print(f"  Welch's t-stat: {t_stat:.2f} | p-value: {tt_p:.4e}")


def plot_comparisons(data_dict: Dict[str, pd.DataFrame], save_dir: str = "results/plots"):
    """Generates high-resolution comparative figures."""
    os.makedirs(save_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    colors = {
        "Fixed-Time (Webster)": "#d9534f",
        "Sensor-Actuated": "#f0ad4e",
        "DQN Agent": "#0275d8",
        "PPO Agent": "#5cb85c"
    }

    # 1. Queue Length Over Simulation Time
    plt.figure(figsize=(12, 6))
    for name, df in data_dict.items():
        plt.plot(df["step"], df["halting_vehicles"], label=name, color=colors.get(name, None), linewidth=1.8, alpha=0.85)

    plt.title("IntelliFlow - Halting Queue Length Comparison Over Time", fontsize=14, fontweight="bold")
    plt.xlabel("Simulation Time (seconds)", fontsize=12)
    plt.ylabel("Halting Vehicles (Queue Count)", fontsize=12)
    plt.legend(frameon=True, facecolor="white", framealpha=0.9, fontsize=11)
    plt.tight_layout()
    queue_plot_path = os.path.join(save_dir, "queue_comparison.png")
    plt.savefig(queue_plot_path, dpi=300)
    plt.close()
    print(f"Saved: {queue_plot_path}")

    # 2. Mean Speed Over Simulation Time
    plt.figure(figsize=(12, 6))
    for name, df in data_dict.items():
        plt.plot(df["step"], df["mean_speed"] * 3.6, label=name, color=colors.get(name, None), linewidth=1.8, alpha=0.85)

    plt.title("IntelliFlow - Traffic Flow Speed Comparison Over Time", fontsize=14, fontweight="bold")
    plt.xlabel("Simulation Time (seconds)", fontsize=12)
    plt.ylabel("Mean Vehicle Speed (km/h)", fontsize=12)
    plt.legend(frameon=True, facecolor="white", framealpha=0.9, fontsize=11)
    plt.tight_layout()
    speed_plot_path = os.path.join(save_dir, "speed_comparison.png")
    plt.savefig(speed_plot_path, dpi=300)
    plt.close()
    print(f"Saved: {speed_plot_path}")

    # 3. Bar Chart Summary Comparison
    controllers = list(data_dict.keys())
    mean_queues = [data_dict[c]["halting_vehicles"].mean() for c in controllers]
    mean_speeds = [data_dict[c]["mean_speed"].mean() * 3.6 for c in controllers]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    x_indices = np.arange(len(controllers))

    bar1 = ax1.bar(x_indices - bar_width/2, mean_queues, bar_width, label="Mean Queue (vehs)", color="#337ab7", alpha=0.9)
    ax1.set_ylabel("Mean Halting Vehicles (lower is better)", color="#337ab7", fontsize=12)
    ax1.tick_params(axis='y', labelcolor="#337ab7")

    ax2 = ax1.twinx()
    bar2 = ax2.bar(x_indices + bar_width/2, mean_speeds, bar_width, label="Mean Speed (km/h)", color="#5cb85c", alpha=0.9)
    ax2.set_ylabel("Mean Speed km/h (higher is better)", color="#5cb85c", fontsize=12)
    ax2.tick_params(axis='y', labelcolor="#5cb85c")

    plt.title("IntelliFlow - Performance Benchmark Comparison", fontsize=14, fontweight="bold")
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(controllers, rotation=15, ha="right", fontsize=10)
    fig.tight_layout()
    barchart_path = os.path.join(save_dir, "summary_barchart.png")
    plt.savefig(barchart_path, dpi=300)
    plt.close()
    print(f"Saved: {barchart_path}")


def main():
    print("\n--- Running IntelliFlow Benchmark Evaluation ---")
    data_dict = load_metrics("results/metrics")
    if not data_dict:
        print("No metrics files found in results/metrics. Run controllers first.")
        return

    summary_df = compute_summary_table(data_dict)
    print("\n" + "=" * 60)
    print("  Controller Benchmark Summary Table")
    print("=" * 60)
    print(summary_df.to_string(index=False))

    output_csv = "results/metrics/benchmark_comparison.csv"
    summary_df.to_csv(output_csv, index=False)
    print(f"\nBenchmark comparison saved to {output_csv}")

    run_statistical_tests(data_dict)
    plot_comparisons(data_dict, save_dir="results/plots")


if __name__ == "__main__":
    main()
