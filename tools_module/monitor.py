"""
系统性能监控模块
提供系统性能指标收集和监控功能
"""

import time
import psutil
import logging
from typing import Dict, Any
from .database import ToolDatabase
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """性能监控类"""
    
    def __init__(self, tool_database: ToolDatabase):
        """初始化性能监控器
        
        Args:
            tool_database: 工具数据库实例，用于监控数据库连接池
        """
        self.tool_database = tool_database
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统性能指标"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }
    
    def get_database_metrics(self) -> Dict[str, Any]:
        """获取数据库性能指标"""
        try:
            pool_status = self.tool_database.get_pool_status()
            return {
                "pool_status": pool_status,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Error getting database metrics: {e}")
            return {"error": str(e), "timestamp": time.time()}
    
    def get_app_metrics(self) -> Dict[str, Any]:
        """获取应用程序指标"""
        try:
            # 获取工具总数
            from .database import ToolEntity
            with self.tool_database.get_session() as session:
                tool_count = session.query(ToolEntity).count()
            
            return {
                "total_tools": tool_count,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Error getting app metrics: {e}")
            return {"error": str(e), "timestamp": time.time()}
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """获取所有性能指标"""
        return {
            "system": self.get_system_metrics(),
            "database": self.get_database_metrics(),
            "application": self.get_app_metrics()
        }
    
    @contextmanager
    def monitor_operation(self, operation_name: str):
        """监控操作执行时间的上下文管理器
        
        Args:
            operation_name: 操作名称
        """
        start_time = time.time()
        logger.info(f"Starting operation: {operation_name}")
        
        try:
            yield
            duration = time.time() - start_time
            logger.info(f"Operation '{operation_name}' completed in {duration:.2f}s")
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Operation '{operation_name}' failed after {duration:.2f}s: {e}")
            raise