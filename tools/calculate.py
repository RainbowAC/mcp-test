# tools/calculate.py
"""
Calculate tool - Basic calculation functionality
"""

from mcp.server.fastmcp import FastMCP

def register_calculate_tool(mcp: FastMCP):
    """Register the calculate tool with the MCP server"""

    @mcp.tool()
    def calculate(expression: str) -> str:
        """Perform basic calculation"""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"