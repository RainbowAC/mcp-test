# tools/get_tool_level.py
"""
Get tool level tool - Get specific tool level functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_get_tool_level_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the get_tool_level tool with the MCP server"""

    @mcp.tool()
    def get_tool_level(tool_name: str) -> dict:
        """Get the level of a specific tool"""
        return tool_manager.get_tool(tool_name)