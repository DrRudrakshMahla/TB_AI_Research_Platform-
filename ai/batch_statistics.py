
"""
ai/batch_statistics.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

from collections import Counter


class BatchStatistics:
    """Utility methods for batch inference statistics."""

    @staticmethod
    def summarize(results):
        summary = {
            "total_cases": len(results),
            "tuberculosis_cases": 0,
            "normal_cases": 0,
            "average_confidence": 0.0,
        }

        if not results:
            return summary

        counts = Counter(r.prediction for r in results)
        summary["tuberculosis_cases"] = counts.get("Tuberculosis", 0)
        summary["normal_cases"] = counts.get("Normal", 0)
        summary["average_confidence"] = (
            sum(r.confidence for r in results) / len(results)
        )
        return summary

    @staticmethod
    def calculate(results):
        return BatchStatistics.summarize(results)

    @staticmethod
    def to_json(results):
        return [
            {
                "case_id": r.case_id,
                "filename": r.filename,
                "prediction": r.prediction,
                "probability": r.probability,
                "confidence": r.confidence,
            }
            for r in results
        ]