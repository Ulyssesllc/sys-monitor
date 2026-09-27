from pathlib import Path

import pandas as pd
import pytest

from collector import analyze_metrics_vectorized, capture_snapshot
from main import export_data, main, setup_logging
from visualize import generate_metrics_chart


def test_capture_snapshot() -> None:
    snapshot = capture_snapshot()
    assert "timestamp" in snapshot
    assert "cpu_percent" in snapshot
    assert "ram_percent" in snapshot
    assert "disk_percent" in snapshot
    assert isinstance(snapshot["cpu_percent"], float)


def test_analyze_metrics_vectorized_empty() -> None:
    df = pd.DataFrame()
    result = analyze_metrics_vectorized(df)
    assert result.empty


def test_analyze_metrics_vectorized_thresholds() -> None:
    raw_data = [
        {
            "timestamp": "10:00:00",
            "cpu_percent": 10.0,
            "ram_percent": 20.0,
            "disk_percent": 30.0,
        },
        {
            "timestamp": "10:01:00",
            "cpu_percent": 75.0,
            "ram_percent": 80.0,
            "disk_percent": 30.0,
        },
        {
            "timestamp": "10:02:00",
            "cpu_percent": 90.0,
            "ram_percent": 95.0,
            "disk_percent": 30.0,
        },
    ]
    df = pd.DataFrame(raw_data)
    result = analyze_metrics_vectorized(df)
    assert result.loc[0, "cpu_status"] == "OK"
    assert result.loc[0, "overall_status"] == "OK"

    assert result.loc[1, "cpu_status"] == "WARNING"
    assert result.loc[1, "ram_status"] == "WARNING"
    assert result.loc[1, "overall_status"] == "WARNING"
    assert result.loc[2, "cpu_status"] == "CRITICAL"
    assert result.loc[2, "overall_status"] == "CRITICAL"


def test_export_data_and_chart(tmp_path: Path) -> None:
    df = pd.DataFrame(
        [
            {
                "timestamp": "10:00:00",
                "cpu_percent": 50.0,
                "ram_percent": 60.0,
                "disk_percent": 70.0,
                "cpu_status": "OK",
                "ram_status": "OK",
                "overall_status": "OK",
            }
        ]
    )
    output_dir = tmp_path / "reports"
    export_data(df, output_dir)
    assert (output_dir / "sys_summary.csv").exists()
    assert (output_dir / "sys_summary.json").exists()
    chart_path = generate_metrics_chart(df, output_dir)
    assert chart_path.exists()


def test_setup_logging() -> None:
    setup_logging(verbose=True)
    setup_logging(verbose=False)


def test_main_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output_dir = tmp_path / "cli_reports"
    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "--count",
            "2",
            "--interval",
            "0.1",
            "-o",
            str(output_dir),
            "-v",
        ],
    )
    main()
    assert (output_dir / "sys_summary.csv").exists()
    assert (output_dir / "sys_summary.json").exists()
    assert (output_dir / "sys_metrics.png").exists()
