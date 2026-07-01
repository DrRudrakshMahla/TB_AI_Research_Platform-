"""
TB AI Research Platform v3.0
reports/csv_report.py
"""

from __future__ import annotations

import csv
from pathlib import Path


class CSVReport:
    """Export batch prediction results to CSV."""

    HEADERS = [
        "Filename",
        "Prediction",
        "Probability",
        "Confidence",
        "Risk Level",
        "Inference Time (s)",
        "Model",
        "Version",
    ]

    @staticmethod
    def save(results, output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSVReport.HEADERS)

            for r in results:
                writer.writerow([
                    r.metadata.get("filename", ""),
                    r.prediction,
                    round(r.probability, 4),
                    round(r.confidence, 4),
                    r.risk_level,
                    round(r.inference_time, 4),
                    r.model_name,
                    r.model_version,
                ])

        return output_path
