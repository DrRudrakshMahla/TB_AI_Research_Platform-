
"""
ai/batch_inference.py
Complete replacement (fixed for Hugging Face Spaces)
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from ai.model_loader import ModelLoader
from ai.inference import InferenceEngine
from ai.data_models import BatchCase, BatchStatistics
from preprocessing.transforms import preprocess_with_original


class BatchInference:

    SUPPORTED_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"
    }

    def __init__(self, model_path: str, device):
        model = ModelLoader.load(model_path, device)
        self.engine = InferenceEngine(model, device)

    def predict_folder(self, folder_path):
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(folder)

        results = []
        stats = BatchStatistics()

        for image_path in sorted(folder.iterdir()):

            if image_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            image = Image.open(image_path).convert("RGB")

            _, processed = preprocess_with_original(image)

            prediction = self.engine.predict(processed)

            results.append(
                BatchCase(
                    case_id=image_path.stem,
                    filename=image_path.name,
                    prediction=prediction.prediction,
                    probability=prediction.probability,
                    confidence=prediction.confidence,
                )
            )

        stats.total_cases = len(results)
        stats.tuberculosis_cases = sum(
            r.prediction == "Tuberculosis" for r in results
        )
        stats.normal_cases = sum(
            r.prediction == "Normal" for r in results
        )
        stats.average_confidence = (
            sum(r.confidence for r in results) / len(results)
            if results else 0.0
        )

        return results, stats