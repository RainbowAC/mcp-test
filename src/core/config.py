"""
MCP工具管理服务器 - 配置管理模块

提供开发环境配置管理，支持环境变量和默认值配置。
包含服务器配置、数据库配置、应用配置和性能配置。

特性:
- 环境变量优先，默认值备用
- 类型安全的配置管理
- 动态数据库URL生成
- 开发环境优化配置
"""

import os
from typing import ClassVar


class DevelopmentConfig:
    """
    开发环境配置类
    
    提供MCP工具管理服务器的开发环境配置，支持环境变量覆盖。
    所有配置项都有合理的默认值，便于开发环境快速启动。
    """
    
    # =========================================================================
    # 服务器配置
    # =========================================================================
    
    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
    """服务器主机地址，默认: localhost"""
    
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "3000"))
    """服务器端口号，默认: 3000"""
    
    SERVER_NAME: str = os.getenv("SERVER_NAME", "mcp-tool-server-dev")
    """服务器名称标识，默认: mcp-tool-server-dev"""
    
    # =========================================================================
    # MySQL数据库配置
    # =========================================================================
    
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    """MySQL数据库主机地址，默认: localhost"""
    
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "3306"))
    """MySQL数据库端口号，默认: 3306"""
    
    DATABASE_USER: str = os.getenv("DATABASE_USER", "root")
    """MySQL数据库用户名，默认: root"""
    
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "123456")
    """MySQL数据库密码，默认: 123456"""
    
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "mcp_dev")
    """MySQL数据库名称，默认: mcp_dev"""
    
    @property
    def DATABASE_URL(self) -> str:
        """
        构建MySQL数据库连接URL
        
        根据数据库配置动态生成SQLAlchemy兼容的连接URL。
        
        Returns:
            str: MySQL连接URL，格式: mysql+pymysql://user:password@host:port/database
        """
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
    
    # =========================================================================
    # 应用配置
    # =========================================================================
    
    DEBUG: bool = True
    """调试模式开关，开发环境建议开启，默认: True"""
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    """日志级别，可选: DEBUG, INFO, WARNING, ERROR，默认: DEBUG"""
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-for-development")
    """应用密钥，用于安全相关功能，默认: dev-secret-key-for-development"""
    
    # =========================================================================
    # 性能配置
    # =========================================================================
    
    CACHE_EXPIRY: int = int(os.getenv("CACHE_EXPIRY", "300"))
    """缓存过期时间(秒)，默认: 300秒(5分钟)"""
    
    POOL_SIZE: int = int(os.getenv("POOL_SIZE", "5"))
    """数据库连接池大小，默认: 5个连接"""
    
    MAX_OVERFLOW: int = int(os.getenv("MAX_OVERFLOW", "10"))
    """数据库连接池最大溢出连接数，默认: 10个连接"""


# 全局配置实例
config: DevelopmentConfig = DevelopmentConfig()
"""
全局配置实例

在整个应用中使用的单一配置实例，确保配置一致性。
通过 `from src.core.config import config` 导入使用。
"""