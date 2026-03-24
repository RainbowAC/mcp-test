#!/usr/bin/env python3
"""
MySQL版代码测试脚本
验证MySQL数据库连接和功能是否正常工作
"""

import os
import sys

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        from src.core.config import config
        from src.database.models import Tool
        from src.utils.cache import SimpleCache
        from src.tools.simple.calculator import SafeCalculator
        
        print("✅ 所有模块导入成功")
        assert True, "导入成功"
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        assert False, f"导入失败: {e}"

def test_config():
    """测试配置系统"""
    print("\n🧪 测试配置系统...")
    
    try:
        from src.core.config import config
        
        print(f"✅ 服务器名称: {config.SERVER_NAME}")
        print(f"✅ 服务器端口: {config.SERVER_PORT}")
        print(f"✅ 数据库主机: {config.DATABASE_HOST}")
        print(f"✅ 数据库端口: {config.DATABASE_PORT}")
        print(f"✅ 数据库名称: {config.DATABASE_NAME}")
        print(f"✅ 数据库URL: {config.DATABASE_URL}")
        print(f"✅ 调试模式: {config.DEBUG}")
        
        # 验证配置值
        assert config.SERVER_NAME == "mcp-tool-server-dev", "服务器名称配置错误"
        assert config.SERVER_PORT == 3000, "服务器端口配置错误"
        assert config.DATABASE_HOST == "localhost", "数据库主机配置错误"
        assert config.DATABASE_NAME == "mcp_dev", "数据库名称配置错误"
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        assert False, f"配置测试失败: {e}"

def test_calculator():
    """测试安全计算器"""
    print("\n🧪 测试安全计算器...")
    
    try:
        from src.tools.simple.calculator import SafeCalculator
        
        # 测试基本运算
        test_cases = [
            ("2 + 3", "5"),
            ("10 - 4", "6"),
            ("3 * 4", "12"),
            ("15 / 3", "5"),
            ("2 ** 3", "8")
        ]
        
        all_passed = True
        for expr, expected in test_cases:
            result = SafeCalculator.evaluate(expr)
            if str(result) == expected:
                print(f"✅ {expr} = {result}")
            else:
                print(f"❌ {expr} = {result} (期望: {expected})")
                all_passed = False
        
        # 测试危险表达式（应该被拒绝）
        dangerous_expr = "__import__('os').system('ls')"
        result = SafeCalculator.evaluate(dangerous_expr)
        if "错误" in str(result) or "不允许" in str(result):
            print(f"✅ 危险表达式被正确拒绝: {result}")
        else:
            print(f"❌ 危险表达式未被正确拒绝: {result}")
            all_passed = False
        
        assert all_passed, "计算器测试失败"
        
    except Exception as e:
        print(f"❌ 计算器测试失败: {e}")
        assert False, f"计算器测试失败: {e}"

def test_cache():
    """测试缓存系统"""
    print("\n🧪 测试缓存系统...")
    
    try:
        from src.utils.cache import SimpleCache
        
        cache = SimpleCache(expiry_time=1)  # 1秒过期
        
        # 测试设置和获取
        cache.set("test_key", "test_value")
        value = cache.get("test_key")
        
        if value == "test_value":
            print("✅ 缓存设置和获取正常")
        else:
            print(f"❌ 缓存获取失败: {value}")
            return False
        
        # 测试过期
        import time
        time.sleep(1.1)  # 等待过期
        expired_value = cache.get("test_key")
        
        if expired_value is None:
            print("✅ 缓存过期机制正常")
        else:
            print(f"❌ 缓存过期失败: {expired_value}")
            return False
        
        assert True, "缓存测试成功"
        
    except Exception as e:
        print(f"❌ 缓存测试失败: {e}")
        assert False, f"缓存测试失败: {e}"

def test_tool_model():
    """测试工具数据模型"""
    print("\n🧪 测试工具数据模型...")
    
    try:
        from src.database.models import Tool
        
        # 测试创建工具（带描述）
        tool = Tool(name="Python", level=5, category="Programming", 
                   description="Python programming language")
        
        # 测试转换为字典
        tool_dict = tool.to_dict()
        expected_dict = {
            "name": "Python",
            "level": 5,
            "category": "Programming",
            "description": "Python programming language"
        }
        
        if tool_dict == expected_dict:
            print("✅ 工具模型转换正常")
        else:
            print(f"❌ 工具模型转换失败: {tool_dict}")
            return False
        
        # 测试从字典创建
        tool_from_dict = Tool.from_dict(expected_dict)
        if tool_from_dict.name == "Python" and tool_from_dict.description == "Python programming language":
            print("✅ 工具模型创建正常")
        else:
            print(f"❌ 工具模型创建失败: {tool_from_dict}")
            return False
        
        assert True, "工具模型测试成功"
        
    except Exception as e:
        print(f"❌ 工具模型测试失败: {e}")
        assert False, f"工具模型测试失败: {e}"

def test_mysql_connection():
    """测试MySQL数据库连接"""
    print("\n🧪 测试MySQL数据库连接...")
    
    try:
        from src.database.connection import DatabaseManager
        from src.core.config import config
        
        # 测试数据库连接
        db_manager = DatabaseManager(config.DATABASE_URL)
        
        # 测试会话管理
        with db_manager.get_session() as session:
            # 测试查询
            from src.database.connection import ToolEntity
            count = session.query(ToolEntity).count()
            print(f"✅ MySQL数据库连接成功，工具数量: {count}")
        
        # 测试连接池状态
        pool_status = db_manager.get_pool_status()
        print(f"✅ 连接池状态: {pool_status}")
        
        assert True, "MySQL数据库连接测试成功"
        
    except Exception as e:
        print(f"❌ MySQL数据库连接测试失败: {e}")
        print("💡 提示: 请确保MySQL服务器正在运行，并且数据库已创建")
        print("💡 可以运行 'python init_mysql.py' 来初始化数据库")
        assert False, f"MySQL数据库连接测试失败: {e}"

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 MCP 工具管理服务器 - 优化版测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_calculator,
        test_cache,
        test_tool_model,
        test_mysql_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！优化版代码正常工作。")
        return True
    else:
        print("❌ 部分测试失败，请检查代码。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)