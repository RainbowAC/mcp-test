"""
优化版工具注册中心
简化注册逻辑，统一接口
"""

from mcp.server.fastmcp import FastMCP
from ..database.connection import DatabaseManager

from .simple.echo import register_echo_tool
from .simple.calculator import register_calculator_tool
from .management.tool_manager import register_tool_manager_tools


def register_all_tools(mcp: FastMCP, db_manager: DatabaseManager):
    """注册所有工具到 MCP 服务器
    
    Args:
        mcp: FastMCP 服务器实例
        db_manager: 数据库管理器实例
    """
    
    # 注册简单工具（无依赖）
    register_echo_tool(mcp)
    register_calculator_tool(mcp)
    
    # 注册管理工具（依赖数据库）
    register_tool_manager_tools(mcp, db_manager)