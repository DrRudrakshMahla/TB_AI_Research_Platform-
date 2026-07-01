"""
TB AI Research Platform v3.0
launch.py
"""

from __future__ import annotations

import gradio as gr

from ui.single_analysis import build_single_analysis
from ai.inference import InferenceEngine
from explainability.native_gradcam import NativeGradCAM
from controllers.single_controller import SingleAnalysisController


def create_app(model_path: str):
    inference = InferenceEngine(model_path)
    target_layers = [inference.model.features[-1]]
    gradcam = NativeGradCAM(inference.model, target_layers)
    controller = SingleAnalysisController(inference, gradcam)

    with gr.Blocks(title="TB AI Research Platform v3.0") as app:
        gr.Markdown("# TB AI Research Platform v3.0")

        with gr.Tabs():
            with gr.Tab("Single Analysis"):
                build_single_analysis(controller)

    return app
