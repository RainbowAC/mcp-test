"""
优化版性能监控模块
增强监控功能，添加数据库连接池监控
"""

import time
import psutil
from typing import Dict, Any, Optional
from contextlib import contextmanager
import logging
from sqlalchemy import inspect

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """性能监控类 - 增强版本"""
    
    def __init__(self, db_engine=None):
        """初始化性能监控器"""
        self._start_time = time.time()
        self.db_engine = db_engine
        self._operation_stats = {
            'total_operations': 0,
            'failed_operations': 0,
            'slow_operations': 0
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统性能指标"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage_percent": psutil.disk_usage('/').percent,
                "uptime": time.time() - self._start_time,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {"error": str(e), "timestamp": time.time()}
    
    def get_database_metrics(self) -> Dict[str, Any]:
        """获取数据库连接池指标"""
        if not self.db_engine:
            return {"error": "Database engine not available"}
        
        try:
            pool = self.db_engine.pool
            return {
                "pool_size": pool.size(),
                "checked_out": pool.checkedout(),
                "checked_in": pool.checkedin(),
                "overflow": pool.overflow(),
                "connections": pool.status()
            }
        except Exception as e:
            logger.error(f"Error getting database metrics: {e}")
            return {"error": str(e)}
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """获取所有性能指标"""
        return {
            "system": self.get_system_metrics(),
            "database": self.get_database_metrics(),
            "operations": self._operation_stats.copy(),
            "uptime": time.time() - self._start_time,
            "timestamp": time.time()
        }
    
    @contextmanager
    def monitor_operation(self, operation_name: str, slow_threshold: float = 1.0):
        """监控操作执行时间的上下文管理器
        
        Args:
            operation_name: 操作名称
            slow_threshold: 慢操作阈值（秒）
        """
        start_time = time.time()
        self._operation_stats['total_operations'] += 1
        
        try:
            yield
            duration = time.time() - start_time
            
            # 记录操作统计
            if duration > slow_threshold:
                self._operation_stats['slow_operations'] += 1
                logger.warning(f"Slow operation '{operation_name}' took {duration:.2f}s")
            else:
                logger.info(f"Operation '{operation_name}' completed in {duration:.2f}s")
                
        except Exception as e:
            duration = time.time() - start_time
            self._operation_stats['failed_operations'] += 1
            logger.error(f"Operation '{operation_name}' failed after {duration:.2f}s: {e}")
            raise