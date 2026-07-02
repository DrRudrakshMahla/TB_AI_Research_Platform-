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


    @staticmethod
    def update_with_quality(result: PredictionResult, quality_score: float | None):
        ConfidenceEngine.update(result)
        result.image_quality = quality_score
        if quality_score is None:
            return result
        result.confidence_label = (
            "Reliable" if quality_score>=80 else
            "Interpret with caution" if quality_score>=60 else
            "Low reliability due to image quality"
        )
        return result
