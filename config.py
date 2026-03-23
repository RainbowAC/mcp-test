"""
生产环境配置文件
用于设置数据库连接、服务器配置和其他生产环境选项
"""

import os
from typing import Optional


class Config:
    """应用配置类"""
    
    # 服务器配置
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "3000"))
    
    # 数据库配置
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
    DATABASE_USER = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "123456")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "mcp_platform")
    
    # 完整的数据库URL
    DATABASE_URL_FORMAT = os.getenv(
        "DATABASE_URL_FORMAT", 
        "mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
    )
    DATABASE_URL = DATABASE_URL_FORMAT.format(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        name=DATABASE_NAME
    )
    
    # 可以根据环境变量使用不同的数据库URL
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)
    
    # 日志级别
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 调试模式
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 服务器名称
    SERVER_NAME = os.getenv("SERVER_NAME", "mcp-production-server")
    
    # 安全相关配置
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # 连接池配置
    POOL_SIZE = int(os.getenv("POOL_SIZE", "10"))
    MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", "20"))
    POOL_RECYCLE = int(os.getenv("POOL_RECYCLE", "3600"))  # 1 hour
    POOL_PRE_PING = os.getenv("POOL_PRE_PING", "True").lower() == "true"


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    DATABASE_URL = os.getenv("DEV_DATABASE_URL", "sqlite:///./mcp_dev.db")
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)


class StagingConfig(Config):
    """预发布环境配置"""
    DEBUG = False
    LOG_LEVEL = "INFO"
    # 可以在这里指定不同的数据库或其他预发布环境配置
    DATABASE_URL = os.getenv("STAGING_DATABASE_URL", "sqlite:///./mcp_staging.db")
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    
    # 在生产环境中强制要求SECRET_KEY
    def __init__(self):
        if not os.getenv("SECRET_KEY"):
            raise ValueError("SECRET_KEY environment variable is required in production")


# 根据环境选择配置
def get_config():
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production":
        return ProductionConfig()
    elif env == "staging":
        return StagingConfig()
    else:
        return DevelopmentConfig()


# 创建配置实例
config = get_config()