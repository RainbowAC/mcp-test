# tools/update_tool.py
"""
Update tool tool - Update existing tool functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_update_tool_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the update_tool tool with the MCP server"""

    @mcp.tool()
    def update_tool(name: str, level: int = None, category: str = None) -> dict:
        """Update an existing tool's information"""
        return tool_manager.update_tool(name, level, category)