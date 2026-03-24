"""
开发环境服务器主入口
简化启动逻辑，专注于开发环境需求
"""

import logging
from mcp.server.fastmcp import FastMCP

from .config import config
from ..tools.registry import register_all_tools
from ..database.connection import DatabaseManager

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_server():
    """创建并配置 MCP 服务器"""
    
    # 创建 FastMCP 服务器实例
    mcp = FastMCP(config.SERVER_NAME)
    
    try:
        # 初始化数据库管理器
        db_manager = DatabaseManager(config.DATABASE_URL)
        logger.info("Database manager initialized successfully")
        
        # 注册所有工具
        register_all_tools(mcp, db_manager)
        logger.info("All tools registered successfully")
        
        # 注册健康检查资源
        @mcp.resource("mcp://health")
        def health_check() -> dict:
            """健康检查端点"""
            return {
                "status": "healthy",
                "server": config.SERVER_NAME,
                "environment": "development"
            }
        
        return mcp
        
    except Exception as e:
        logger.error(f"Failed to initialize server: {str(e)}")
        raise


def main():
    """服务器主函数"""
    
    logger.info(f"Starting MCP server: {config.SERVER_NAME}")
    logger.info(f"Environment: development")
    logger.info(f"Server: {config.SERVER_HOST}:{config.SERVER_PORT}")
    logger.info(f"Database: {config.DATABASE_URL}")
    
    try:
        # 创建并启动服务器
        mcp = create_server()
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise


if __name__ == "__main__":
    main()