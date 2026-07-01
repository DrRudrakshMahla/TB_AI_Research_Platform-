"""
TB AI Research Platform v3.0
preprocessing/transforms.py

Image preprocessing transforms for inference.
"""

from __future__ import annotations

from PIL import Image
import numpy as np


IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def preprocess_image(image: Image.Image, image_size: int = 224) -> np.ndarray:
    """
    Convert a PIL image into a normalized HWC float32 array.
    """
    image = image.convert("RGB")
    image = image.resize((image_size, image_size), Image.BILINEAR)

    array = np.asarray(image).astype(np.float32) / 255.0
    array = (array - IMAGENET_MEAN) / IMAGENET_STD

    return array


def preprocess_with_original(
    image: Image.Image,
    image_size: int = 224,
):
    """
    Return normalized model input and untouched original image.
    """
    original = image.copy()
    processed = preprocess_image(image, image_size)
    return original, processed
