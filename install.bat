@echo off
REM MCP Platform Windows 安装脚本

echo =================================
echo MCP Development Platform 安装脚本
echo =================================

REM 检查是否已安装 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python。请先安装 Python 3.8 或更高版本。
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%a in ('python --version') do set PYTHON_VERSION=%%a
echo Python 版本: %PYTHON_VERSION%

REM 检查 Python 版本
echo Checking Python version...
for /f "tokens=1,2,3 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% lss 3 (
    echo 错误: Python 版本过低。需要 Python 3.8 或更高版本。
    pause
    exit /b 1
)

if %MAJOR% equ 3 if %MINOR% lss 8 (
    echo 错误: Python 版本过低。需要 Python 3.8 或更高版本。
    pause
    exit /b 1
)

echo Python 版本检查通过 ^! 

REM 检查是否已安装 pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 pip。请先安装 pip。
    pause
    exit /b 1
)

echo pip 已安装 ^!

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo 虚拟环境创建完成 ^!
) else (
    echo 虚拟环境已存在，跳过创建 ^!
)

REM 激活虚拟环境并安装依赖
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

REM 升级 pip
echo 升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

echo 依赖安装完成 ^!

REM 检查是否是首次安装
if not exist ".installed" (
    echo 首次安装，创建示例配置文件...
    
    REM 如果没有配置文件，复制示例配置
    if not exist ".env" (
        copy .env.development .env
        echo 已创建 .env 配置文件，请根据需要修改配置
    )
    
    REM 标记安装完成
    echo. > .installed
    echo 首次安装完成 ^!
) else (
    echo 更新现有安装 ^!
)

echo.
echo =================================
echo 安装完成^!
echo.
echo 启动服务器:
echo   venv\Scripts\activate && python server.py
echo.
echo 或使用启动脚本:
echo   start.bat
echo =================================

pause