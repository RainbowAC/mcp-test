# tools/add_tool.py
"""
Add tool tool - Add new tool functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_add_tool_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the add_tool tool with the MCP server"""

    @mcp.tool()
    def add_tool(name: str, level: int, category: str) -> dict:
        """Add a new tool to the database"""
        return tool_manager.add_tool(name, level, category)