# tools_module/utils.py
"""
工具函数模块
提供通用的辅助功能
"""

from typing import Dict, List
from .models import Tool, ToolStatistics


def normalize_tool_name(name: str) -> str:
    """
    标准化工具名称
    
    Args:
        name: 原始工具名称
        
    Returns:
        标准化后的名称（小写，空格替换为下划线）
    """
    return name.lower().replace(" ", "_")


def calculate_statistics(tools: Dict[str, Tool]) -> ToolStatistics:
    """
    计算工具统计信息
    
    Args:
        tools: 工具字典
        
    Returns:
        ToolStatistics 对象
    """
    if not tools:
        return ToolStatistics(
            total_tools=0,
            average_level=0.0,
            by_category={}
        )
    
    # 计算平均等级
    total_level = sum(tool.level for tool in tools.values())
    avg_level = round(total_level / len(tools), 2)
    
    # 按类别统计
    category_stats = {}
    for tool in tools.values():
        cat = tool.category
        if cat not in category_stats:
            category_stats[cat] = {
                "count": 0,
                "total_level": 0,
                "avg_level": 0
            }
        category_stats[cat]["count"] += 1
        category_stats[cat]["total_level"] += tool.level
    
    # 计算每个类别的平均等级
    for cat in category_stats:
        category_stats[cat]["avg_level"] = round(
            category_stats[cat]["total_level"] / category_stats[cat]["count"], 2
        )
        del category_stats[cat]["total_level"]  # 移除中间数据
    
    return ToolStatistics(
        total_tools=len(tools),
        average_level=avg_level,
        by_category=category_stats
    )


def format_tool_response(tool: Tool, found: bool = True) -> dict:
    """
    格式化工具响应
    
    Args:
        tool: Tool 对象
        found: 是否找到
        
    Returns:
        格式化的响应字典
    """
    if found:
        return {
            "found": True,
            "tool": tool.to_dict()
        }
    else:
        return {
            "found": False,
            "message": f"Tool '{tool.name}' not found"
        }


def format_error_response(message: str, success: bool = False) -> dict:
    """
    格式化错误响应
    
    Args:
        message: 错误消息
        success: 成功标志
        
    Returns:
        格式化的错误响应字典
    """
    return {
        "success": success,
        "message": message
    }


def format_success_response(message: str, data: dict = None) -> dict:
    """
    格式化成功响应
    
    Args:
        message: 成功消息
        data: 附加数据
        
    Returns:
        格式化的成功响应字典
    """
    response = {
        "success": True,
        "message": message
    }
    if data:
        response.update(data)
    return response
