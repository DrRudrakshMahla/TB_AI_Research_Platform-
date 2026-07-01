
"""
app.py
Complete replacement for TB AI Research Platform v3
"""

from __future__ import annotations

import torch

from ai.model_loader import ModelLoader
from ui.main_window import MainWindow

MODEL_PATH = "models/TB_AI_Final_Model.pth"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_model = ModelLoader.load(MODEL_PATH, DEVICE)
TARGET_LAYERS = [_model.features[-1]]

main_window = MainWindow(
    model_path=MODEL_PATH,
    device=DEVICE,
    target_layers=TARGET_LAYERS,
)

demo = main_window.build()

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )