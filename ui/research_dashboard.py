
"""
ui/research_dashboard.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

import json
from pathlib import Path

import gradio as gr

from ai.batch_statistics import BatchStatistics


class ResearchDashboard:
    """Research dashboard Gradio UI."""

    def __init__(self):
        self._latest_results = []

    def update_results(self, results):
        self._latest_results = results or []

    def generate(self):
        if not self._latest_results:
            return (
                "## Research Dashboard\n\nNo batch analysis has been run yet.",
                None,
            )

        summary = BatchStatistics.summarize(self._latest_results)

        report = {
            "summary": summary,
            "results": BatchStatistics.to_json(self._latest_results),
        }

        out = Path("research_summary.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        md = f"""## Research Dashboard

**Total Cases:** {summary['total_cases']}

**Tuberculosis Cases:** {summary['tuberculosis_cases']}

**Normal Cases:** {summary['normal_cases']}

**Average Confidence:** {summary['average_confidence']:.2f}
"""

        return md, str(out)

    def build(self):
        gr.Markdown("## Research Dashboard")
        btn = gr.Button("Generate Research Summary", variant="primary")
        summary = gr.Markdown()
        report = gr.File(label="Research JSON Report")

        btn.click(
            fn=self.generate,
            outputs=[summary, report],
        )