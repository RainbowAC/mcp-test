# MCP 工具开发指南

本文档详细介绍如何在 MCP (Model Context Protocol) 服务器上开发自定义工具。

## 目录
1. [MCP 工具简介](#mcp-工具简介)
2. [工具开发基础](#工具开发基础)
3. [简单工具开发示例](#简单工具开发示例)
4. [复杂工具开发示例](#复杂工具开发示例)
5. [工具注册机制](#工具注册机制)
6. [最佳实践](#最佳实践)
7. [错误处理](#错误处理)
8. [测试工具](#测试工具)

## MCP 工具简介

MCP (Model Context Protocol) 工具是允许外部系统与 MCP 服务器交互的功能组件。这些工具可以执行各种任务，如计算、数据检索、系统监控等。

### 工具类型
- **简单工具**: 不依赖外部资源的独立功能
- **复杂工具**: 依赖数据库、文件系统或其他外部资源的工具

## 工具开发基础

### 工具结构
每个 MCP 工具通常包含以下几个部分：

1. **导入必要的库**
2. **定义注册函数**
3. **创建工具装饰器**
4. **实现工具逻辑**

### 基础工具模板

```python
# tools/my_tool.py
from mcp.server.fastmcp import FastMCP

def register_my_tool(mcp: FastMCP):
    """注册我的工具到 MCP 服务器"""

    @mcp.tool()
    def my_tool(param1: str, param2: int) -> dict:
        """
        我的工具描述
        
        Args:
            param1: 参数1的描述
            param2: 参数2的描述
            
        Returns:
            工具执行结果
        """
        # 工具逻辑
        result = {
            "param1": param1,
            "param2": param2,
            "message": "工具执行成功"
        }
        return result
```

## 简单工具开发示例

### Echo 工具
这是最简单的工具示例，直接返回输入的参数：

```python
# tools/echo.py
from mcp.server.fastmcp import FastMCP

def register_echo_tool(mcp: FastMCP):
    """注册 Echo 工具"""

    @mcp.tool()
    def echo(message: str) -> str:
        """回显输入的消息"""
        return f"Echo: {message}"
```

### 计算工具
执行基本数学运算的工具：

```python
# tools/calculate.py
from mcp.server.fastmcp import FastMCP

def register_calculate_tool(mcp: FastMCP):
    """注册计算工具"""

    @mcp.tool()
    def calculate(expression: str) -> str:
        """执行基本数学计算"""
        try:
            # 安全计算表达式（限制内置函数）
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
```

### 时间工具
获取当前时间信息：

```python
# tools/time_info.py
from mcp.server.fastmcp import FastMCP
from datetime import datetime

def register_time_info_tool(mcp: FastMCP):
    """注册时间信息工具"""

    @mcp.tool()
    def get_current_time(format_type: str = "iso") -> str:
        """
        获取当前时间
        
        Args:
            format_type: 时间格式 ("iso", "date", "time", "timestamp")
        """
        now = datetime.now()
        
        if format_type == "iso":
            return now.isoformat()
        elif format_type == "date":
            return now.strftime("%Y-%m-%d")
        elif format_type == "time":
            return now.strftime("%H:%M:%S")
        elif format_type == "timestamp":
            return str(now.timestamp())
        else:
            return now.isoformat()
```

## 复杂工具开发示例

复杂工具通常需要访问数据库、文件系统或其他外部资源。

### 数据库工具示例

```python
# tools/database_operations.py
from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_database_operations_tool(mcp: FastMCP, tool_manager: ToolManager):
    """注册数据库操作工具"""

    @mcp.tool()
    def add_tool_to_system(name: str, level: int, category: str) -> dict:
        """
        向系统添加新工具
        
        Args:
            name: 工具名称
            level: 工具等级 (1-10)
            category: 工具分类
            
        Returns:
            包含操作结果的字典
        """
        try:
            result = tool_manager.add_tool(name, level, category)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "添加工具失败"
            }

    @mcp.tool()
    def search_tools_by_category(category: str) -> dict:
        """
        按类别搜索工具
        
        Args:
            category: 工具类别
            
        Returns:
            包含匹配工具的字典
        """
        try:
            return tool_manager.list_by_category(category)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "搜索工具失败"
            }
```

### 文件操作工具示例

```python
# tools/file_operations.py
import os
from mcp.server.fastmcp import FastMCP

def register_file_operations_tool(mcp: FastMCP):
    """注册文件操作工具"""
    
    @mcp.tool()
    def read_file(file_path: str) -> dict:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含文件内容的字典
        """
        try:
            # 安全检查：确保路径在允许的范围内
            base_dir = os.path.abspath(".")  # 当前工作目录
            abs_path = os.path.abspath(file_path)
            
            if not abs_path.startswith(base_dir):
                return {
                    "success": False,
                    "error": "Access denied: Path outside allowed directory",
                    "content": None
                }
            
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "size": len(content)
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "content": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": None
            }

    @mcp.tool()
    def list_directory(directory_path: str = ".") -> dict:
        """
        列出目录内容
        
        Args:
            directory_path: 目录路径，默认为当前目录
            
        Returns:
            包含目录内容的字典
        """
        try:
            base_dir = os.path.abspath(".")
            abs_path = os.path.abspath(directory_path)
            
            if not abs_path.startswith(base_dir):
                return {
                    "success": False,
                    "error": "Access denied: Path outside allowed directory",
                    "files": []
                }
            
            items = os.listdir(abs_path)
            files = []
            directories = []
            
            for item in items:
                item_path = os.path.join(abs_path, item)
                if os.path.isfile(item_path):
                    files.append(item)
                elif os.path.isdir(item_path):
                    directories.append(item)
            
            return {
                "success": True,
                "directory": abs_path,
                "files": files,
                "directories": directories,
                "total_items": len(items)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "files": [],
                "directories": []
            }
```

### 系统监控工具示例

```python
# tools/system_monitor.py
import psutil
from mcp.server.fastmcp import FastMCP

def register_system_monitor_tool(mcp: FastMCP):
    """注册系统监控工具"""

    @mcp.tool()
    def get_system_info() -> dict:
        """获取系统信息"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory_total": memory_info.total,
            "memory_available": memory_info.available,
            "memory_percent": memory_info.percent,
            "disk_total": disk_info.total,
            "disk_used": disk_info.used,
            "disk_free": disk_info.free,
            "disk_percent": (disk_info.used / disk_info.total) * 100
        }

    @mcp.tool()
    def get_network_stats() -> dict:
        """获取网络统计信息"""
        net_io = psutil.net_io_counters()
        
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "errin": net_io.errin,
            "errout": net_io.errout,
            "dropin": net_io.dropin,
            "dropout": net_io.dropout
        }
```

## 工具注册机制

### 注册流程

1. **创建工具文件**: 在 `tools/` 目录下创建新的工具文件
2. **定义注册函数**: 实现接受 `mcp` 和可能的其他参数的注册函数
3. **使用装饰器**: 使用 `@mcp.tool()` 装饰器标记工具函数
4. **更新注册器**: 将新工具添加到 `tools/registry.py`

### 更新注册器示例

```python
# 在 tools/registry.py 中添加新工具
from . import (
    echo,
    calculate,
    list_tools,
    add_tool,
    # ... 其他工具
    time_info,        # 新增时间工具
    file_operations,  # 新增文件操作工具
    system_monitor    # 新增系统监控工具
)

def register_all_tools(mcp: FastMCP, tool_manager: ToolManager):
    # 注册简单工具
    echo.register_echo_tool(mcp)
    calculate.register_calculate_tool(mcp)
    time_info.register_time_info_tool(mcp)  # 注册时间工具

    # 注册复杂工具
    list_tools.register_list_tools_tool(mcp, tool_manager)
    add_tool.register_add_tool_tool(mcp, tool_manager)
    file_operations.register_file_operations_tool(mcp)  # 注册文件操作工具
    system_monitor.register_system_monitor_tool(mcp)    # 注册系统监控工具
```

## 最佳实践

### 1. 类型注解
始终为工具函数和参数添加类型注解：

```python
@mcp.tool()
def my_tool(input_param: str, number_param: int) -> dict:
    # 函数实现
    pass
```

### 2. 文档字符串
为每个工具函数添加清晰的文档字符串：

```python
@mcp.tool()
def my_tool(input_param: str, number_param: int) -> dict:
    """
    工具功能描述
    
    Args:
        input_param: 输入参数描述
        number_param: 数字参数描述
        
    Returns:
        结果描述
    """
    # 函数实现
    pass
```

### 3. 错误处理
实现适当的错误处理：

```python
@mcp.tool()
def my_tool(input_param: str) -> dict:
    try:
        # 执行工具逻辑
        result = process_input(input_param)
        return {"success": True, "result": result}
    except ValueError as e:
        return {"success": False, "error": f"Invalid input: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
```

### 4. 安全考虑
对于文件操作等敏感操作，实施安全检查：

```python
def validate_path(user_path: str) -> bool:
    """验证用户提供的路径是否安全"""
    base_dir = os.path.abspath(".")  # 基础目录
    abs_path = os.path.abspath(user_path)
    return abs_path.startswith(base_dir)

@mcp.tool()
def read_file_safely(file_path: str) -> dict:
    if not validate_path(file_path):
        return {"success": False, "error": "Unsafe path provided"}
    
    # 安全地处理文件
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## 错误处理

### 常见错误类型
- **输入验证错误**: 用户输入不符合预期格式
- **资源访问错误**: 数据库连接失败、文件不存在等
- **系统错误**: 内存不足、权限不足等

### 错误响应格式
统一的错误响应格式有助于客户端处理错误：

```python
def format_error_response(error_msg: str, details: str = None) -> dict:
    """格式化错误响应"""
    response = {
        "success": False,
        "error": error_msg
    }
    if details:
        response["details"] = details
    return response

@mcp.tool()
def my_tool(input_param: str) -> dict:
    if not input_param:
        return format_error_response("Input parameter is required")
    
    try:
        result = process_input(input_param)
        return {"success": True, "result": result}
    except Exception as e:
        return format_error_response(
            "An error occurred processing your request",
            str(e)
        )
```

## 测试工具

### 单元测试示例

```python
# tests/test_my_tool.py
import unittest
from tools.my_tool import register_my_tool
from mcp.server.fastmcp import FastMCP

class TestMyTool(unittest.TestCase):
    def setUp(self):
        self.mcp = FastMCP("test-server")
        register_my_tool(self.mcp)
    
    def test_my_tool_basic_functionality(self):
        # 测试工具的基本功能
        # 注意：具体的测试方法取决于 MCP 框架的测试设施
        pass
    
    def test_my_tool_with_invalid_input(self):
        # 测试工具对无效输入的处理
        pass
```

### 集成测试示例

```python
# tests/integration_test.py
import requests
import unittest
from server import mcp  # 假设服务器已启动

class TestMCPIntegration(unittest.TestCase):
    def test_echo_tool_integration(self):
        """测试 Echo 工具集成"""
        # 这里需要实际的服务器端点来测试
        pass
    
    def test_calculate_tool_integration(self):
        """测试计算工具集成"""
        # 这里需要实际的服务器端点来测试
        pass
```

## 高级主题

### 工具组合
可以创建组合多个工具的高级工具：

```python
# tools/advanced_operations.py
from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_advanced_operations_tool(mcp: FastMCP, tool_manager: ToolManager):
    @mcp.tool()
    def advanced_analysis(tool_name: str) -> dict:
        """
        对指定工具进行高级分析
        
        Args:
            tool_name: 要分析的工具名称
            
        Returns:
            包含分析结果的字典
        """
        # 获取工具信息
        tool_info = tool_manager.get_tool(tool_name)
        
        if not tool_info.get('found'):
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        # 执行更复杂的分析逻辑
        analysis_result = {
            "tool": tool_info['tool'],
            "recommendations": [],
            "related_tools": []
        }
        
        # 添加分析逻辑...
        
        return {
            "success": True,
            "analysis": analysis_result
        }
```

### 异步工具
如果需要长时间运行的操作，可以使用异步工具：

```python
import asyncio
from mcp.server.fastmcp import FastMCP

def register_async_tool(mcp: FastMCP):
    @mcp.tool()
    async def long_running_task(task_id: str) -> dict:
        """
        模拟长时间运行的任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务执行结果
        """
        # 模拟耗时操作
        await asyncio.sleep(2)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "duration": "2 seconds"
        }
```

---

这份指南涵盖了MCP工具开发的各个方面，从基础概念到高级主题。按照这些指导原则，您可以开发出功能强大且安全的MCP工具。