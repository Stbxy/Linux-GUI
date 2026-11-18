#!/usr/bin/env bash
set -e
VENV="$HOME/robot-venv"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/python" -V
"$VENV/bin/python" -m pip -V
echo "--- proxy env ---"
printenv | grep -i proxy || echo "no proxy env"
echo "--- venv size ---"
du -sh "$VENV"
echo "VENV_OK"
