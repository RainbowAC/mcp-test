"""
优化版缓存管理模块
简化缓存实现，提高性能
"""

import time
from typing import Any, Dict, Optional
import re


class SimpleCache:
    """简单缓存类"""
    
    def __init__(self, expiry_time: int = 300):
        """初始化缓存
        
        Args:
            expiry_time: 缓存过期时间（秒）
        """
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._expiry_time = expiry_time
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值或 None（如果不存在或已过期）
        """
        if key not in self._timestamps:
            return None
        
        if time.time() - self._timestamps[key] > self._expiry_time:
            # 缓存已过期，清除
            self._delete(key)
            return None
        
        return self._cache.get(key)
    
    def set(self, key: str, value: Any):
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        self._cache[key] = value
        self._timestamps[key] = time.time()
    
    def delete(self, key: str):
        """删除指定缓存
        
        Args:
            key: 缓存键
        """
        self._delete(key)
    
    def clear(self):
        """清除所有缓存"""
        self._cache.clear()
        self._timestamps.clear()
    
    def clear_pattern(self, pattern: str):
        """清除匹配模式的缓存
        
        Args:
            pattern: 正则表达式模式
        """
        keys_to_delete = []
        
        for key in self._cache.keys():
            if re.search(pattern, key):
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            self._delete(key)
    
    def _delete(self, key: str):
        """内部删除方法"""
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        current_time = time.time()
        expired_count = 0
        
        for timestamp in self._timestamps.values():
            if current_time - timestamp > self._expiry_time:
                expired_count += 1
        
        return {
            "total_entries": len(self._cache),
            "expired_entries": expired_count,
            "expiry_time": self._expiry_time
        }