"""
性能测试脚本
用于测试优化后的工具管理器性能
"""

import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools_module import ToolManager

def performance_test():
    """执行性能测试"""
    print("开始性能测试...")
    
    # 创建工具管理器实例
    manager = ToolManager(cache_expiry=300)  # 设置较短的缓存过期时间以便测试
    
    # 测试1: 测试缓存性能
    print("\n1. 测试缓存性能...")
    start_time = time.time()
    
    # 第一次获取所有工具（无缓存）
    result1 = manager.list_all()
    first_call_time = time.time() - start_time
    print(f"   首次调用耗时: {first_call_time:.4f}秒")
    
    # 第二次获取所有工具（应使用缓存）
    start_time = time.time()
    result2 = manager.list_all()
    cached_call_time = time.time() - start_time
    print(f"   缓存调用耗时: {cached_call_time:.4f}秒")
    print(f"   性能提升: {first_call_time/cached_call_time:.2f}x" if cached_call_time > 0 else "无法计算")
    
    # 测试2: 测试批量操作性能
    print("\n2. 测试批量操作性能...")
    start_time = time.time()
    
    # 批量添加工具
    tools_data = [
        {"name": f"TestTool{i}", "level": i % 5 + 1, "category": "Testing"} 
        for i in range(10)
    ]
    batch_result = manager.bulk_add_tools(tools_data)
    batch_time = time.time() - start_time
    print(f"   批量添加10个工具耗时: {batch_time:.4f}秒")
    print(f"   成功添加: {batch_result['summary']['added']} 个")
    
    # 测试3: 测试性能监控
    print("\n3. 测试性能监控...")
    metrics = manager.get_performance_metrics()
    print(f"   工具总数: {metrics['application'].get('total_tools', 'N/A')}")
    print(f"   CPU使用率: {metrics['system'].get('cpu_percent', 'N/A')}%")
    print(f"   内存使用率: {metrics['system'].get('memory_percent', 'N/A')}%")
    
    # 清理测试数据
    print("\n4. 清理测试数据...")
    for i in range(10):
        manager.delete_tool(f"TestTool{i}")
    
    print("\n性能测试完成!")

if __name__ == "__main__":
    performance_test()