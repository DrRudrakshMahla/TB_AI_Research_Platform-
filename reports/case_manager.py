"""
TB AI Research Platform v3.0
reports/case_manager.py
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import shutil


class CaseManager:
    """Create and manage case folders."""

    def __init__(self, root: str | Path = "Cases"):
        self.root = Path(root)

    def create_case(self) -> Path:
        now = datetime.now()
        case_dir = (
            self.root
            / str(now.year)
            / now.strftime("%Y%m%d_%H%M%S")
        )
        case_dir.mkdir(parents=True, exist_ok=True)
        return case_dir

    @staticmethod
    def save_file(source: str | Path, case_dir: str | Path, name: str) -> Path:
        source = Path(source)
        case_dir = Path(case_dir)
        destination = case_dir / name
        shutil.copy2(source, destination)
        return destination
