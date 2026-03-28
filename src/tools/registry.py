"""
MCP工具管理服务器 - 工具注册中心模块

提供统一的工具注册接口，管理所有MCP工具的注册过程。
支持简单工具和管理工具的分别注册，确保依赖关系正确。

特性:
- 统一的工具注册接口
- 支持依赖注入（数据库管理器）
- 模块化的工具注册逻辑
- 清晰的工具分类管理
"""

from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from ..database.connection import DatabaseManager

from .simple.echo import register_echo_tool
from .simple.calculator import register_calculator_tool
from .simple.datetime_tool import register_datetime_tool
from .management.tool_manager import register_tool_manager_tools


# =============================================================================
# 工具注册函数
# =============================================================================

def register_all_tools(mcp: FastMCP, db_manager: DatabaseManager) -> None:
    """
    注册所有工具到MCP服务器
    
    按照工具类型和依赖关系进行注册:
    - 简单工具: 无外部依赖，直接注册
    - 管理工具: 依赖数据库，需要数据库管理器实例
    
    Args:
        mcp (FastMCP): FastMCP服务器实例，用于工具注册
        db_manager (DatabaseManager): 数据库管理器实例，用于需要数据库的工具
        
    Raises:
        Exception: 如果工具注册过程中出现错误
        
    Example:
        >>> from src.core.config import config
        >>> from src.database.connection import DatabaseManager
        >>> from mcp.server.fastmcp import FastMCP
        >>> 
        >>> mcp = FastMCP(config.SERVER_NAME)
        >>> db_manager = DatabaseManager(config.DATABASE_URL)
        >>> register_all_tools(mcp, db_manager)
    """
    
    # =========================================================================
    # 注册简单工具（无外部依赖）
    # =========================================================================
    
    register_echo_tool(mcp)
    """注册回显工具 - 简单的消息回显功能"""
    
    register_calculator_tool(mcp)
    """注册安全计算器工具 - 安全的数学表达式计算"""
    
    register_datetime_tool(mcp)
    """注册时间日期工具 - 多时区时间处理和转换"""
    
    # =========================================================================
    # 注册管理工具（依赖数据库）
    # =========================================================================
    
    register_tool_manager_tools(mcp, db_manager)
    """注册工具管理器工具 - 工具CRUD操作和统计功能"""