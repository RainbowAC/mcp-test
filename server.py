"""MCP Server - 技能管理服务器

基于 FastMCP 构建，提供技能管理的完整 API
"""

from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager
from tools.registry import register_all_tools

# 使用 FastMCP 创建服务器
mcp = FastMCP("test-mcp-server")

# 创建全局工具管理器实例
tool_manager = ToolManager()

# 注册所有工具
register_all_tools(mcp, tool_manager)


@mcp.resource("test://data/sample")
def get_sample_data() -> str:
    """A sample data resource for testing"""
    return "This is sample data content"


if __name__ == "__main__":
    mcp.run()
