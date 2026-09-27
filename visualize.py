from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_metrics_chart(df: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_path = output_dir / "sys_metrics.png"

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        df["timestamp"],
        df["cpu_percent"],
        marker="o",
        label="CPU (%)",
        color="#d9354f",
    )
    ax.plot(
        df["timestamp"],
        df["ram_percent"],
        marker="s",
        label="RAM (%)",
        color="#0275d8",
    )
    ax.plot(
        df["timestamp"],
        df["disk_percent"],
        marker="^",
        label="Disk (%)",
        color="#5cb85c",
    )

    ax.axhline(y=70, color="orange", linestyle="--", alpha=0.7, label="Warning (70%)")
    ax.axhline(y=85, color="red", linestyle="--", alpha=0.7, label="Critical (85%)")

    ax.set_title("System Resource Utilization Trend", fontsize=14, fontweight="bold")

    ax.set_xlabel("Timestamp", fontsize=10)
    ax.set_ylabel("Usage (%)", fontsize=10)
    ax.set_ylim(0, 105)
    ax.legend(loc="upper right")
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    fig.savefig(chart_path, dpi=150)
    plt.close(fig)

    return chart_path
