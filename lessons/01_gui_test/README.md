# 第 1 课：WSLg + PySide6 + OpenCV 最小闭环

> 键盘没有 `~` 键？把下文的 `~/...` 换成 `"$HOME/..."` 即可，效果一样。

## 目标

在 WSL 里弹出一个 Linux GUI 窗口，显示由 NumPy/OpenCV 生成的测试图；如果有摄像头，再切换到实时画面。

这一步验证三件事：

1. WSLg 能把 Linux 窗口显示到 Windows 桌面。
2. Python 虚拟环境里的 PySide6 能正常加载 Qt 平台插件。
3. OpenCV 生成的图像能正确转换成 Qt 的 `QPixmap` 并显示。

## 前置

- 已完成仓库初始化（根目录有 `指导.md`、`日志.md`）。
- WSL 内已创建 `~/robot-venv`。
- 已安装依赖（见下）。

## 安装依赖

### 1. 系统库（需要输入 Ubuntu 密码）

在 **Ubuntu 终端** 执行：

```bash
sudo apt update
sudo apt install -y \
  fonts-noto-cjk v4l-utils \
  libgl1 libglib2.0-0 \
  libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
  libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 \
  libxcb-xkb1 libxkbcommon-x11-0 libdbus-1-3 libfontconfig1
```

> 这些是 Qt 的 xcb 平台插件和中文显示所需的最小系统库。PySide6 的 wheel 自带 Qt，但不会自带这些系统 `.so`。

### 2. Python 包

```bash
bash /mnt/d/DSH/linux-gui/scripts/install_python_deps.sh
```

脚本会：

- 激活 `~/robot-venv`
- 安装 `numpy`、`opencv-python-headless`、`PySide6`
- 打印三个包的版本

## 运行

```bash
source ~/robot-venv/bin/activate
cd /mnt/d/DSH/linux-gui
python lessons/01_gui_test/main.py
```

## 验收

- Windows 桌面上出现标题为 `Robot Vision GUI - Lesson 01` 的窗口。
- 窗口中有彩色渐变、移动的白色圆、左上角标题、左下角 FPS。
- 点击“打开摄像头”：
  - 有 `/dev/video0`：显示实时画面（左右镜像）。
  - 没有摄像头：状态栏提示“未检测到 /dev/video0”，继续显示测试图，不崩溃。
- 关闭窗口后终端回到提示符，无 Python traceback。

## 排错

### 报错：Could not load the Qt platform plugin "xcb"

缺系统库。执行上面的 `apt install`，然后重试。可以用下面的命令确认：

```bash
python -c "import PySide6; print(PySide6.__version__)"
QT_DEBUG_PLUGINS=1 python lessons/01_gui_test/main.py
```

### 报错：ModuleNotFoundError: No module named 'PySide6'

没有激活虚拟环境。先执行：

```bash
source ~/robot-venv/bin/activate
which python
```

确认 `which python` 指向 `/home/stbxy/robot-venv/bin/python`。

### 窗口能开但中文是方块

缺中文字体：

```bash
sudo apt install -y fonts-noto-cjk
fc-cache -fv
```

### 没有 /dev/video0

第 1 课不要求摄像头；测试图能显示就算通过。第 2 课再配置 usbipd-win 透传。

## 验收记录（2026-11-18）

- `Robot Vision GUI - Lesson 01` 窗口正常出现。
- 环境：Ubuntu 24.04.5 / numpy 2.5.5 / OpenCV 5.1.0 / PySide6 6.12.0。
- 结论：L1 通过；L2 相机接入暂停，下次继续。

## 出处

- Qt for Python：<https://doc.qt.io/qtforpython-6/>
- QImage / QPixmap：<https://doc.qt.io/qtforpython-6/PySide6/QtGui/QImage.html>
- OpenCV Python：<https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html>
- WSLg：<https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps>
