"""
ui/single_analysis.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import gradio as gr

from controllers.single_analysis_controller import SingleAnalysisController


class SingleAnalysisUI:
    """Gradio UI for single image analysis."""

    def __init__(self, model_path: str, device, target_layers):
        self.controller = SingleAnalysisController(
            model_path=model_path,
            device=device,
            target_layers=target_layers,
        )

    def analyze(self, image):
        if image is None:
            raise gr.Error("Please upload a chest X-ray image.")

        work = Path(tempfile.mkdtemp())
        pdf_path = work / "TB_Report.pdf"
        json_path = work / "TB_Result.json"

        result = self.controller.analyze(
            image=image,
            pdf_path=pdf_path,
            json_path=json_path,
        )

        return (
            result.prediction,
            result.probability,
            result.confidence,
            result.risk_level,
            result.heatmap_path,
            result.report_path,
            str(json_path),
        )

    def build(self):
        with gr.Row():
            with gr.Column(scale=1):
                image = gr.Image(
                    type="pil",
                    label="Chest X-ray"
                )
                analyze_btn = gr.Button(
                    "Analyze",
                    variant="primary"
                )

            with gr.Column(scale=1):
                prediction = gr.Textbox(label="Prediction")
                probability = gr.Number(label="Probability")
                confidence = gr.Number(label="Confidence")
                risk = gr.Textbox(label="Risk Level")

            with gr.Column(scale=1):
                heatmap = gr.Image(label="Grad-CAM")
                pdf = gr.File(label="PDF Report")
                json_file = gr.File(label="JSON Report")

        analyze_btn.click(
            fn=self.analyze,
            inputs=image,
            outputs=[
                prediction,
                probability,
                confidence,
                risk,
                heatmap,
                pdf,
                json_file,
            ],
        )

# v4 Quality UI helper
def quality_status(result):
    if result is None:
        return ""
    return f"Quality: {getattr(result,'overall_score',0):.0f}/100"
