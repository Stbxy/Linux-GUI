#!/usr/bin/env bash
set -euo pipefail
source "$HOME/robot-venv/bin/activate"
python -m pip install --upgrade pip wheel
python -m pip install "numpy<3" opencv-python-headless PySide6
python - <<'PY'
import numpy, cv2, PySide6
print("NUMPY", numpy.__version__)
print("OPENCV", cv2.__version__)
print("PYSIDE6", PySide6.__version__)
PY
echo "DEPS_OK"
