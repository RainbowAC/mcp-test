"""
优化版工具管理器
统一管理工具操作，简化接口
"""

import time
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

from ...database.connection import DatabaseManager
from ...database.operations import ToolOperations
from ...utils.cache import SimpleCache


class ToolManager:
    """工具管理器类"""
    
    def __init__(self, db_manager: DatabaseManager, cache_expiry: int = 300):
        """初始化工具管理器"""
        self.operations = ToolOperations(db_manager)
        self.cache = SimpleCache(expiry_time=cache_expiry)
    
    def list_all_tools(self) -> Dict[str, Any]:
        """列出所有工具"""
        cache_key = "list_all"
        
        # 检查缓存
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # 从数据库获取
        tools_dict = self.operations.get_all_tools()
        tools_list = [tool.to_dict() for tool in tools_dict.values()]
        
        result = {
            "tools": tools_list,
            "count": len(tools_list)
        }
        
        # 设置缓存
        self.cache.set(cache_key, result)
        return result
    
    def get_tool(self, name: str) -> Dict[str, Any]:
        """获取特定工具"""
        cache_key = f"get_tool:{name}"
        
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        tool = self.operations.get_tool_by_name(name)
        
        if tool:
            result = {
                "found": True,
                "tool": tool.to_dict()
            }
        else:
            result = {
                "found": False,
                "message": f"工具 '{name}' 未找到"
            }
        
        self.cache.set(cache_key, result)
        return result
    
    def add_tool(self, name: str, level: int, category: str) -> Dict[str, Any]:
        """添加新工具"""
        from ...database.models import Tool
        
        # 验证输入
        if not name or not category:
            return {"success": False, "message": "工具名称和类别不能为空"}
        
        if level < 1 or level > 10:
            return {"success": False, "message": "工具等级必须在 1-10 之间"}
        
        # 检查工具是否已存在
        existing_tool = self.operations.get_tool_by_name(name)
        if existing_tool:
            return {"success": False, "message": f"工具 '{name}' 已存在"}
        
        # 创建并添加工具
        tool = Tool(name=name, level=level, category=category)
        success = self.operations.add_tool(tool)
        
        if success:
            # 清除相关缓存
            self.cache.clear_pattern("list")
            self.cache.clear_pattern("statistics")
            
            return {
                "success": True,
                "message": f"工具 '{name}' 添加成功",
                "tool": tool.to_dict()
            }
        else:
            return {"success": False, "message": "添加工具失败"}
    
    def update_tool(self, name: str, level: Optional[int] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """更新工具"""
        # 检查工具是否存在
        existing_tool = self.operations.get_tool_by_name(name)
        if not existing_tool:
            return {"success": False, "message": f"工具 '{name}' 未找到"}
        
        # 验证等级
        if level is not None and (level < 1 or level > 10):
            return {"success": False, "message": "工具等级必须在 1-10 之间"}
        
        # 更新工具
        success = self.operations.update_tool(name, level, category)
        
        if success:
            # 清除相关缓存
            self.cache.clear_pattern(f"get_tool:{name}")
            self.cache.clear_pattern("list")
            self.cache.clear_pattern("statistics")
            
            return {"success": True, "message": f"工具 '{name}' 更新成功"}
        else:
            return {"success": False, "message": "更新工具失败"}
    
    def delete_tool(self, name: str) -> Dict[str, Any]:
        """删除工具"""
        # 检查工具是否存在
        existing_tool = self.operations.get_tool_by_name(name)
        if not existing_tool:
            return {"success": False, "message": f"工具 '{name}' 未找到"}
        
        # 删除工具
        success = self.operations.delete_tool(name)
        
        if success:
            # 清除相关缓存
            self.cache.clear_pattern(f"get_tool:{name}")
            self.cache.clear_pattern("list")
            self.cache.clear_pattern("statistics")
            
            return {"success": True, "message": f"工具 '{name}' 删除成功"}
        else:
            return {"success": False, "message": "删除工具失败"}
    
    def search_tools(self, query: str) -> Dict[str, Any]:
        """搜索工具"""
        cache_key = f"search:{query}"
        
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        tools_dict = self.operations.get_all_tools()
        
        # 简单搜索实现（可根据需要扩展）
        query_lower = query.lower()
        matching_tools = []
        
        for tool in tools_dict.values():
            if (query_lower in tool.name.lower() or 
                query_lower in tool.category.lower()):
                matching_tools.append(tool.to_dict())
        
        result = {
            "tools": matching_tools,
            "count": len(matching_tools),
            "query": query
        }
        
        self.cache.set(cache_key, result)
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取工具统计信息"""
        cache_key = "statistics"
        
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        stats = self.operations.get_statistics()
        
        self.cache.set(cache_key, stats)
        return stats
    
    def get_tools_by_category(self, category: str) -> Dict[str, Any]:
        """按类别获取工具"""
        cache_key = f"category:{category}"
        
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        tools = self.operations.get_tools_by_category(category)
        tools_list = [tool.to_dict() for tool in tools]
        
        result = {
            "tools": tools_list,
            "count": len(tools_list),
            "category": category
        }
        
        self.cache.set(cache_key, result)
        return result


def register_tool_manager_tools(mcp: FastMCP, db_manager: DatabaseManager):
    """注册工具管理器相关工具"""
    
    tool_manager = ToolManager(db_manager)
    
    @mcp.tool()
    def list_tools() -> dict:
        """列出所有工具"""
        return tool_manager.list_all_tools()
    
    @mcp.tool()
    def get_tool(name: str) -> dict:
        """获取特定工具的详细信息"""
        return tool_manager.get_tool(name)
    
    @mcp.tool()
    def add_tool(name: str, level: int, category: str) -> dict:
        """添加新工具"""
        return tool_manager.add_tool(name, level, category)
    
    @mcp.tool()
    def update_tool(name: str, level: Optional[int] = None, category: Optional[str] = None) -> dict:
        """更新工具信息"""
        return tool_manager.update_tool(name, level, category)
    
    @mcp.tool()
    def delete_tool(name: str) -> dict:
        """删除工具"""
        return tool_manager.delete_tool(name)
    
    @mcp.tool()
    def search_tools(query: str) -> dict:
        """搜索工具"""
        return tool_manager.search_tools(query)
    
    @mcp.tool()
    def get_statistics() -> dict:
        """获取工具统计信息"""
        return tool_manager.get_statistics()
    
    @mcp.tool()
    def get_tools_by_category(category: str) -> dict:
        """按类别获取工具"""
        return tool_manager.get_tools_by_category(category)