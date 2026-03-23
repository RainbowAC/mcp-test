#!/bin/bash
# MCP Platform 安装脚本

set -e  # 出错时退出

echo "==================================="
echo "MCP Development Platform 安装脚本"
echo "==================================="

# 检查是否已安装 Python
if ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python。请先安装 Python 3.8 或更高版本。"
    exit 1
fi

PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l) -ne 1 ]]; then
    echo "错误: Python 版本过低。需要 Python 3.8 或更高版本，当前版本: $PYTHON_VERSION"
    exit 1
fi

echo "Python 版本: $PYTHON_VERSION ✓"

# 检查是否已安装 pip
if ! command -v pip &> /dev/null; then
    echo "错误: 未找到 pip。请先安装 pip。"
    exit 1
fi

echo "pip 已安装 ✓"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
    echo "虚拟环境创建完成 ✓"
else
    echo "虚拟环境已存在，跳过创建 ✓"
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

echo "依赖安装完成 ✓"

# 检查是否是首次安装
if [ ! -f ".installed" ]; then
    echo "首次安装，创建示例配置文件..."
    
    # 如果没有配置文件，复制示例配置
    if [ ! -f ".env" ]; then
        cp .env.development .env
        echo "已创建 .env 配置文件，请根据需要修改配置"
    fi
    
    # 标记安装完成
    touch .installed
    echo "首次安装完成 ✓"
else
    echo "更新现有安装 ✓"
fi

echo ""
echo "==================================="
echo "安装完成！"
echo ""
echo "启动服务器:"
echo "  source venv/bin/activate && python server.py"
echo ""
echo "或使用启动脚本:"
echo "  chmod +x start.sh && ./start.sh"
echo "==================================="