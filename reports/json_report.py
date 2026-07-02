
"""
reports/json_report.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path


class JSONReport:
    """Export prediction results safely to JSON."""

    @staticmethod
    def save(result, output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if is_dataclass(result):
            data = asdict(result)
        elif hasattr(result, "to_dict"):
            data = result.to_dict()
        elif hasattr(result, "__dict__"):
            data = dict(result.__dict__)
        else:
            data = {"result": str(result)}

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
                default=str,
            )

        return output_path

def attach_quality(report: dict, quality_result):
    """Attach quality metrics to exported JSON."""
    if quality_result is None:
        return report
    report["image_quality"] = {
        "overall_score": getattr(quality_result, "overall_score", None),
        "blur_score": getattr(quality_result, "blur_score", None),
        "exposure_score": getattr(quality_result, "exposure_score", None),
        "contrast_score": getattr(quality_result, "contrast_score", None),
        "recommendation": getattr(quality_result, "recommendation", ""),
        "analysis_allowed": getattr(quality_result, "analysis_allowed", False),
    }
    return report
