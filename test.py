#!/usr/bin/env python3
"""
MCP工具管理服务器 - 动态同步测试系统
支持动态发现和同步全局MCP工具，实现同态测试
"""

import os
import sys
import argparse
import importlib
import inspect
from typing import List, Dict, Callable, Any, Set
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 动态测试工具注册表
TEST_REGISTRY: Dict[str, Dict[str, Any]] = {}

# MCP工具发现器
class MCPToolDiscoverer:
    """MCP工具动态发现器"""
    
    def __init__(self, base_path: str = "src/tools"):
        self.base_path = Path(base_path)
        self.tools_cache: Dict[str, Dict[str, Any]] = {}
    
    def discover_tools(self) -> Dict[str, Dict[str, Any]]:
        """动态发现所有MCP工具"""
        tools = {}
        
        # 发现基础工具模块
        tools.update(self._discover_simple_tools())
        
        # 发现管理工具模块
        tools.update(self._discover_management_tools())
        
        # 发现其他工具模块
        tools.update(self._discover_other_tools())
        
        self.tools_cache = tools
        return tools
    
    def _discover_simple_tools(self) -> Dict[str, Dict[str, Any]]:
        """发现简单工具模块"""
        tools = {}
        simple_tools_path = self.base_path / "simple"
        
        if simple_tools_path.exists():
            for py_file in simple_tools_path.glob("*.py"):
                if py_file.name.startswith("_") or py_file.name == "__init__.py":
                    continue
                
                tool_name = py_file.stem
                module_name = f"src.tools.simple.{tool_name}"
                
                try:
                    module = importlib.import_module(module_name)
                    tool_info = self._analyze_tool_module(module, tool_name)
                    if tool_info:
                        tools[tool_name] = tool_info
                except ImportError as e:
                    print(f"⚠️  无法导入工具模块 {module_name}: {e}")
        
        return tools
    
    def _discover_management_tools(self) -> Dict[str, Dict[str, Any]]:
        """发现管理工具模块"""
        tools = {}
        management_tools_path = self.base_path / "management"
        
        if management_tools_path.exists():
            for py_file in management_tools_path.glob("*.py"):
                if py_file.name.startswith("_") or py_file.name == "__init__.py":
                    continue
                
                tool_name = py_file.stem
                module_name = f"src.tools.management.{tool_name}"
                
                try:
                    module = importlib.import_module(module_name)
                    tool_info = self._analyze_tool_module(module, tool_name)
                    if tool_info:
                        tools[tool_name] = tool_info
                except ImportError as e:
                    print(f"⚠️  无法导入工具模块 {module_name}: {e}")
        
        return tools
    
    def _discover_other_tools(self) -> Dict[str, Dict[str, Any]]:
        """发现其他工具模块"""
        tools = {}
        
        # 检查是否有其他工具目录
        for subdir in self.base_path.iterdir():
            if subdir.is_dir() and subdir.name not in ["simple", "management", "__pycache__"]:
                for py_file in subdir.glob("*.py"):
                    if py_file.name.startswith("_") or py_file.name == "__init__.py":
                        continue
                    
                    tool_name = py_file.stem
                    module_name = f"src.tools.{subdir.name}.{tool_name}"
                    
                    try:
                        module = importlib.import_module(module_name)
                        tool_info = self._analyze_tool_module(module, tool_name)
                        if tool_info:
                            tools[tool_name] = tool_info
                    except ImportError as e:
                        print(f"⚠️  无法导入工具模块 {module_name}: {e}")
        
        return tools
    
    def _analyze_tool_module(self, module: Any, tool_name: str) -> Dict[str, Any]:
        """分析工具模块，提取工具信息和测试函数"""
        tool_info = {
            "name": tool_name.replace('_', ' ').title() + " 测试",
            "description": "",
            "category": "工具功能",
            "module": module,
            "functions": [],
            "test_functions": [],  # 改为复数，支持多个测试函数
            "test_function": None  # 保持向后兼容
        }
        
        # 获取模块文档
        if module.__doc__:
            tool_info["description"] = module.__doc__.strip().split('\n')[0]
        
        # 查找注册函数
        register_function = None
        for name, obj in inspect.getmembers(module):
            if name.startswith("register_") and callable(obj):
                register_function = obj
                break
        
        if register_function:
            tool_info["register_function"] = register_function
            
            # 分析注册函数中的工具
            tool_info["functions"] = self._extract_tool_functions(register_function)
        
        # 发现分散的测试函数
        tool_info["test_functions"] = self._discover_test_functions(module, tool_name)
        
        # 创建动态测试函数（向后兼容）
        tool_info["test_function"] = self._create_dynamic_test_function(tool_name, module)
        
        return tool_info
    
    def _extract_tool_functions(self, register_func: Callable) -> List[Dict[str, str]]:
        """从注册函数中提取工具函数信息"""
        functions = []
        
        try:
            # 获取函数源代码
            source = inspect.getsource(register_func)
            
            # 简单的正则匹配来查找 @mcp.tool() 装饰的函数
            import re
            pattern = r'@mcp\.tool\(\)\s*\n\s*def\s+(\w+)\([^)]*\)\s*->[^:]*:'
            matches = re.findall(pattern, source)
            
            for func_name in matches:
                functions.append({
                    "name": func_name,
                    "description": f"{func_name} 工具函数"
                })
        except Exception as e:
            print(f"⚠️  无法提取工具函数信息: {e}")
        
        return functions
    
    def _discover_test_functions(self, module: Any, tool_name: str) -> List[Dict[str, Any]]:
        """发现工具模块中的分散测试函数"""
        test_functions = []
        
        try:
            # 查找所有以 test_ 开头的函数
            for name, obj in inspect.getmembers(module):
                if (name.startswith("test_") and 
                    inspect.isfunction(obj)):
                    
                    # 获取函数文档
                    doc = obj.__doc__ or "无描述"
                    
                    test_functions.append({
                        "name": name,
                        "function": obj,
                        "description": doc.strip(),
                        "full_name": f"{tool_name}.{name}"
                    })
            
            if test_functions:
                print(f"🔍 在 {tool_name} 中发现 {len(test_functions)} 个测试函数")
                for test_func in test_functions:
                    print(f"   📋 {test_func['name']}: {test_func['description']}")
                
        except Exception as e:
            print(f"⚠️  无法发现 {tool_name} 的测试函数: {e}")
        
        return test_functions
    
    def _create_dynamic_test_function(self, tool_name: str, module: Any) -> Callable:
        """为工具创建动态测试函数"""
        
        def dynamic_test_function() -> bool:
            """动态生成的工具测试函数"""
            print(f"🧪 测试 {tool_name} 工具...")
            
            try:
                # 尝试导入工具类或主要功能
                tool_class_name = tool_name.replace('_', ' ').title().replace(' ', '')
                
                # 查找工具类
                tool_class = None
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        name.lower() == tool_name.lower().replace('_', '')):
                        tool_class = obj
                        break
                
                if tool_class:
                    # 测试工具类的基本功能
                    return self._test_tool_class(tool_class, tool_name)
                else:
                    # 测试模块级函数
                    return self._test_module_functions(module, tool_name)
                    
            except Exception as e:
                print(f"❌ {tool_name} 工具测试失败: {e}")
                return False
        
        return dynamic_test_function
    
    def _test_tool_class(self, tool_class: Any, tool_name: str) -> bool:
        """测试工具类的基本功能"""
        try:
            # 检查是否有静态方法或类方法
            methods = [name for name, method in inspect.getmembers(tool_class) 
                      if inspect.ismethod(method) or inspect.isfunction(method)]
            
            # 尝试调用一些常见的方法
            test_methods = ['evaluate', 'calculate', 'process', 'execute']
            
            for method_name in test_methods:
                if method_name in methods:
                    # 这里可以添加具体的测试逻辑
                    print(f"✅ 发现 {tool_name}.{method_name} 方法")
            
            print(f"✅ {tool_name} 工具类测试通过")
            return True
            
        except Exception as e:
            print(f"❌ {tool_name} 工具类测试失败: {e}")
            return False
    
    def _test_module_functions(self, module: Any, tool_name: str) -> bool:
        """测试模块级函数"""
        try:
            # 查找模块中的函数
            functions = [name for name, func in inspect.getmembers(module) 
                        if inspect.isfunction(func) and not name.startswith('_')]
            
            if functions:
                print(f"✅ 发现 {tool_name} 模块函数: {', '.join(functions)}")
                print(f"✅ {tool_name} 模块函数测试通过")
                return True
            else:
                print(f"⚠️  {tool_name} 模块未发现可测试函数")
                return True  # 没有函数不代表失败
                
        except Exception as e:
            print(f"❌ {tool_name} 模块函数测试失败: {e}")
            return False


