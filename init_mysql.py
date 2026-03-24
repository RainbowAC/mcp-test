#!/usr/bin/env python3
"""
MySQL数据库初始化脚本
用于创建数据库和测试连接
"""

import os
import sys
from sqlalchemy import create_engine, text

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.config import config

def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    
    # 连接到MySQL服务器（不指定数据库）
    temp_url = f"mysql+pymysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/mysql"
    
    try:
        engine = create_engine(temp_url)
        
        with engine.connect() as conn:
            # 检查数据库是否存在
            result = conn.execute(
                text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{config.DATABASE_NAME}'")
            )
            
            if result.fetchone() is None:
                # 创建数据库
                conn.execute(text(f"CREATE DATABASE {config.DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                print(f"✅ 数据库 '{config.DATABASE_NAME}' 创建成功")
            else:
                print(f"✅ 数据库 '{config.DATABASE_NAME}' 已存在")
                
    except Exception as e:
        print(f"❌ 数据库创建失败: {e}")
        return False
    
    return True

def test_connection():
    """测试数据库连接"""
    
    try:
        # 使用配置中的数据库URL
        engine = create_engine(config.DATABASE_URL)
        
        with engine.connect() as conn:
            # 执行简单查询测试连接
            result = conn.execute(text("SELECT 1"))
            print("✅ MySQL数据库连接测试成功")
            return True
            
    except Exception as e:
        print(f"❌ MySQL数据库连接测试失败: {e}")
        return False

def main():
    """主函数"""
    
    print("=" * 50)
    print("MySQL数据库初始化脚本")
    print("=" * 50)
    
    print(f"数据库配置:")
    print(f"  主机: {config.DATABASE_HOST}")
    print(f"  端口: {config.DATABASE_PORT}")
    print(f"  用户: {config.DATABASE_USER}")
    print(f"  数据库: {config.DATABASE_NAME}")
    print()
    
    # 创建数据库
    if not create_database_if_not_exists():
        sys.exit(1)
    
    # 测试连接
    if not test_connection():
        sys.exit(1)
    
    print()
    print("🎉 MySQL数据库初始化完成！")
    print("现在可以运行 'python start.py' 启动服务器")

if __name__ == "__main__":
    main()