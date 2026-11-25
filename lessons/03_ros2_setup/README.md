# L3：安装 ROS 2 Jazzy

## 目标

在 WSL 的 Ubuntu 24.04 上安装 ROS 2 Jazzy，并跑通 talker/listener。

## 前置

- Ubuntu 24.04（Noble）
- 能访问 GitHub 和 packages.ros.org
- 至少 5 GB 空闲磁盘
- 已打开 Ubuntu 终端

## 第 0 步：检查环境

```bash
lsb_release -ds
locale
df -h /
```

逐行解释：

- `lsb_release -ds`：确认是 Ubuntu 24.04。
- `locale`：确认 LANG 是 UTF-8。
- `df -h /`：确认根分区剩余空间。

## 第 1 步：安装 ROS 2 apt 源

```bash
sudo apt update
sudo apt install -y curl software-properties-common
sudo add-apt-repository universe -y
curl -L -o /tmp/ros2-apt-source.deb https://github.com/ros-infrastructure/ros-apt-source/releases/download/1.3.0/ros2-apt-source_1.3.0.noble_all.deb
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update
```

逐行解释：

- `sudo apt update`：刷新 Ubuntu 软件源。
- `sudo apt install -y curl software-properties-common`：安装下载工具和 `add-apt-repository`。
- `sudo add-apt-repository universe -y`：启用 Ubuntu universe 仓库。
- `curl -L -o ...`：下载 ros2-apt-source 的 noble 包。
- `sudo dpkg -i ...`：安装 ROS 2 的 apt 源和密钥配置。
- `sudo apt update`：刷新 ROS 2 软件源。

> 版本 `1.3.0` 是 2026-11-25 的最新版；如果链接失效，按官方文档重新获取。

## 第 2 步：安装 ROS 2 Jazzy Desktop

```bash
sudo apt install -y ros-jazzy-desktop
```

逐行解释：

- `sudo apt install -y`：自动确认安装。
- `ros-jazzy-desktop`：ROS 2 Jazzy 桌面版，包含 RViz、rqt、demo 和教程。

下载量较大，可能需要几分钟到十几分钟。

## 第 3 步：加载环境

```bash
source /opt/ros/jazzy/setup.bash
ros2 --help
```

逐行解释：

- `source /opt/ros/jazzy/setup.bash`：把 ROS 2 命令加入当前 shell。
- `ros2 --help`：确认 `ros2` 命令可用。

## 第 4 步：跑 talker/listener

终端 A：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

终端 B：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

逐行解释：

- 第一行：每个新终端都要先加载 ROS 2 环境。
- `ros2 run`：运行一个 ROS 2 包里的节点。
- `demo_nodes_cpp talker`：C++ 发布者，持续发送 `Hello World`。
- `demo_nodes_py listener`：Python 订阅者，打印收到的消息。

## 验收

- `ros2 --help` 能列出命令。
- talker 持续输出 `Publishing: 'Hello World: N'`。
- listener 持续输出 `I heard: [Hello World: N]`。

## 排错

- `ros2: command not found`：没有 `source /opt/ros/jazzy/setup.bash`。
- apt 下载失败：检查代理和网络。
- `dpkg` 依赖错误：把完整输出发我，不要继续乱装。

## listener 收不到消息

先不要重装。按顺序检查。

### 1. 两个终端都加载环境

两个终端都执行：

~~~bash
deactivate
source /opt/ros/jazzy/setup.bash
~~~

逐行解释：

- `deactivate`：如果还在 `(robot-venv)` 里，先退出；ROS 2 用系统 Python。
- `source ...`：加载 ROS 2 环境。

### 2. 确认节点和话题

在 talker 运行时，另开终端：

~~~bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
ros2 topic info /chatter
~~~

逐行解释：

- `ros2 node list`：应该看到 `/talker`。
- `ros2 topic list`：应该看到 `/chatter`。
- `ros2 topic info /chatter`：看发布者/订阅者数量。

### 3. 直接 echo 话题

~~~bash
ros2 topic echo /chatter
~~~

逐行解释：

- `ros2 topic echo`：直接订阅并打印话题内容。
- 能看到 `data: Hello World: N`，说明发布/发现正常，问题在 listener。
- 看不到，说明 DDS 发现或网络有问题。

### 4. 限制为本地发现

两个终端都执行，然后重启 talker/listener：

~~~bash
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
~~~

逐行解释：

- `export`：设置当前 shell 的环境变量。
- `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`：只在本机发现节点，避开 WSL 多播问题。

### 5. 诊断报告

~~~bash
ros2 doctor --report
~~~

逐行解释：

- `ros2 doctor`：检查 ROS 2 配置和网络。
- `--report`：输出完整报告。
## 出处

- ROS 2 Jazzy 官方安装文档：<https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html>
- ros2-apt-source Releases：<https://github.com/ros-infrastructure/ros-apt-source/releases>
- ROS 2 教程：<https://docs.ros.org/en/jazzy/Tutorials.html>