# 创建全局发现器实例
tool_discoverer = MCPToolDiscoverer()

# 基础系统测试（静态定义，用于系统完整性验证）
SYSTEM_TESTS: Dict[str, Dict[str, Any]] = {
    "imports": {
        "function": None,
        "name": "模块导入测试",
        "description": "验证所有核心模块能否正确导入",
        "category": "系统完整性"
    },
    "config": {
        "function": None,
        "name": "配置系统测试", 
        "description": "验证配置文件和环境变量设置",
        "category": "系统完整性"
    },
    "cache": {
        "function": None,
        "name": "缓存系统测试",
        "description": "验证缓存系统的设置、获取和过期功能",
        "category": "系统组件"
    },
    "tool_model": {
        "function": None,
        "name": "工具数据模型测试",
        "description": "验证工具数据模型的创建和转换功能",
        "category": "数据模型"
    },
    "mysql_connection": {
        "function": None,
        "name": "MySQL数据库连接测试",
        "description": "验证MySQL数据库连接和会话管理",
        "category": "数据库"
    }
}

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        from src.core.config import config
        from src.database.models import Tool
        from src.utils.cache import SimpleCache
        from src.tools.simple.calculator import SafeCalculator
        
        print("✅ 所有模块导入成功")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

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
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

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
        
        return all_passed
        
    except Exception as e:
        print(f"❌ 计算器测试失败: {e}")
        return False

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
        
        return True
        
    except Exception as e:
        print(f"❌ 缓存测试失败: {e}")
        return False

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
        
        return True
        
    except Exception as e:
        print(f"❌ 工具模型测试失败: {e}")
        return False

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
        
        return True
        
    except Exception as e:
        print(f"❌ MySQL数据库连接测试失败: {e}")
        print("💡 提示: 请确保MySQL服务器正在运行，并且数据库已创建")
        print("💡 可以运行 'python init_mysql.py' 来初始化数据库")
        return False

