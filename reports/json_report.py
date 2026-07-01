
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