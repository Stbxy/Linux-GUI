# 机器人 Linux 视觉与 GUI 学习仓库

这个仓库记录我从零开始，为机器人搭建 **Linux 视觉采集 + 图形界面（GUI）** 的学习过程。

## 目标

最终在机器人本体的 Linux 系统上跑通这条链路：

```text
相机 → Linux 采集 → 视觉处理（OpenCV / ROS 2）→ GUI 显示与操作 → 机器人执行
```

## 当前环境

| 项目 | 配置 |
|---|---|
| 开发机 | Windows 11 + WSL2 |
| Linux | Ubuntu 24.04.5 LTS |
| WSL | 3.0.5，WSLg 可用 |
| Python | 3.12.3 |
| 视觉/GUI | numpy 2.5.5、OpenCV 5.1.0、PySide6 6.12.0 |
| 状态 | L0 + L1 完成；L2 相机接入暂停，下次继续 |

GitHub 仓库：<https://github.com/Stbxy/Linux-GUI>

## 文档

- [指导.md](指导.md)：课程路线、每课步骤、验收标准、权威出处
- [日志.md](日志.md)：每次对话与学习记录

## 学习路线

| 阶段 | 内容 | 产出 |
|---|---|---|
| L0 | 环境、Git、文档 | 可复现的学习仓库 |
| L1 | WSLg + Python + OpenCV + PySide6 | 能显示图像的 Linux GUI 窗口 |
| L2 | 相机接入与标定 | 实时画面 + 相机内参 |
| L3 | ROS 2 Jazzy | 图像话题、rqt、RViz2 |
| L4 | Qt GUI 接入 ROS 2 | 机器人操作界面 |
| L5 | 部署到机器人 | 开机自启、kiosk、性能优化 |

## 常用命令

```bash
# 进入 WSL
wsl -d Ubuntu-24.04

# 查看仓库状态
git status
git log --oneline --graph

# 第 1 课运行
source ~/robot-venv/bin/activate
cd /mnt/d/DSH/linux-gui
python lessons/01_gui_test/main.py
```

> 说明：WSL2 是开发环境，最终要部署到机器人本体的 Linux（Jetson / 树莓派 / 工控机）。两者不能混为一谈。
