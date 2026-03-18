# tools/list_tools.py
"""
List tools tool - List all tools functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_list_tools_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the list_tools tool with the MCP server"""

    @mcp.tool()
    def list_tools(category: str = None) -> dict:
        """List all available tools, optionally filtered by category"""
        if category:
            return tool_manager.list_by_category(category)
        return tool_manager.list_all()