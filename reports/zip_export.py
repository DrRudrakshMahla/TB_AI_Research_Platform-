"""
TB AI Research Platform v3.0
reports/zip_export.py
"""

from __future__ import annotations

from pathlib import Path
import zipfile


class ZipExport:
    """Create a ZIP archive from a case folder or output directory."""

    @staticmethod
    def create(source_dir: str | Path, output_zip: str | Path) -> Path:
        source_dir = Path(source_dir)
        output_zip = Path(output_zip)

        output_zip.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in source_dir.rglob("*"):
                if file.is_file():
                    zf.write(file, arcname=file.relative_to(source_dir))

        return output_zip