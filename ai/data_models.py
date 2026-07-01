
"""
ai/data_models.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class PredictionResult:
    prediction: str
    probability: float
    confidence: float
    risk_level: str = ""
    heatmap_path: str = ""
    report_path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass
class BatchCase:
    case_id: str
    filename: str
    prediction: str
    probability: float
    confidence: float
    heatmap_path: str = ""
    report_path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass
class BatchStatistics:
    total_cases: int = 0
    tuberculosis_cases: int = 0
    normal_cases: int = 0
    average_confidence: float = 0.0

    @property
    def tb_percentage(self):
        return 0.0 if self.total_cases == 0 else round(
            self.tuberculosis_cases * 100 / self.total_cases, 2
        )

    @property
    def normal_percentage(self):
        return 0.0 if self.total_cases == 0 else round(
            self.normal_cases * 100 / self.total_cases, 2
        )

    def to_dict(self):
        return {
            "total_cases": self.total_cases,
            "tuberculosis_cases": self.tuberculosis_cases,
            "normal_cases": self.normal_cases,
            "average_confidence": self.average_confidence,
            "tb_percentage": self.tb_percentage,
            "normal_percentage": self.normal_percentage,
        }