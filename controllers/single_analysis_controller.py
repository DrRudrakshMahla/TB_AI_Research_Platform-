"""
TB AI Research Platform v3.0
controllers/single_analysis_controller.py
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image

from ai.model_loader import ModelLoader
from ai.inference import InferenceEngine
from explainability.gradcam import NativeGradCAM
from preprocessing.transforms import preprocess_with_original
from reports.pdf_report import PDFReport
from reports.json_report import JSONReport


class SingleAnalysisController:

    def __init__(self, model_path, device, target_layers=None):

        self.device = device

        self.model = ModelLoader.load(
            model_path,
            device,
        )

        self.inference = InferenceEngine(
            self.model,
            device,
        )

        self.gradcam = NativeGradCAM(
            self.model,
            [self.model.features[-1]],
        )

    def analyze(self, image: Image.Image, pdf_path, json_path):

        original, processed = preprocess_with_original(image)

        result = self.inference.predict(processed)

        heatmap = self.gradcam.generate(
            self.inference.last_tensor,
            original,
        )

        pdf_path = Path(pdf_path)
        json_path = Path(json_path)

        heatmap_path = json_path.with_name(
            json_path.stem + "_gradcam.png"
        )

        heatmap.save(heatmap_path)

        result.heatmap_path = str(heatmap_path)

        PDFReport.save(result, str(pdf_path))
        JSONReport.save(result, str(json_path))

        result.report_path = str(pdf_path)

        return result