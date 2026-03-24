#!/usr/bin/env python3
"""
开发环境启动脚本
简化启动流程，专注于开发环境需求
"""

import os
import sys

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """主启动函数"""
    
    print("=" * 50)
    print("启动 MCP 工具管理服务器 (开发环境)")
    print("=" * 50)
    
    try:
        # 导入并启动服务器
        from src.core.server import main as server_main
        server_main()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"启动错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()