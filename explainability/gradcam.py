"""
TB AI Research Platform v3.0
explainability/gradcam.py
"""

from __future__ import annotations

import cv2
import numpy as np
import torch
from PIL import Image

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image


class NativeGradCAM:
    """Generate Grad-CAM overlays."""

    def __init__(self, model, target_layers):
        self.cam = GradCAM(
            model=model,
            target_layers=target_layers,
        )

    def generate(self, input_tensor, original_image: Image.Image) -> Image.Image:

        # Convert numpy input to torch tensor if necessary
        if isinstance(input_tensor, np.ndarray):
            input_tensor = (
                torch.from_numpy(input_tensor)
                .permute(2, 0, 1)
                .unsqueeze(0)
                .float()
            )

        cam = self.cam(input_tensor=input_tensor)[0]

        width, height = original_image.size

        cam = cv2.resize(
            cam,
            (width, height),
            interpolation=cv2.INTER_CUBIC,
        )

        rgb = (
            np.asarray(original_image.convert("RGB"))
            .astype(np.float32)
            / 255.0
        )

        overlay = show_cam_on_image(
            rgb,
            cam,
            use_rgb=True,
            image_weight=0.55,
        )

        return Image.fromarray(overlay)

    @staticmethod
    def save(image: Image.Image, output_path: str):
        image.save(output_path)
        return output_path
    @staticmethod
    def normalize_heatmap(cam: np.ndarray) -> np.ndarray:
        cam = cam.astype(np.float32)
        cam -= cam.min()
        if cam.max() > 0:
            cam /= cam.max()
        return cam

    @staticmethod
    def blend_overlay(rgb_image: np.ndarray, cam: np.ndarray, alpha: float = 0.45) -> np.ndarray:
        cam = NativeGradCAM.normalize_heatmap(cam)
        heatmap = cv2.applyColorMap(np.uint8(cam * 255), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        return cv2.addWeighted(rgb_image, 1-alpha, heatmap, alpha, 0)
