import time

import numpy as np
import pandas as pd
import psutil


def capture_snapshot() -> dict[str, float | str]:
    cpu_pct = psutil.cpu_percent(interval=None)
    ram_pct = psutil.virtual_memory().percent
    disk_pct = psutil.disk_usage("/").percent
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": timestamp,
        "cpu_percent": float(cpu_pct),
        "ram_percent": float(ram_pct),
        "disk_percent": float(disk_pct),
    }


def analyze_metrics_vectorized(
    df: pd.DataFrame,
    cpu_warn: float = 70.0,
    cpu_crit: float = 85.0,
    ram_warn: float = 75.0,
    ram_crit: float = 90.0,
) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    result_df = df.copy()

    cpu_conditions = [
        result_df["cpu_percent"] >= cpu_crit,
        result_df["cpu_percent"] >= cpu_warn,
    ]
    cpu_choices = ["CRITICAL", "WARNING"]
    result_df["cpu_status"] = np.select(cpu_conditions, cpu_choices, default="OK")

    ram_conditions = [
        result_df["ram_percent"] >= ram_crit,
        result_df["ram_percent"] >= ram_warn,
    ]
    ram_choices = ["CRITICAL", "WARNING"]
    result_df["ram_status"] = np.select(ram_conditions, ram_choices, default="OK")

    overall_conditions = [
        (result_df["cpu_status"] == "CRITICAL")
        | (result_df["ram_status"] == "CRITICAL"),
        (result_df["cpu_status"] == "WARNING") | (result_df["ram_status"] == "WARNING"),
    ]
    overall_choices = ["CRITICAL", "WARNING"]
    result_df["overall_status"] = np.select(
        overall_conditions, overall_choices, default="OK"
    )

    return result_df
