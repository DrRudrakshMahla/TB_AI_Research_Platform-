"""
TB AI Research Platform v3.0
ai/findings.py
"""

from __future__ import annotations

from ai.prediction_result import PredictionResult


class FindingsGenerator:
    """Generate structured AI findings and impression."""

    @staticmethod
    def populate(result: PredictionResult) -> PredictionResult:
        p = result.probability

        if p >= 0.80:
            result.ai_findings = (
                "High probability of pulmonary tuberculosis on chest radiograph."
            )
            result.ai_impression = (
                "AI findings are highly suspicious for pulmonary tuberculosis. "
                "Clinical correlation and microbiological confirmation are advised."
            )

        elif p >= 0.50:
            result.ai_findings = (
                "Indeterminate abnormality with moderate probability of tuberculosis."
            )
            result.ai_impression = (
                "Correlation with clinical findings and additional investigations "
                "is recommended."
            )

        else:
            result.ai_findings = (
                "No significant radiographic features suggestive of pulmonary tuberculosis."
            )
            result.ai_impression = (
                "No AI evidence of pulmonary tuberculosis on this examination."
            )

        return result
