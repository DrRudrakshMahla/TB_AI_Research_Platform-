"""
TB AI Research Platform v3.0
health_check.py
"""

from __future__ import annotations

import importlib
from pathlib import Path
import torch


REQUIRED_MODULES = [
    "torch",
    "torchvision",
    "gradio",
    "numpy",
    "PIL",
    "cv2",
    "reportlab",
    "pydicom",
]


def check_dependencies():
    results = {}
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
            results[module] = "OK"
        except Exception as e:
            results[module] = f"FAILED ({e})"
    return results


def check_model(model_path: str):
    path = Path(model_path)
    if not path.exists():
        return "Model file not found"

    try:
        checkpoint = torch.load(path, map_location="cpu", weights_only=False)
        return f"OK ({type(checkpoint).__name__})"
    except Exception as e:
        return f"FAILED ({e})"


def run_health_check(model_path: str):
    return {
        "python": "OK",
        "device": "CUDA" if torch.cuda.is_available() else "CPU",
        "dependencies": check_dependencies(),
        "model": check_model(model_path),
    }


if __name__ == "__main__":
    from pprint import pprint
    pprint(run_health_check("models/TB_AI_Final_Model.pth"))
