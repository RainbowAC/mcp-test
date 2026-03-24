"""
开发环境配置管理模块
简化配置结构，专注于开发环境需求
"""

import os


class DevelopmentConfig:
    """开发环境配置类"""
    
    # 服务器配置
    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "3000"))
    SERVER_NAME: str = os.getenv("SERVER_NAME", "mcp-tool-server-dev")
    
    # MySQL数据库配置
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "3306"))
    DATABASE_USER: str = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "123456")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "mcp_dev")
    
    # 构建MySQL连接URL
    @property
    def DATABASE_URL(self) -> str:
        """构建MySQL连接URL"""
        return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    # 应用配置
    DEBUG: bool = True
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-for-development")
    
    # 性能配置
    CACHE_EXPIRY: int = int(os.getenv("CACHE_EXPIRY", "300"))
    POOL_SIZE: int = int(os.getenv("POOL_SIZE", "5"))
    MAX_OVERFLOW: int = int(os.getenv("MAX_OVERFLOW", "10"))


# 全局配置实例
config = DevelopmentConfig()