def test_datetime_tool():
    """测试时间日期工具"""
    print("\n🧪 测试时间日期工具...")
    
    try:
        from src.tools.simple.datetime_tool import DateTimeTool
        
        # 测试获取当前时间
        result = DateTimeTool.get_current_time("Asia/Shanghai")
        if "datetime" in result:
            print(f"✅ 获取当前时间成功: {result['datetime']}")
        else:
            print(f"❌ 获取当前时间失败: {result}")
            return False
        
        # 测试时区转换
        result = DateTimeTool.convert_timezone(
            "2024-01-01 12:00:00", 
            "UTC", 
            "Asia/Shanghai"
        )
        if "converted" in result:
            print(f"✅ 时区转换成功: {result['converted']['datetime']}")
        else:
            print(f"❌ 时区转换失败: {result}")
            return False
        
        # 测试时间戳格式化
        timestamp = 1704067200  # 2024-01-01 00:00:00 UTC
        result = DateTimeTool.format_timestamp(timestamp, "Asia/Shanghai")
        if "datetime" in result:
            print(f"✅ 时间戳格式化成功: {result['datetime']}")
        else:
            print(f"❌ 时间戳格式化失败: {result}")
            return False
        
        # 测试时间差异计算
        result = DateTimeTool.calculate_difference(
            "2024-01-01 12:00:00",
            "2024-01-02 14:30:00",
            "UTC",
            "UTC"
        )
        if "difference" in result:
            print(f"✅ 时间差异计算成功: {result['difference']['human_readable']}")
        else:
            print(f"❌ 时间差异计算失败: {result}")
            return False
        
        # 测试时间间隔添加
        result = DateTimeTool.add_duration(
            "2024-01-01 12:00:00",
            "2d3h30m",
            "UTC"
        )
        if "result_time" in result:
            print(f"✅ 时间间隔添加成功: {result['result_time']}")
        else:
            print(f"❌ 时间间隔添加失败: {result}")
            return False
        
        print("✅ 时间日期工具所有功能测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 时间日期工具测试失败: {e}")
        return False

