# tools_module/database.py
"""
工具数据库模块
提供工具数据的持久化存储和管理
"""

from typing import Dict, Optional
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool
import logging
from .models import Tool

# 配置日志
logger = logging.getLogger(__name__)

Base = declarative_base()


class ToolEntity(Base):
    """工具实体类 - 对应数据库表"""
    __tablename__ = 'tools'
    
    name = Column(String(255), primary_key=True)
    level = Column(Integer, nullable=False)
    category = Column(String(255), nullable=False)


class ToolDatabase:
    """工具数据库类"""
    
    def __init__(self, db_url: str = "mysql+pymysql://root:123456@localhost:3306/mcp_tools"):
        """初始化工具数据库"""
        # 配置连接池参数
        self.engine = create_engine(
            db_url,
            echo=False,
            poolclass=QueuePool,  # 显式指定连接池类型
            pool_pre_ping=True,   # 检测断开的连接
            pool_recycle=3600,    # 1小时回收连接
            pool_size=10,         # 连接池大小
            max_overflow=20,      # 最大溢出连接数
            pool_timeout=30,      # 连接超时时间
            pool_reset_on_return='commit'  # 返回连接池时重置连接
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        
        # 初始化默认工具数据（仅当数据库为空时）
        self._initialize_default_tools_if_empty()
        
        # 记录连接池信息
        logger.info(f"Database connection established. Pool size: {self.engine.pool.size()}, "
                   f"Max overflow: {getattr(self.engine.pool, 'max_overflow', 'N/A')}")
    
    @contextmanager
    def get_session(self):
        """获取数据库会话的上下文管理器"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def _initialize_default_tools_if_empty(self):
        """如果数据库为空，则初始化默认工具数据"""
        with self.get_session() as db:
            try:
                count = db.query(ToolEntity).count()
            except SQLAlchemyError:
                # 如果查询失败（例如表不存在），则捕获异常并继续
                count = 0
                
            if count == 0:
                default_tools = [
                    {"name": "Python", "level": 5, "category": "Programming"},
                    {"name": "JavaScript", "level": 4, "category": "Programming"},
                    {"name": "Docker", "level": 3, "category": "DevOps"},
                    {"name": "Kubernetes", "level": 2, "category": "DevOps"},
                ]
                
                for tool_data in default_tools:
                    tool_entity = ToolEntity(**tool_data)
                    db.add(tool_entity)
    
    def _normalize_key(self, name: str) -> str:
        """标准化工具名称作为键"""
        return name.lower().replace(" ", "_")
    
    def get_all(self) -> Dict[str, Tool]:
        """获取所有工具"""
        with self.get_session() as db:
            entities = db.query(ToolEntity).all()
            tools = {}
            for entity in entities:
                tool = Tool(name=entity.name, level=entity.level, category=entity.category)
                key = self._normalize_key(tool.name)
                tools[key] = tool
            return tools
    
    def get(self, name: str) -> Optional[Tool]:
        """获取指定工具"""
        with self.get_session() as db:
            entity = db.query(ToolEntity).filter(ToolEntity.name == name).first()
            if entity:
                return Tool(name=entity.name, level=entity.level, category=entity.category)
            return None
    
    def add(self, tool: Tool) -> bool:
        """添加工具"""
        with self.get_session() as db:
            try:
                existing_entity = db.query(ToolEntity).filter(ToolEntity.name == tool.name).first()
                if existing_entity:
                    return False
                
                entity = ToolEntity(name=tool.name, level=tool.level, category=tool.category)
                db.add(entity)
                return True
            except SQLAlchemyError:
                return False
    
    def update(self, name: str, level: Optional[int] = None, category: Optional[str] = None) -> Optional[Tool]:
        """更新工具信息"""
        with self.get_session() as db:
            try:
                entity = db.query(ToolEntity).filter(ToolEntity.name == name).first()
                if not entity:
                    return None
                
                if level is not None:
                    entity.level = level
                if category is not None:
                    entity.category = category
                
                return Tool(name=entity.name, level=entity.level, category=entity.category)
            except SQLAlchemyError:
                return None
    
    def delete(self, name: str) -> Optional[Tool]:
        """删除工具"""
        with self.get_session() as db:
            try:
                entity = db.query(ToolEntity).filter(ToolEntity.name == name).first()
                if not entity:
                    return None
                
                deleted_tool = Tool(name=entity.name, level=entity.level, category=entity.category)
                db.delete(entity)
                return deleted_tool
            except SQLAlchemyError:
                return None
    
    def get_by_category(self, category: str) -> Dict[str, Tool]:
        """按类别获取工具"""
        with self.get_session() as db:
            entities = db.query(ToolEntity).filter(ToolEntity.category == category).all()
            tools = {}
            for entity in entities:
                tool = Tool(name=entity.name, level=entity.level, category=entity.category)
                key = self._normalize_key(tool.name)
                tools[key] = tool
            return tools
    
    def get_categories(self) -> list:
        """获取所有类别"""
        with self.get_session() as db:
            results = db.execute(text("SELECT DISTINCT category FROM tools")).fetchall()
            categories = [row[0] for row in results]
            return sorted(categories)
    
    def count(self) -> int:
        """获取工具总数"""
        with self.get_session() as db:
            return db.query(ToolEntity).count()
    
    def clear(self):
        """清空数据库（用于测试）"""
        with self.get_session() as db:
            db.execute(text("DELETE FROM tools"))
            # 直接添加默认工具，而不是调用 _initialize_default_tools_if_empty
            # 因为那个方法会先检查计数，而此时数据库已经被清空
            default_tools = [
                {"name": "Python", "level": 5, "category": "Programming"},
                {"name": "JavaScript", "level": 4, "category": "Programming"},
                {"name": "Docker", "level": 3, "category": "DevOps"},
                {"name": "Kubernetes", "level": 2, "category": "DevOps"},
            ]
            
            for tool_data in default_tools:
                tool_entity = ToolEntity(**tool_data)
                db.add(tool_entity)
    
    def search(self, keyword: str) -> Dict[str, Tool]:
        """搜索工具"""
        if not keyword:
            return {}
        
        with self.get_session() as db:
            entities = db.query(ToolEntity).filter(ToolEntity.name.like(f"%{keyword}%")).all()
            tools = {}
            for entity in entities:
                tool = Tool(name=entity.name, level=entity.level, category=entity.category)
                key = self._normalize_key(tool.name)
                tools[key] = tool
            return tools

    def get_pool_status(self) -> dict:
        """获取连接池状态信息"""
        try:
            # 获取连接池信息
            pool = self.engine.pool
            status = {
                "pool_size": pool.size(),
                "checked_in_connections": getattr(pool, 'checkedin', lambda: 'N/A')(),  # 有些池类型可能没有此方法
                "overflow": getattr(pool, 'overflow', lambda: 'N/A')(),
                "connections_checked_out": 'N/A'  # 由于不同池类型有不同的属性，简化处理
            }
            return status
        except Exception as e:
            logger.warning(f"Could not retrieve pool status: {e}")
            return {"error": str(e)}