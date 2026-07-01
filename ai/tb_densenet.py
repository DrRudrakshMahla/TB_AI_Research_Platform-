"""
TB AI Research Platform v3.0
ai/models/tb_densenet.py

DenseNet121 architecture used by the TB classifier.
"""

from __future__ import annotations

import torch.nn as nn
from torchvision.models import densenet121


def build_tb_densenet(num_classes: int = 1) -> nn.Module:
    """
    Build the DenseNet121 model architecture.

    Parameters
    ----------
    num_classes : int
        Number of output classes. For TB binary classification this is 1.
    """
    model = densenet121(weights=None)

    in_features = model.classifier.in_features
    model.classifier = nn.Linear(in_features, num_classes)

    return model
