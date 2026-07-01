"""
preprocessing/preprocess.py
"""

from __future__ import annotations

import torch
import torchvision.transforms as transforms
from PIL import Image

from config.settings import Settings

IMAGE_SIZE = Settings.IMAGE_SIZE
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


def load_image(image):
    if isinstance(image, Image.Image):
        return image.convert("RGB")
    return Image.open(image).convert("RGB")


def preprocess_image(image):
    """
    Returns:
        original_image, input_tensor
    """
    image = load_image(image)
    tensor = _transform(image)
    tensor = tensor.unsqueeze(0).to(DEVICE)
    return image, tensor
