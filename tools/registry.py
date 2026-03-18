# tools/registry.py
"""
Tools registry - Central registry for all MCP tools
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

from . import (
    echo,
    calculate,
    list_tools,
    add_tool,
    get_tool_level,
    search_tools,
    update_tool,
    delete_tool,
    get_categories,
    get_statistics
)

def register_all_tools(mcp: FastMCP, tool_manager: ToolManager):
    """
    Register all tools with the MCP server

    Args:
        mcp: FastMCP server instance
        tool_manager: ToolManager instance
    """
    # Register simple tools (no dependencies)
    echo.register_echo_tool(mcp)
    calculate.register_calculate_tool(mcp)

    # Register tools that depend on ToolManager
    list_tools.register_list_tools_tool(mcp, tool_manager)
    add_tool.register_add_tool_tool(mcp, tool_manager)
    get_tool_level.register_get_tool_level_tool(mcp, tool_manager)
    search_tools.register_search_tools_tool(mcp, tool_manager)
    update_tool.register_update_tool_tool(mcp, tool_manager)
    delete_tool.register_delete_tool_tool(mcp, tool_manager)
    get_categories.register_get_categories_tool(mcp, tool_manager)
    get_statistics.register_get_statistics_tool(mcp, tool_manager)