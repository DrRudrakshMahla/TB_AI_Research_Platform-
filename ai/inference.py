"""
TB AI Research Platform v3.0
ai/inference.py
"""

from __future__ import annotations

import time
import numpy as np
import torch

from ai.prediction_result import PredictionResult


class InferenceEngine:
    """Inference engine for TB classification."""

    def __init__(self, model, device):
        self.model = model
        self.device = device
        self.last_tensor = None
        self.last_logits = None

        self.model.to(device)
        self.model.eval()

    def predict(self, image: np.ndarray) -> PredictionResult:

        start = time.perf_counter()

        tensor = (
            torch.from_numpy(image)
            .permute(2, 0, 1)
            .unsqueeze(0)
            .float()
            .to(self.device)
        )

        # Enable gradients for Grad-CAM
        tensor.requires_grad_(True)

        self.last_tensor = tensor

        self.model.zero_grad()

        logits = self.model(tensor)

        self.last_logits = logits

        probability = torch.sigmoid(logits).flatten()[0].item()

        result = PredictionResult(
            prediction="Tuberculosis"
            if probability >= 0.5
            else "Normal",
            probability=float(probability),
            confidence=float(max(probability, 1.0 - probability)),
            risk_level=(
                "High"
                if probability >= 0.70
                else "Moderate"
                if probability >= 0.40
                else "Low"
            ),
        )

        result.inference_time = round(
            time.perf_counter() - start,
            4,
        )

        return result