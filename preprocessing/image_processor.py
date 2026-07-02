"""
TB AI Research Platform v3.0
preprocessing/image_processor.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from PIL import Image

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


@dataclass
class ProcessedImage:
    original: Image.Image
    resized: Image.Image
    tensor: torch.Tensor
    width: int
    height: int


class ImageProcessor:
    def __init__(self, image_size: int = 224):
        self.image_size = image_size

    def process(self, image: Image.Image) -> ProcessedImage:
        if image is None:
            raise ValueError("Input image is None")

        original = image.convert("RGB")
        width, height = original.size

        resized = original.resize(
            (self.image_size, self.image_size),
            Image.BILINEAR,
        )

        arr = np.asarray(resized).astype(np.float32) / 255.0
        arr = (arr - IMAGENET_MEAN) / IMAGENET_STD

        tensor = (
            torch.from_numpy(arr)
            .permute(2, 0, 1)
            .unsqueeze(0)
            .float()
        )

        return ProcessedImage(
            original=original,
            resized=resized,
            tensor=tensor,
            width=width,
            height=height,
        )


import cv2

def compute_basic_quality(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim==3 else image
    return {
        "blur": float(cv2.Laplacian(gray, cv2.CV_64F).var()),
        "brightness": float(gray.mean()),
        "contrast": float(gray.std()),
    }
