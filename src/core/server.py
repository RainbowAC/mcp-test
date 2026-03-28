"""
MCP工具管理服务器 - 服务器主入口模块

提供MCP服务器的创建、配置和启动功能。
包含工具注册、数据库初始化、健康检查等核心功能。

特性:
- 基于FastMCP框架的服务器实现
- 自动工具注册和数据库初始化
- 内置健康检查端点
- 完整的错误处理和日志记录
"""

import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP

from .config import config
from ..tools.registry import register_all_tools
from ..database.connection import DatabaseManager

# =============================================================================
# 日志配置
# =============================================================================

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# 服务器创建函数
# =============================================================================

def create_server() -> FastMCP:
    """
    创建并配置MCP服务器实例
    
    执行以下初始化步骤:
    1. 创建FastMCP服务器实例
    2. 初始化数据库连接管理器
    3. 注册所有MCP工具
    4. 配置健康检查端点
    5. 返回配置完成的服务器实例
    
    Returns:
        FastMCP: 配置完成的MCP服务器实例
        
    Raises:
        Exception: 如果初始化过程中出现错误
    """
    
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
            """
            健康检查端点
            
            提供服务器状态检查功能，用于监控和负载均衡。
            
            Returns:
                dict: 包含服务器状态信息的字典
            """
            return {
                "status": "healthy",
                "server": config.SERVER_NAME,
                "environment": "development"
            }
        
        logger.info("MCP server created and configured successfully")
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