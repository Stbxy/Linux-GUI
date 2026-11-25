#!/usr/bin/env python3
"""Lesson 01: a minimal PySide6 + OpenCV robot vision GUI.

Run inside WSL with the project venv activated:
    source ~/robot-venv/bin/activate
    python lessons/01_gui_test/main.py

The window shows a generated test pattern at first. Click "打开摄像头" to try
/dev/video0; if no camera is present, it stays on the test pattern.
"""

# Teaching scaffold generated for this course on 2026-11-18.
# Not an official Qt/OpenCV/ROS example. See ../../AUTHORS.md.

from __future__ import annotations

import sys
import time

import cv2
import numpy as np
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCloseEvent, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class VisionWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("My Robot Vision GUI")
        self.resize(1000, 680)

        self.cap: cv2.VideoCapture | None = None
        self.frame_count = 0
        self.fps = 0.0
        self.last_time = time.perf_counter()

        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.image_label = QLabel("starting...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(640, 360)
        self.image_label.setStyleSheet("background:#1b2a41; color:#ffffff;")
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.image_label, 1)

        controls = QHBoxLayout()
        self.source_button = QPushButton("开启相机")
        self.source_button.clicked.connect(self.toggle_camera)
        controls.addWidget(self.source_button)

        self.status_label = QLabel("测试图模式（未使用摄像头）")
        controls.addWidget(self.status_label, 1)
        layout.addLayout(controls)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(40)  # ~25 FPS, safe for WSLg software rendering

    # ---------- frame sources ----------

    def make_test_frame(self) -> np.ndarray:
        width, height = 960, 540
        frame = np.full((height, width, 3), (65, 42, 27), dtype=np.uint8)

        t = time.perf_counter()
        cx = int((t * 150) % width)
        cy = int(height / 2 + 70 * np.sin(t * 2.0))
        cv2.circle(frame, (cx, cy), 56, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(frame, (cx, cy), 56, (20, 20, 20), 3, cv2.LINE_AA)

        cv2.putText(
            frame,
            "Robot Vision GUI - Lesson 01",
            (30, 62),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.05,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            f"FPS {self.fps:5.1f} | frame {self.frame_count}",
            (30, height - 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        return frame

    def read_camera_frame(self) -> np.ndarray | None:
        if self.cap is None or not self.cap.isOpened():
            return None
        ok, frame = self.cap.read()
        if not ok or frame is None:
            self.close_camera()
            self.status_label.setText("摄像头读取失败，已回到测试图")
            return None
        # Mirror the image so the operator's movement feels natural.
        return cv2.flip(frame, 1)

    def toggle_camera(self) -> None:
        if self.cap is not None:
            self.close_camera()
            self.status_label.setText("测试图模式（摄像头已关闭）")
            return

        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not cap.isOpened():
            cap.release()
            self.status_label.setText(
                "未检测到 /dev/video0：继续测试图。第 2 课配置 USB 透传。"
            )
            return
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap = cap
        self.source_button.setText("关闭摄像头")
        self.status_label.setText("摄像头模式：/dev/video0")

    def close_camera(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.source_button.setText("打开摄像头")

    # ---------- display loop ----------

    def update_frame(self) -> None:
        now = time.perf_counter()
        dt = now - self.last_time
        self.last_time = now
        if dt > 0:
            instant = 1.0 / dt
            self.fps = instant if self.fps == 0.0 else 0.9 * self.fps + 0.1 * instant

        frame = self.read_camera_frame()
        if frame is None:
            frame = self.make_test_frame()
            source = "TEST"
        else:
            source = "CAM"
            cv2.putText(
                frame,
                f"{source} | FPS {self.fps:5.1f}",
                (20, 36),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

        self.frame_count += 1
        self.show_frame(frame)

    def show_frame(self, frame_bgr: np.ndarray) -> None:
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb.shape
        image = QImage(
            rgb.data,
            width,
            height,
            rgb.strides[0],
            QImage.Format.Format_RGB888,
        ).copy()  # copy() is required: the NumPy buffer is reused next frame
        pixmap = QPixmap.fromImage(image)

        target = self.image_label.size()
        if target.width() < 10 or target.height() < 10:
            target = pixmap.size()
        self.image_label.setPixmap(
            pixmap.scaled(
                target,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.timer.stop()
        self.close_camera()
        event.accept()


def main() -> int:
    app = QApplication(sys.argv)
    window = VisionWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
