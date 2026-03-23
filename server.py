"""MCP Production Server - 技能管理服务器

基于 FastMCP 构建，提供生产就绪的技能管理 API
支持多种数据库后端和环境配置
"""

import os
import logging
from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager
from tools.registry import register_all_tools
from config import config

# 配置日志
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL.upper()))
logger = logging.getLogger(__name__)

# 使用 FastMCP 创建服务器，使用配置中的服务器名称
mcp = FastMCP(config.SERVER_NAME)

try:
    # 创建全局工具管理器实例，使用配置中的数据库URL
    tool_manager = ToolManager(db_url=config.SQLALCHEMY_DATABASE_URL)
    logger.info("Tool manager initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize tool manager: {str(e)}")
    raise

# 注册所有工具
try:
    register_all_tools(mcp, tool_manager)
    logger.info("All tools registered successfully")
except Exception as e:
    logger.error(f"Failed to register tools: {str(e)}")
    raise

# 注册示例资源
@mcp.resource("mcp://data/sample")
def get_sample_data() -> str:
    """A sample data resource for demonstration"""
    return "This is sample data content from production server"


@mcp.resource("mcp://health")
def health_check() -> dict:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server_name": config.SERVER_NAME,
        "environment": os.getenv("ENVIRONMENT", "development")
    }


if __name__ == "__main__":
    logger.info(f"Starting MCP server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Database: {config.DATABASE_NAME} at {config.DATABASE_HOST}:{config.DATABASE_PORT}")
    
    try:
        # FastMCP可能不需要指定host和port，或者使用不同的参数名
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise