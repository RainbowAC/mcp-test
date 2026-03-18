# tools_module/manager.py
"""
工具管理器模块
提供工具业务逻辑处理
"""

from typing import Optional, Dict
from .models import Tool, ToolStatistics
from .database import ToolDatabase
from . import utils


class ToolManager:
    """工具管理器类"""
    
    def __init__(self):
        """初始化工具管理器"""
        self._db = ToolDatabase()
    
    def list_all(self) -> dict:
        """
        列出所有工具
        
        Returns:
            包含工具列表和数量的字典
        """
        tools = self._db.get_all()
        return {
            "tools": [tool.to_dict() for tool in tools.values()],
            "count": len(tools)
        }
    
    def list_by_category(self, category: str) -> dict:
        """
        按类别列出工具
        
        Args:
            category: 类别名称
            
        Returns:
            筛选后的工具列表和数量
        """
        tools = self._db.get_by_category(category)
        return {
            "tools": [tool.to_dict() for tool in tools.values()],
            "count": len(tools)
        }
    
    def get_tool(self, tool_name: str) -> dict:
        """
        获取指定工具的详细信息
        
        Args:
            tool_name: 工具名称
            
        Returns:
            包含工具信息的字典
        """
        tool = self._db.get(tool_name)
        
        if tool:
            return {
                "found": True,
                "tool": tool.to_dict()
            }
        else:
            return {
                "found": False,
                "message": f"Tool '{tool_name}' not found"
            }
    
    def add_tool(self, name: str, level: int, category: str) -> dict:
        """
        添加新工具
        
        Args:
            name: 工具名称
            level: 工具等级
            category: 类别
            
        Returns:
            操作结果
        """
        # 检查是否已存在
        existing_tool = self._db.get(name)
        if existing_tool:
            return utils.format_error_response(
                f"Tool '{name}' already exists",
                success=False
            )
        
        # 创建并添加新工具
        new_tool = Tool(name=name, level=level, category=category)
        success = self._db.add(new_tool)
        
        if success:
            return utils.format_success_response(
                f"Tool '{name}' added successfully",
                data={"tool": new_tool.to_dict()}
            )
        else:
            return utils.format_error_response(
                f"Failed to add tool '{name}'",
                success=False
            )
    
    def update_tool(self, name: str, level: Optional[int] = None, 
                     category: Optional[str] = None) -> dict:
        """
        更新现有工具的信息
        
        Args:
            name: 工具名称
            level: 新的等级（可选）
            category: 新的类别（可选）
            
        Returns:
            操作结果
        """
        tool = self._db.update(name, level, category)
        
        if tool:
            return utils.format_success_response(
                f"Tool '{name}' updated successfully",
                data={"tool": tool.to_dict()}
            )
        else:
            return utils.format_error_response(
                f"Tool '{name}' not found",
                success=False
            )
    
    def delete_tool(self, name: str) -> dict:
        """
        删除指定工具
        
        Args:
            name: 工具名称
            
        Returns:
            操作结果
        """
        deleted_tool = self._db.delete(name)
        
        if deleted_tool:
            return utils.format_success_response(
                f"Tool '{name}' deleted successfully",
                data={"deleted_tool": deleted_tool.to_dict()}
            )
        else:
            return utils.format_error_response(
                f"Tool '{name}' not found",
                success=False
            )
    
    def get_categories(self) -> dict:
        """
        获取所有工具类别
        
        Returns:
            类别列表和数量
        """
        categories = self._db.get_categories()
        return {
            "categories": categories,
            "count": len(categories)
        }
    
    def get_statistics(self) -> dict:
        """
        获取工具统计信息
        
        Returns:
            统计信息字典
        """
        tools = self._db.get_all()
        stats = utils.calculate_statistics(tools)
        return stats.to_dict()
    
    def get_database(self) -> ToolDatabase:
        """
        获取数据库实例（用于测试）
        
        Returns:
            ToolDatabase 实例
        """
        return self._db

    def search_tools(self, keyword: str) -> dict:
        """
        搜索工具
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            搜索结果列表和数量
        """
        tools = self._db.search(keyword)
        return {
            "tools": [tool.to_dict() for tool in tools.values()],
            "count": len(tools)
        }
