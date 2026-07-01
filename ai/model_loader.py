"""
TB AI Research Platform v3.0
ai/model_loader.py
"""

from __future__ import annotations

from pathlib import Path

import torch

from ai.tb_densenet import build_tb_densenet


class ModelLoader:
    """Load the trained TB AI model."""

    @staticmethod
    def load(
        model_path: str | Path,
        device,
    ):
        """
        Load the trained DenseNet model.

        Args:
            model_path: Path to .pth file.
            device: torch.device

        Returns:
            Loaded model.
        """

        model = build_tb_densenet()

        checkpoint = torch.load(
            model_path,
            map_location=device,
        )

        if isinstance(checkpoint, dict):
            if "state_dict" in checkpoint:
                checkpoint = checkpoint["state_dict"]
            elif "model_state_dict" in checkpoint:
                checkpoint = checkpoint["model_state_dict"]

        model.load_state_dict(checkpoint)

        model.to(device)
        model.eval()

        return model