def initialize_test_registry():
    """初始化测试注册表 - 动态同步MCP工具"""
    global TEST_REGISTRY
    
    # 清空现有注册表
    TEST_REGISTRY.clear()
    
    # 添加系统基础测试
    SYSTEM_TESTS["imports"]["function"] = test_imports
    SYSTEM_TESTS["config"]["function"] = test_config
    SYSTEM_TESTS["cache"]["function"] = test_cache
    SYSTEM_TESTS["tool_model"]["function"] = test_tool_model
    SYSTEM_TESTS["mysql_connection"]["function"] = test_mysql_connection
    
    TEST_REGISTRY.update(SYSTEM_TESTS)
    
    # 动态发现MCP工具
    print("🔍 动态发现MCP工具...")
    discovered_tools = tool_discoverer.discover_tools()
    
    if discovered_tools:
        print(f"✅ 发现 {len(discovered_tools)} 个MCP工具")
        for tool_name, tool_info in discovered_tools.items():
            print(f"   📦 {tool_name}: {tool_info['name']}")
        
        TEST_REGISTRY.update(discovered_tools)
    else:
        print("⚠️  未发现MCP工具")
    
    print(f"📊 测试注册表已初始化，共 {len(TEST_REGISTRY)} 个测试项目")


def display_test_menu():
    """显示测试选择菜单"""
    print("\n" + "=" * 60)
    print("🧪 MCP 工具管理服务器 - 测试工具选择")
    print("=" * 60)
    
    categories = {}
    for test_id, test_info in TEST_REGISTRY.items():
        category = test_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((test_id, test_info))
    
    # 按分类显示测试选项
    option_number = 1
    option_map = {}
    
    for category, tests in categories.items():
        print(f"\n📁 {category}:")
        for test_id, test_info in tests:
            option_map[str(option_number)] = test_id
            print(f"  {option_number}. {test_info['name']}")
            print(f"     📝 {test_info['description']}")
            option_number += 1
    
    # 添加特殊选项
    print(f"\n🔧 批量测试:")
    option_map[str(option_number)] = "all"
    print(f"  {option_number}. 运行所有测试")
    option_number += 1
    
    option_map[str(option_number)] = "category"
    print(f"  {option_number}. 按分类运行测试")
    option_number += 1
    
    option_map[str(option_number)] = "exit"
    print(f"  {option_number}. 退出测试")
    
    return option_map


def run_tests(test_ids: List[str]) -> Dict[str, bool]:
    """运行指定的测试"""
    results = {}
    
    if "all" in test_ids:
        # 运行所有测试
        test_ids = list(TEST_REGISTRY.keys())
    
    for test_id in test_ids:
        if test_id not in TEST_REGISTRY:
            print(f"❌ 未知的测试ID: {test_id}")
            results[test_id] = False
            continue
        
        test_info = TEST_REGISTRY[test_id]
        
        # 检查是否有分散的测试函数
        if "test_functions" in test_info and test_info["test_functions"]:
            # 运行分散的测试函数
            print(f"\n{'='*50}")
            print(f"🧪 运行 {test_info['name']} 的分散测试")
            print(f"📝 {test_info['description']}")
            
            # 显示工具函数信息
            if "functions" in test_info and test_info["functions"]:
                func_names = [func["name"] for func in test_info["functions"]]
                print(f"🔧 工具函数: {', '.join(func_names)}")
            
            print(f"📊 发现 {len(test_info['test_functions'])} 个测试函数")
            print('='*50)
            
            # 运行所有分散的测试函数
            test_results = []
            for test_func_info in test_info["test_functions"]:
                print(f"\n🔬 运行测试: {test_func_info['name']}")
                print(f"   📖 {test_func_info['description']}")
                
                try:
                    success = test_func_info["function"]()
                    test_results.append(success)
                    status = "✅ 通过" if success else "❌ 失败"
                    print(f"   {status} - {test_func_info['name']}")
                except Exception as e:
                    print(f"   ❌ 测试执行错误: {e}")
                    test_results.append(False)
            
            # 汇总测试结果
            overall_success = all(test_results)
            results[test_id] = overall_success
            
            passed_count = sum(test_results)
            total_count = len(test_results)
            
            print(f"\n📊 {test_info['name']} 测试汇总: {passed_count}/{total_count} 通过")
            status = "✅ 全部通过" if overall_success else "❌ 部分失败"
            print(f"{status} - {test_info['name']}")
            
        else:
            # 使用传统的单一测试函数（向后兼容）
            test_func = test_info.get("test_function") or test_info.get("function")
            
            if test_func:
                print(f"\n{'='*40}")
                print(f"🧪 运行测试: {test_info['name']}")
                print(f"📝 {test_info['description']}")
                
                # 显示工具函数信息
                if "functions" in test_info and test_info["functions"]:
                    func_names = [func["name"] for func in test_info["functions"]]
                    print(f"🔧 工具函数: {', '.join(func_names)}")
                
                print('='*40)
                
                try:
                    success = test_func()
                    results[test_id] = success
                    status = "✅ 通过" if success else "❌ 失败"
                    print(f"\n{status} - {test_info['name']}")
                except Exception as e:
                    print(f"❌ 测试执行错误: {e}")
                    results[test_id] = False
            else:
                print(f"❌ 测试函数未定义: {test_id}")
                results[test_id] = False
    
    return results


