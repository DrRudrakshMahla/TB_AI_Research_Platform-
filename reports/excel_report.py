"""
TB AI Research Platform v3.0
reports/excel_report.py
"""

from __future__ import annotations

from pathlib import Path
from openpyxl import Workbook


class ExcelReport:
    """Export batch prediction results to Excel."""

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

        wb = Workbook()
        ws = wb.active
        ws.title = "Batch Results"

        ws.append(ExcelReport.HEADERS)

        for r in results:
            ws.append([
                r.metadata.get("filename", ""),
                r.prediction,
                round(r.probability, 4),
                round(r.confidence, 4),
                r.risk_level,
                round(r.inference_time, 4),
                r.model_name,
                r.model_version,
            ])

        wb.save(output_path)
        return output_path
