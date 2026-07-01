"""
research_controller.py
"""

from __future__ import annotations

from ai.batch_statistics import BatchStatistics


class ResearchController:
    """Controller for research summaries."""

    def generate_summary(self, results):
        return BatchStatistics.summarize(results)

    def export_dataset(self, results):
        return BatchStatistics.to_json(results)
