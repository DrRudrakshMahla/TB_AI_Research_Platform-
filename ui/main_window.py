
"""
ui/main_window.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

import gradio as gr

from ui.single_analysis import SingleAnalysisUI
from ui.batch_analysis import BatchAnalysisUI
from ui.research_dashboard import ResearchDashboard


class MainWindow:

    def __init__(self, model_path, device, target_layers):
        self.single = SingleAnalysisUI(
            model_path=model_path,
            device=device,
            target_layers=target_layers,
        )
        self.batch = BatchAnalysisUI(
            model_path=model_path,
            device=device,
        )
        self.research = ResearchDashboard()

    def analyze_single(self, image, pdf_path=None, json_path=None):
        # Backward-compatible wrapper used by app.py
        return self.single.controller.analyze(image, pdf_path, json_path)

    def build(self):
        with gr.Blocks(title="TB AI Research Platform v3") as demo:
            gr.Markdown("# TB AI Research Platform v3")

            with gr.Tabs():
                with gr.Tab("Single Analysis"):
                    self.single.build()

                with gr.Tab("Batch Analysis"):
                    self.batch.build()

                with gr.Tab("Research"):
                    self.research.build()

        return demo
# v4 Quality integration ready
