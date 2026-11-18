#!/usr/bin/env bash
set +e
echo "=== OS ==="
lsb_release -a 2>/dev/null
uname -a
echo "IDENTITY=$(id)"
echo "SYSTEMD=$(timeout -k 2 5 systemctl is-system-running 2>&1)"
echo "WSLG=$(test -d /mnt/wslg && echo yes || echo no)"
echo "DISPLAY=$(printenv DISPLAY || echo unset)"
echo "WAYLAND=$(printenv WAYLAND_DISPLAY || echo unset)"
echo "AUDIO=$(printenv PULSE_SERVER || echo unset)"
echo "=== HW ==="
echo "CORES=$(nproc)"
free -h
df -h /
echo "=== PYTHON ==="
python3 --version
timeout 10 python3 -m pip --version 2>&1 | head -1
python3 - <<'PY'
mods = ["numpy", "cv2", "PySide6", "PyQt6", "rclpy"]
for m in mods:
    try:
        mod = __import__(m)
        print(m, getattr(mod, "__version__", "ok"))
    except Exception as e:
        print(m, "MISSING", type(e).__name__)
PY
echo "=== ROS ==="
ls -d /opt/ros/* 2>/dev/null || echo no-ros
command -v ros2 || true
echo "=== QT/OPENCV PKGS ==="
dpkg -l 2>/dev/null | awk '/qt6-base|pyside6|python3-opencv|ros-jazzy/ {print $2, $3}' | head -20
echo "=== CAMERA ==="
ls -l /dev/video* 2>/dev/null || echo no-video-device
command -v v4l2-ctl || true
echo "=== NET ==="
timeout 8 curl -sI https://github.com | head -1
timeout 8 curl -sI https://docs.ros.org | head -1
echo "=== APT SOURCES ==="
grep -rhsE '^deb ' /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null | head -8
echo "=== CJK FONTS ==="
timeout 8 fc-list :lang=zh 2>/dev/null | head -3
echo "=== DONE ==="
