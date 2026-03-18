# tools/get_categories.py
"""
Get categories tool - Get all tool categories functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_get_categories_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the get_categories tool with the MCP server"""

    @mcp.tool()
    def get_categories() -> dict:
        """Get all tool categories"""
        return tool_manager.get_categories()