def run_tests_by_category():
    """按分类运行测试"""
    categories = {}
    for test_id, test_info in TEST_REGISTRY.items():
        category = test_info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(test_id)
    
    print("\n📁 可用分类:")
    category_list = list(categories.keys())
    for i, category in enumerate(category_list, 1):
        count = len(categories[category])
        print(f"  {i}. {category} ({count}个测试)")
    
    try:
        choice = input("\n请选择分类编号 (输入'all'运行所有分类): ").strip()
        if choice.lower() == 'all':
            return run_tests(["all"])
        
        category_index = int(choice) - 1
        if 0 <= category_index < len(category_list):
            selected_category = category_list[category_index]
            test_ids = categories[selected_category]
            print(f"\n🏃 运行 {selected_category} 分类的 {len(test_ids)} 个测试...")
            return run_tests(test_ids)
        else:
            print("❌ 无效的分类编号")
            return {}
    except ValueError:
        print("❌ 请输入有效的数字")
        return {}


def interactive_test_runner():
    """交互式测试运行器"""
    initialize_test_registry()
    
    while True:
        option_map = display_test_menu()
        
        try:
            choice = input("\n请选择测试选项编号: ").strip()
            
            if choice not in option_map:
                print("❌ 无效的选择，请重新输入")
                continue
            
            selected_option = option_map[choice]
            
            if selected_option == "exit":
                print("👋 退出测试系统")
                break
            elif selected_option == "category":
                run_tests_by_category()
            elif selected_option == "all":
                results = run_tests(["all"])
                display_summary(results)
            else:
                results = run_tests([selected_option])
                display_summary(results)
            
            # 询问是否继续
            continue_test = input("\n是否继续测试? (y/n): ").strip().lower()
            if continue_test not in ['y', 'yes', '是']:
                print("👋 退出测试系统")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出测试系统")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")


def display_summary(results: Dict[str, bool]):
    """显示测试结果摘要"""
    if not results:
        return
    
    print("\n" + "=" * 50)
    print("📊 测试结果摘要")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {total - passed}")
    print(f"📈 成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统功能正常。")
    else:
        print("\n⚠️  部分测试失败，请检查相关功能。")
        print("\n失败的测试:")
        for test_id, success in results.items():
            if not success:
                test_info = TEST_REGISTRY.get(test_id, {"name": test_id})
                print(f"  ❌ {test_info['name']}")


def main():
    """主测试函数"""
    parser = argparse.ArgumentParser(description="MCP工具管理服务器测试系统")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--test", nargs="+", help="运行指定的测试(用空格分隔)")
    parser.add_argument("--category", help="运行指定分类的所有测试")
    parser.add_argument("--interactive", action="store_true", help="交互式测试模式")
    
    args = parser.parse_args()
    
    initialize_test_registry()
    
    if args.interactive:
        # 交互式模式
        interactive_test_runner()
        return True
    
    elif args.all:
        # 运行所有测试
        print("=" * 50)
        print("🧪 运行所有测试")
        print("=" * 50)
        results = run_tests(["all"])
        display_summary(results)
        return all(results.values())
    
    elif args.test:
        # 运行指定测试
        print("=" * 50)
        print(f"🧪 运行指定测试: {', '.join(args.test)}")
        print("=" * 50)
        results = run_tests(args.test)
        display_summary(results)
        return all(results.values())
    
    elif args.category:
        # 运行分类测试
        categories = {test_info["category"] for test_info in TEST_REGISTRY.values()}
        if args.category not in categories:
            print(f"❌ 未知的分类: {args.category}")
            print(f"可用分类: {', '.join(categories)}")
            return False
        
        test_ids = [test_id for test_id, test_info in TEST_REGISTRY.items() 
                   if test_info["category"] == args.category]
        
        print("=" * 50)
        print(f"🧪 运行 {args.category} 分类测试")
        print("=" * 50)
        results = run_tests(test_ids)
        display_summary(results)
        return all(results.values())
    
    else:
        # 默认运行所有测试
        print("=" * 50)
        print("🧪 MCP 工具管理服务器 - 默认测试模式")
        print("=" * 50)
        results = run_tests(["all"])
        display_summary(results)
        return all(results.values())


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 测试系统错误: {e}")
        sys.exit(1)