# tools/delete_tool.py
"""
Delete tool tool - Delete tool functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_delete_tool_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the delete_tool tool with the MCP server"""

    @mcp.tool()
    def delete_tool(name: str) -> dict:
        """Delete a tool from the database"""
        return tool_manager.delete_tool(name)