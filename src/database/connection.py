"""
MySQL数据库连接管理
优化MySQL连接池配置，改进错误处理和性能
"""

from typing import Dict, Optional, Generator
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
import logging
import time
from functools import wraps

from .models import Tool

logger = logging.getLogger(__name__)

Base = declarative_base()


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """数据库操作重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except SQLAlchemyError as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Database operation failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"Database operation failed (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator


class ToolEntity(Base):
    """工具实体类 - 对应MySQL数据库表"""
    __tablename__ = 'tools'
    
    name = Column(String(255), primary_key=True)
    level = Column(Integer, nullable=False)
    category = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)  # 新增描述字段


class DatabaseManager:
    """MySQL数据库管理器类 - 优化版本"""
    
    def __init__(self, db_url: str):
        """初始化MySQL数据库管理器"""
        self.db_url = db_url
        self._connection_stats = {
            'total_connections': 0,
            'failed_connections': 0,
            'last_connection_time': None
        }
        
        # 创建MySQL数据库引擎 - 优化配置
        self.engine = create_engine(
            db_url,
            echo=False,  # 生产环境关闭SQL日志
            poolclass=QueuePool,
            pool_pre_ping=True,  # 连接前检查
            pool_recycle=1800,   # 30分钟回收连接
            pool_size=8,         # 优化连接池大小
            max_overflow=15,     # 优化溢出连接数
            pool_timeout=30,     # 连接超时时间
            connect_args={
                "charset": "utf8mb4",
                "connect_timeout": 10,  # 连接超时
                "read_timeout": 30,     # 读取超时
                "write_timeout": 30     # 写入超时
            }
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine,
            expire_on_commit=False  # 优化性能
        )
        
        # 创建表结构
        self._create_tables()
        
        # 初始化默认数据
        self._initialize_default_data()
        
        logger.info(f"MySQL database manager initialized with URL: {db_url}")
    
    @retry_on_failure(max_retries=3, delay=1.0)
    def _create_tables(self):
        """创建表结构 - 带重试机制"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("MySQL database tables created successfully")
    
    @contextmanager
    def get_session(self) -> Generator:
        """获取数据库会话的上下文管理器 - 带性能监控"""
        start_time = time.time()
        session = self.SessionLocal()
        
        try:
            self._connection_stats['total_connections'] += 1
            self._connection_stats['last_connection_time'] = time.time()
            
            yield session
            session.commit()
            
            # 记录成功操作
            duration = time.time() - start_time
            if duration > 1.0:  # 超过1秒的操作记录警告
                logger.warning(f"Database operation took {duration:.2f}s")
                
        except Exception as e:
            session.rollback()
            self._connection_stats['failed_connections'] += 1
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            session.close()
    
    def _initialize_default_data(self):
        """初始化默认数据"""
        with self.get_session() as session:
            try:
                # 检查是否已有数据
                count = session.query(ToolEntity).count()
                if count == 0:
                    # 添加默认工具
                    default_tools = [
                        ToolEntity(name="Python", level=5, category="Programming", 
                                 description="Python programming language"),
                        ToolEntity(name="JavaScript", level=4, category="Programming",
                                 description="JavaScript programming language"),
                        ToolEntity(name="Docker", level=3, category="DevOps",
                                 description="Containerization platform"),
                        ToolEntity(name="Kubernetes", level=2, category="DevOps",
                                 description="Container orchestration platform"),
                    ]
                    
                    session.add_all(default_tools)
                    session.commit()
                    logger.info("Default tools initialized in MySQL")
                    
            except SQLAlchemyError as e:
                logger.warning(f"Failed to initialize default data: {e}")
    
    def get_pool_status(self) -> Dict:
        """获取连接池状态"""
        return {
            "checked_in": self.engine.pool.checkedin(),
            "checked_out": self.engine.pool.checkedout(),
            "size": self.engine.pool.size(),
            "overflow": self.engine.pool.overflow()
        }