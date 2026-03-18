# tools/echo.py
"""
Echo tool - Simple echo functionality
"""

from mcp.server.fastmcp import FastMCP

def register_echo_tool(mcp: FastMCP):
    """Register the echo tool with the MCP server"""

    @mcp.tool()
    def echo(message: str) -> str:
        """Echo back the input message"""
        return f"Echo: {message}"