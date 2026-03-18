# tools_module/__init__.py
"""
Tools Module - 工具管理模块包

提供完整的工具管理功能，包括：
- 数据模型定义 (models)
- 数据库管理 (database)
- 业务逻辑处理 (manager)
- 工具函数 (utils)

使用示例:
    from tools_module import ToolManager
    
    manager = ToolManager()
    
    # 列出所有工具
    tools = manager.list_all()
    
    # 添加工具
    result = manager.add_tool("Machine Learning", 5, "AI")
    
    # 获取统计信息
    stats = manager.get_statistics()
"""

from .models import Tool, ToolStatistics
from .database import ToolDatabase
from .manager import ToolManager
from . import utils

__all__ = [
    'Tool',
    'ToolStatistics', 
    'ToolDatabase',
    'ToolManager',
    'utils'
]

__version__ = '1.0.0'
