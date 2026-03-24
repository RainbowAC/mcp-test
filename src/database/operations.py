"""
优化版数据库操作模块
统一数据库操作接口，简化代码
"""

from typing import Dict, List, Optional
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import logging

from .connection import DatabaseManager
from .models import Tool

logger = logging.getLogger(__name__)


class ToolOperations:
    """工具数据库操作类"""
    
    def __init__(self, db_manager: DatabaseManager):
        """初始化工具操作类"""
        self.db_manager = db_manager
    
    def get_all_tools(self) -> Dict[str, Tool]:
        """获取所有工具"""
        with self.db_manager.get_session() as session:
            try:
                entities = session.query(self.db_manager.ToolEntity).all()
                tools = {}
                for entity in entities:
                    tool = Tool(
                        name=entity.name,
                        level=entity.level,
                        category=entity.category
                    )
                    tools[tool.name.lower()] = tool
                return tools
                
            except SQLAlchemyError as e:
                logger.error(f"Error getting all tools: {e}")
                return {}
    
    def get_tool_by_name(self, name: str) -> Optional[Tool]:
        """根据名称获取工具"""
        with self.db_manager.get_session() as session:
            try:
                entity = session.query(self.db_manager.ToolEntity).filter_by(name=name).first()
                if entity:
                    return Tool(
                        name=entity.name,
                        level=entity.level,
                        category=entity.category
                    )
                return None
                
            except SQLAlchemyError as e:
                logger.error(f"Error getting tool {name}: {e}")
                return None
    
    def add_tool(self, tool: Tool) -> bool:
        """添加工具"""
        with self.db_manager.get_session() as session:
            try:
                entity = self.db_manager.ToolEntity(
                    name=tool.name,
                    level=tool.level,
                    category=tool.category
                )
                session.add(entity)
                return True
                
            except SQLAlchemyError as e:
                logger.error(f"Error adding tool {tool.name}: {e}")
                return False
    
    def update_tool(self, name: str, level: Optional[int] = None, category: Optional[str] = None) -> bool:
        """更新工具"""
        with self.db_manager.get_session() as session:
            try:
                entity = session.query(self.db_manager.ToolEntity).filter_by(name=name).first()
                if entity:
                    if level is not None:
                        entity.level = level
                    if category is not None:
                        entity.category = category
                    return True
                return False
                
            except SQLAlchemyError as e:
                logger.error(f"Error updating tool {name}: {e}")
                return False
    
    def delete_tool(self, name: str) -> bool:
        """删除工具"""
        with self.db_manager.get_session() as session:
            try:
                entity = session.query(self.db_manager.ToolEntity).filter_by(name=name).first()
                if entity:
                    session.delete(entity)
                    return True
                return False
                
            except SQLAlchemyError as e:
                logger.error(f"Error deleting tool {name}: {e}")
                return False
    
    def get_tools_by_category(self, category: str) -> List[Tool]:
        """根据类别获取工具"""
        with self.db_manager.get_session() as session:
            try:
                entities = session.query(self.db_manager.ToolEntity).filter_by(category=category).all()
                return [
                    Tool(name=entity.name, level=entity.level, category=entity.category)
                    for entity in entities
                ]
                
            except SQLAlchemyError as e:
                logger.error(f"Error getting tools by category {category}: {e}")
                return []
    
    def get_statistics(self) -> Dict:
        """获取工具统计信息"""
        with self.db_manager.get_session() as session:
            try:
                total_tools = session.query(self.db_manager.ToolEntity).count()
                
                # 计算平均等级
                avg_level_result = session.query(
                    sqlalchemy.func.avg(self.db_manager.ToolEntity.level)
                ).scalar()
                average_level = round(avg_level_result or 0, 2)
                
                # 按类别统计
                category_stats = session.query(
                    self.db_manager.ToolEntity.category,
                    sqlalchemy.func.count(self.db_manager.ToolEntity.name)
                ).group_by(self.db_manager.ToolEntity.category).all()
                
                by_category = {category: count for category, count in category_stats}
                
                return {
                    "total_tools": total_tools,
                    "average_level": average_level,
                    "by_category": by_category
                }
                
            except SQLAlchemyError as e:
                logger.error(f"Error getting statistics: {e}")
                return {"total_tools": 0, "average_level": 0, "by_category": {}}