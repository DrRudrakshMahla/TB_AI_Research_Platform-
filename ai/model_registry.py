"""
TB AI Research Platform v3.0
ai/model_registry.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable


class ModelRegistry:
    """Registry for AI models."""

    def __init__(self):
        self._models = {}

    def register(
        self,
        name: str,
        builder: Callable,
        weights: str | Path,
    ) -> None:
        self._models[name] = {
            "builder": builder,
            "weights": str(weights),
            "instance": None,
        }

    def load(self, name: str):
        if name not in self._models:
            raise KeyError(f"Unknown model: {name}")

        entry = self._models[name]

        if entry["instance"] is None:
            entry["instance"] = entry["builder"](entry["weights"])

        return entry["instance"]

    def unload(self, name: str):
        if name in self._models:
            self._models[name]["instance"] = None

    def list_models(self):
        return list(self._models.keys())

    def is_loaded(self, name: str) -> bool:
        return (
            name in self._models and
            self._models[name]["instance"] is not None
        )
