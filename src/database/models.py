"""
MySQL数据模型模块
适配MySQL数据库结构，添加描述字段
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Tool:
    """工具数据模型"""
    name: str
    level: int
    category: str
    description: Optional[str] = None
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "name": self.name,
            "level": self.level,
            "category": self.category,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Tool":
        """从字典创建工具实例"""
        return cls(**data)