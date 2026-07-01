"""
batch_controller.py
"""

from __future__ import annotations

from ai.batch_inference import BatchInference
from ai.batch_statistics import BatchStatistics


class BatchController:
    """Coordinates batch inference and statistics."""

    def __init__(self, model_path: str, device):
        self.engine = BatchInference(model_path, device)

    def analyze(self, folder_path):
        results, _ = self.engine.predict_folder(folder_path)
        summary = BatchStatistics.summarize(results)
        return {
            "results": results,
            "summary": summary,
        }
