@echo off
REM MCP Platform 启动脚本
REM 用于在Windows环境下启动MCP生产服务器

setlocal

REM 检查是否提供了环境参数
if "%1"=="" (
    echo 使用方法: start.bat [environment]
    echo 环境选项: development^|production^|testing
    echo 默认环境: development
    set ENVIRONMENT=development
) else (
    set ENVIRONMENT=%1
)

REM 设置环境变量
set ENVIRONMENT=%ENVIRONMENT%
set SERVER_HOST=0.0.0.0
set SERVER_PORT=3000

REM 显示启动信息
echo ========================================
echo 启动 MCP Platform 服务器
echo 环境: %ENVIRONMENT%
echo 服务器: %SERVER_HOST%:%SERVER_PORT%
echo ========================================

REM 启动服务器
python server.py

endlocal