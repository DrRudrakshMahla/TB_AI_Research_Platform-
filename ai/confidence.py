"""
TB AI Research Platform v3.0
ai/confidence.py
"""

from __future__ import annotations

from ai.prediction_result import PredictionResult


class ConfidenceEngine:
    """Compute confidence and risk level from prediction probability."""

    @staticmethod
    def update(result: PredictionResult) -> PredictionResult:
        p = float(result.probability)

        result.confidence = max(p, 1.0 - p)

        if p >= 0.90:
            result.risk_level = "Very High"
        elif p >= 0.80:
            result.risk_level = "High"
        elif p >= 0.50:
            result.risk_level = "Moderate"
        elif p >= 0.20:
            result.risk_level = "Low"
        else:
            result.risk_level = "Very Low"

        result.metadata["confidence_percent"] = round(result.confidence * 100, 2)
        result.metadata["tb_probability_percent"] = round(p * 100, 2)

        return result
