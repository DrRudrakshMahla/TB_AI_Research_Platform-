"""
TB AI Research Platform v3.0
ai/prediction_result.py

Standard prediction result dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class PredictionResult:
    prediction: str = ""
    probability: float = 0.0
    confidence: float = 0.0
    risk_level: str = ""

    ai_findings: str = ""
    ai_impression: str = ""

    heatmap_path: Optional[str] = None
    report_path: Optional[str] = None

    inference_time: float = 0.0

    model_name: str = ""
    model_version: str = ""

    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Return the result as a serializable dictionary."""
        return asdict(self)
