"""
优化版 Echo 工具
简化实现，移除冗余代码
"""

from mcp.server.fastmcp import FastMCP


def register_echo_tool(mcp: FastMCP):
    """注册 Echo 工具"""
    
    @mcp.tool()
    def echo(message: str) -> str:
        """回显输入的消息
        
        Args:
            message: 要回显的消息
            
        Returns:
            回显后的消息
        """
        return f"Echo: {message}"