import argparse
import json
import logging
import time
from pathlib import Path

import pandas as pd

from collector import analyze_metrics_vectorized, capture_snapshot
from visualize import generate_metrics_chart

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def export_data(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "sys_summary.csv"
    json_path = output_dir / "sys_summary.json"

    df.to_csv(csv_path, index=False)

    records = df.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

    logger.info(f"Đã xuất báo cáo CSV: {csv_path}")
    logger.info(f"Đã xuất báo cáo JSON: {json_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="sys-monitor: Công cụ thu thập và biểu diễn hiệu năng hệ thống CLI"
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1.0,
        help="Khoảng thời gian lấy mẫu (giây). Mặc định: 1.0",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=5,
        help="Số lần lấy mẫu chỉ số. Mặc định: 5",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Thư mục xuất báo cáo. Mặc định: reports",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Hiển thị log chi tiết (DEBUG)",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    logger.info(
        f"Bắt đầu thu thập {args.count} mẫu tài nguyên (Interval: {args.interval}s)..."
    )

    samples: list[dict[str, float | str]] = []
    for idx in range(1, args.count + 1):
        snapshot = capture_snapshot()
        samples.append(snapshot)
        logger.debug(f"Mẫu {idx}/{args.count}: {snapshot}")
        if idx < args.count:
            time.sleep(args.interval)

    raw_df = pd.DataFrame(samples)
    analyzed_df = analyze_metrics_vectorized(raw_df)

    export_data(analyzed_df, args.output_dir)
    chart_file = generate_metrics_chart(analyzed_df, args.output_dir)
    logger.info(f"Đã tạo biểu đồ xu hướng: {chart_file}")
    logger.info("Hoàn tất quy trình thu thập và phân tích sys-monitor!")


if __name__ == "__main__":
    main()
