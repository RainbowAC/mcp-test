# tools_module/database.py
"""
工具数据库模块
提供工具数据的持久化存储和管理
"""

from typing import Dict, Optional
from .models import Tool


class ToolDatabase:
    """工具数据库类"""
    
    def __init__(self):
        """初始化工具数据库"""
        self._tools: Dict[str, Tool] = {}
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """初始化默认工具数据"""
        default_tools = [
            {"name": "Python", "level": 5, "category": "Programming"},
            {"name": "JavaScript", "level": 4, "category": "Programming"},
            {"name": "Docker", "level": 3, "category": "DevOps"},
            {"name": "Kubernetes", "level": 2, "category": "DevOps"},
        ]
        
        for tool_data in default_tools:
            tool = Tool.from_dict(tool_data)
            key = self._normalize_key(tool.name)
            self._tools[key] = tool
    
    def _normalize_key(self, name: str) -> str:
        """标准化工具名称作为键"""
        return name.lower().replace(" ", "_")
    
    def get_all(self) -> Dict[str, Tool]:
        """获取所有工具"""
        return self._tools.copy()
    
    def get(self, name: str) -> Optional[Tool]:
        """获取指定工具"""
        key = self._normalize_key(name)
        return self._tools.get(key)
    
    def add(self, tool: Tool) -> bool:
        """添加工具"""
        key = self._normalize_key(tool.name)
        if key in self._tools:
            return False
        self._tools[key] = tool
        return True
    
    def update(self, name: str, level: Optional[int] = None, category: Optional[str] = None) -> Optional[Tool]:
        """更新工具信息"""
        key = self._normalize_key(name)
        if key not in self._tools:
            return None
        
        tool = self._tools[key]
        if level is not None:
            tool.level = level
        if category is not None:
            tool.category = category
        
        return tool
    
    def delete(self, name: str) -> Optional[Tool]:
        """删除工具"""
        key = self._normalize_key(name)
        if key not in self._tools:
            return None
        return self._tools.pop(key)
    
    def get_by_category(self, category: str) -> Dict[str, Tool]:
        """按类别获取工具"""
        return {
            key: tool for key, tool in self._tools.items()
            if tool.category.lower() == category.lower()
        }
    
    def get_categories(self) -> list:
        """获取所有类别"""
        categories = set(tool.category for tool in self._tools.values())
        return sorted(list(categories))
    
    def count(self) -> int:
        """获取工具总数"""
        return len(self._tools)
    
    def clear(self):
        """清空数据库（用于测试）"""
        self._tools.clear()
        self._initialize_default_tools()
    
    def search(self, keyword: str) -> Dict[str, Tool]:
        """搜索工具"""
        if not keyword:
            return {}
        
        keyword_lower = keyword.lower()
        return {
            key: tool for key, tool in self._tools.items()
            if keyword_lower in tool.name.lower()
        }
