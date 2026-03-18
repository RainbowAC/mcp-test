# tools/search_tools.py
"""
Search tools tool - Search tools by keyword functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_search_tools_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the search_tools tool with the MCP server"""

    @mcp.tool()
    def search_tools(keyword: str) -> dict:
        """Search tools by keyword in name"""
        return tool_manager.search_tools(keyword)