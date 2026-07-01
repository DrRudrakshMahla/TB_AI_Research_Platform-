"""
TB AI Research Platform v3.0
Module : ai/device.py
Author : Dr. Rudraksh Mahla & OpenAI ChatGPT

Central device management for AI inference.
"""

from __future__ import annotations

import platform
import torch


def get_device() -> torch.device:
    """Return the best available inference device."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


DEVICE = get_device()


def device_name() -> str:
    if DEVICE.type == "cuda":
        return torch.cuda.get_device_name(0)
    if DEVICE.type == "mps":
        return "Apple Metal (MPS)"
    return platform.processor() or "CPU"


def is_gpu_available() -> bool:
    return DEVICE.type in ("cuda", "mps")


def device_summary() -> dict:
    return {
        "device": str(DEVICE),
        "device_name": device_name(),
        "gpu_available": is_gpu_available(),
        "torch_version": torch.__version__,
    }


if __name__ == "__main__":
    print("=" * 50)
    print("TB AI Research Platform v3.0")
    print("Device Summary")
    print("=" * 50)
    for k, v in device_summary().items():
        print(f"{k:15}: {v}")
