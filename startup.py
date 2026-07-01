"""
TB AI Research Platform v3.0
startup.py
"""

from __future__ import annotations

import sys

from health_check import run_health_check
from launch import create_app

MODEL_PATH = "models/TB_AI_Final_Model.pth"


def main() -> int:
    status = run_health_check(MODEL_PATH)

    print("=" * 60)
    print("TB AI Research Platform v3.0 Startup")
    print("=" * 60)
    print(f"Device : {status['device']}")
    print(f"Model  : {status['model']}")

    failed = [
        name for name, state in status["dependencies"].items()
        if state != "OK"
    ]

    if failed:
        print("
Dependency check failed:")
        for dep in failed:
            print(f" - {dep}: {status['dependencies'][dep]}")
        return 1

    print("
All checks passed. Launching application...")

    app = create_app(MODEL_PATH)
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
