# tools_module/models.py
"""
工具数据模型模块
定义工具相关的数据结构和模型
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Tool:
    """工具数据模型"""
    name: str
    level: int
    category: str
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "name": self.name,
            "level": self.level,
            "category": self.category
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Tool":
        """从字典创建工具实例"""
        return cls(
            name=data["name"],
            level=data["level"],
            category=data["category"]
        )


@dataclass
class ToolStatistics:
    """工具统计信息模型"""
    total_tools: int
    average_level: float
    by_category: dict
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "total_tools": self.total_tools,
            "average_level": self.average_level,
            "by_category": self.by_category
        }
