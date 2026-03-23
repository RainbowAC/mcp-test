# tools_module/manager.py
"""
工具管理器模块
提供工具业务逻辑处理
"""

from typing import Optional, Dict, Any
from functools import wraps
import time
from .models import Tool, ToolStatistics
from .database import ToolDatabase
from . import utils
from .monitor import PerformanceMonitor



class ToolManager:
    """工具管理器类"""
    
    def __init__(self, 
                 db_url: str = "mysql+pymysql://root:123456@localhost:3306/mcp_tools", 
                 cache_expiry: int = 300):
        """初始化工具管理器
        
        Args:
            db_url: 数据库连接URL
            cache_expiry: 缓存过期时间（秒）
        """
        self._db = ToolDatabase(db_url=db_url)
        # 初始化缓存
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_expiry = cache_expiry  # 可配置的缓存有效期
        
        # 初始化性能监控器
        self._monitor = PerformanceMonitor(self._db)
    
    def _is_cache_valid(self, key: str) -> bool:
        """检查缓存是否有效"""
        if key not in self._cache_timestamps:
            return False
        return time.time() - self._cache_timestamps[key] < self._cache_expiry
    
    def _get_from_cache(self, key: str) -> Any:
        """从缓存获取数据"""
        if self._is_cache_valid(key):
            return self._cache[key]
        return None
    
    def _set_cache(self, key: str, value: Any):
        """设置缓存数据"""
        self._cache[key] = value
        self._cache_timestamps[key] = time.time()
    
    def _invalidate_cache(self, *keys):
        """失效指定的缓存"""
        for key in keys:
            if key in self._cache:
                del self._cache[key]
            if key in self._cache_timestamps:
                del self._cache_timestamps[key]
    
    def _get_tools_list(self, tools_dict: Dict[str, Tool]) -> Dict[str, Any]:
        """辅助方法：将工具字典转换为带计数的字典"""
        tools_list = [tool.to_dict() for tool in tools_dict.values()]
        return {
            "tools": tools_list,
            "count": len(tools_list)
        }
    
    def list_all(self) -> dict:
        """
        列出所有工具
        
        Returns:
            包含工具列表和数量的字典
        """
        cache_key = "list_all"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        tools = self._db.get_all()
        result = self._get_tools_list(tools)
        self._set_cache(cache_key, result)
        return result
    
    def list_by_category(self, category: str) -> dict:
        """
        按类别列出工具
        
        Args:
            category: 类别名称
            
        Returns:
            筛选后的工具列表和数量
        """
        cache_key = f"list_by_category:{category}"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        tools = self._db.get_by_category(category)
        result = self._get_tools_list(tools)
        self._set_cache(cache_key, result)
        return result
    
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
            # 失效相关缓存
            self._invalidate_cache(
                "list_all",
                f"list_by_category:{category}", 
                "get_categories"
            )
            return utils.format_success_response(
                f"Tool '{name}' added successfully",
                data={"tool": new_tool.to_dict()}
            )
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
        # 获取原始工具信息以确定是否类别发生变化
        original_tool = self._db.get(name)
        if original_tool:
            old_category = original_tool.category
        else:
            old_category = None
        
        tool = self._db.update(name, level, category)
        
        if tool:
            # 如果类别发生了变化，需要失效旧类别和新类别的缓存
            categories_to_invalidate = [f"list_by_category:{old_category}"]
            if category and category != old_category:
                categories_to_invalidate.append(f"list_by_category:{category}")
            
            self._invalidate_cache(
                "list_all",
                "get_categories",
                *categories_to_invalidate
            )
            
            return utils.format_success_response(
                f"Tool '{name}' updated successfully",
                data={"tool": tool.to_dict()}
            )
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
        # 获取工具信息以确定类别
        tool_to_delete = self._db.get(name)
        category_to_invalidate = tool_to_delete.category if tool_to_delete else None
        
        deleted_tool = self._db.delete(name)
        
        if deleted_tool:
            # 失效相关缓存
            invalidate_keys = ["list_all"]
            if category_to_invalidate:
                invalidate_keys.append(f"list_by_category:{category_to_invalidate}")
            invalidate_keys.append("get_categories")
            
            self._invalidate_cache(*invalidate_keys)
            
            return utils.format_success_response(
                f"Tool '{name}' deleted successfully",
                data={"deleted_tool": deleted_tool.to_dict()}
            )
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
        cache_key = "get_categories"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        categories = self._db.get_categories()
        result = {
            "categories": categories,
            "count": len(categories)
        }
        self._set_cache(cache_key, result)
        return result
    
    def get_statistics(self) -> dict:
        """
        获取工具统计信息
        
        Returns:
            统计信息字典
        """
        cache_key = "get_statistics"
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        tools = self._db.get_all()
        stats = utils.calculate_statistics(tools)
        result = stats.to_dict()
        self._set_cache(cache_key, result)
        return result
    
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
        return self._get_tools_list(tools)
    
    def bulk_add_tools(self, tools_data: list) -> dict:
        """
        批量添加工具
        
        Args:
            tools_data: 工具数据列表，每个元素为{name, level, category}
            
        Returns:
            操作结果，包括成功和失败的数量
        """
        successes = []
        failures = []
        
        for tool_data in tools_data:
            name = tool_data.get("name")
            level = tool_data.get("level")
            category = tool_data.get("category")
            
            if not all([name, level is not None, category]):
                failures.append({
                    "name": name,
                    "error": "Missing required fields"
                })
                continue
            
            result = self.add_tool(name, level, category)
            if result.get("success", False):
                successes.append(result["tool"])
            else:
                failures.append({
                    "name": name,
                    "error": result.get("message", "Unknown error")
                })
        
        # 失效相关缓存
        self._invalidate_cache("list_all", "get_categories")
        
        return {
            "success": len(successes) > 0,
            "summary": {
                "added": len(successes),
                "failed": len(failures),
                "total": len(tools_data)
            },
            "successes": successes,
            "failures": failures
        }
    
    def get_tools_by_levels(self, min_level: int = None, max_level: int = None) -> dict:
        """
        根据等级范围筛选工具
        
        Args:
            min_level: 最小等级
            max_level: 最大等级
            
        Returns:
            符合条件的工具列表和数量
        """
        all_tools = self._db.get_all()
        filtered_tools = {}
        
        for key, tool in all_tools.items():
            if min_level is not None and tool.level < min_level:
                continue
            if max_level is not None and tool.level > max_level:
                continue
            filtered_tools[key] = tool
        
        return self._get_tools_list(filtered_tools)
    
    def get_performance_metrics(self) -> dict:
        """
        获取系统性能指标
        
        Returns:
            包含系统、数据库和应用性能指标的字典
        """
        return self._monitor.get_all_metrics()
    
    def monitor_operation(self, operation_name: str):
        """
        获取用于监控操作的上下文管理器
        
        Args:
            operation_name: 操作名称
            
        Returns:
            上下文管理器
        """
        return self._monitor.monitor_operation(operation_name)