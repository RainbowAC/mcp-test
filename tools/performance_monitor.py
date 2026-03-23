# tools/performance_monitor.py
"""
Performance Monitor tool - System performance monitoring functionality
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_performance_monitor_tool(mcp: FastMCP, tool_manager: ToolManager):
    """Register the performance monitor tool with the MCP server"""

    @mcp.tool()
    def performance_monitor() -> dict:
        """Get system performance metrics including CPU, memory, and database status"""
        return tool_manager.get_performance_metrics()