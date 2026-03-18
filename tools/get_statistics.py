# tools/get_statistics.py
"""
Get statistics tool - Get tools statistics functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_get_statistics_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the get_statistics tool with the MCP server"""

    @mcp.tool()
    def get_statistics() -> dict:
        """Get statistics about all tools"""
        return tool_manager.get_statistics()