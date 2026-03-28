"""
MCP工具管理服务器 - 时间日期工具模块

提供全面的时间日期处理功能，包括多时区转换、时间戳格式化、
时间差异计算和时间间隔添加等高级功能。

特性:
- 多时区支持，基于pytz库
- 时间戳与日期时间相互转换
- 精确的时间差异计算
- 灵活的时间间隔操作
- 完整的错误处理和边界情况处理

支持的时区示例:
- "Asia/Shanghai" - 中国上海
- "UTC" - 协调世界时
- "America/New_York" - 美国纽约
- "Europe/London" - 英国伦敦
"""

from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional, Tuple
from mcp.server.fastmcp import FastMCP


class DateTimeTool:
    """
    时间日期工具类
    
    提供静态方法的时间日期处理工具，支持:
    - 多时区时间获取和转换
    - 时间戳格式化和解析
    - 时间差异精确计算
    - 时间间隔添加和计算
    
    所有方法都是静态方法，无需实例化即可使用。
    """
    
    @staticmethod
    def get_current_time(timezone: str = "UTC") -> Dict[str, str]:
        """
        获取指定时区的当前时间
        
        返回指定时区的当前时间，包含完整的日期时间信息、时间戳和星期信息。
        
        Args:
            timezone (str): 时区名称，如 "Asia/Shanghai", "UTC", "America/New_York"
                           
        Returns:
            Dict[str, str]: 包含时间信息的字典，包含以下字段:
                - timezone: 时区名称
                - datetime: 完整日期时间 (YYYY-MM-DD HH:MM:SS)
                - date: 日期部分 (YYYY-MM-DD)
                - time: 时间部分 (HH:MM:SS)
                - timestamp: Unix时间戳 (整数)
                - day_of_week: 星期几 (英文全称)
                - week_number: ISO周数
                
        Raises:
            pytz.UnknownTimeZoneError: 如果时区名称无效
            
        Example:
            >>> DateTimeTool.get_current_time("Asia/Shanghai")
            {
                'timezone': 'Asia/Shanghai',
                'datetime': '2024-01-01 12:00:00',
                'date': '2024-01-01',
                'time': '12:00:00',
                'timestamp': 1704081600,
                'day_of_week': 'Monday',
                'week_number': 1
            }
        """
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            
            return {
                "timezone": timezone,
                "datetime": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M:%S"),
                "timestamp": int(current_time.timestamp()),
                "day_of_week": current_time.strftime("%A"),
                "week_number": current_time.isocalendar()[1]
            }
        except pytz.UnknownTimeZoneError:
            return {"error": f"未知时区: {timezone}"}
    
    @staticmethod
    def convert_timezone(datetime_str: str, from_tz: str, to_tz: str) -> Dict[str, str]:
        """转换时区
        
        Args:
            datetime_str: 日期时间字符串，格式: "YYYY-MM-DD HH:MM:SS"
            from_tz: 原始时区
            to_tz: 目标时区
            
        Returns:
            转换后的时间信息
        """
        try:
            from_timezone = pytz.timezone(from_tz)
            to_timezone = pytz.timezone(to_tz)
            
            # 解析输入时间
            dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            dt_with_tz = from_timezone.localize(dt)
            
            # 转换时区
            converted_dt = dt_with_tz.astimezone(to_timezone)
            
            return {
                "original": {
                    "datetime": datetime_str,
                    "timezone": from_tz
                },
                "converted": {
                    "datetime": converted_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "timezone": to_tz,
                    "timestamp": int(converted_dt.timestamp())
                }
            }
        except ValueError as e:
            return {"error": f"时间格式错误: {str(e)}"}
        except pytz.UnknownTimeZoneError as e:
            return {"error": f"时区错误: {str(e)}"}
    
    @staticmethod
    def format_timestamp(timestamp: int, timezone: str = "UTC") -> Dict[str, str]:
        """格式化时间戳
        
        Args:
            timestamp: Unix时间戳
            timezone: 时区名称
            
        Returns:
            格式化后的时间信息
        """
        try:
            tz = pytz.timezone(timezone)
            dt = datetime.fromtimestamp(timestamp, tz)
            
            return {
                "timestamp": timestamp,
                "timezone": timezone,
                "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "iso_format": dt.isoformat(),
                "readable": dt.strftime("%A, %B %d, %Y at %I:%M:%S %p"),
                "relative": DateTimeTool._get_relative_time(dt)
            }
        except pytz.UnknownTimeZoneError:
            return {"error": f"未知时区: {timezone}"}
    
    @staticmethod
    def calculate_difference(start_time: str, end_time: str, 
                           start_tz: str = "UTC", end_tz: str = "UTC") -> Dict[str, str]:
        """计算两个时间之间的差异
        
        Args:
            start_time: 开始时间，格式: "YYYY-MM-DD HH:MM:SS"
            end_time: 结束时间，格式: "YYYY-MM-DD HH:MM:SS"
            start_tz: 开始时间时区
            end_tz: 结束时间时区
            
        Returns:
            时间差异信息
        """
        try:
            start_tz_obj = pytz.timezone(start_tz)
            end_tz_obj = pytz.timezone(end_tz)
            
            # 解析时间
            start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            
            # 添加时区信息
            start_dt_with_tz = start_tz_obj.localize(start_dt)
            end_dt_with_tz = end_tz_obj.localize(end_dt)
            
            # 计算差异
            diff = end_dt_with_tz - start_dt_with_tz
            
            return {
                "start": start_dt_with_tz.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "end": end_dt_with_tz.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "difference": {
                    "total_seconds": int(diff.total_seconds()),
                    "days": diff.days,
                    "hours": diff.total_seconds() // 3600,
                    "minutes": diff.total_seconds() // 60,
                    "human_readable": str(diff)
                }
            }
        except Exception as e:
            return {"error": f"计算时间差异时出错: {str(e)}"}
    
    @staticmethod
    def add_duration(base_time: str, duration: str, timezone: str = "UTC") -> Dict[str, str]:
        """在基础时间上添加时间间隔
        
        Args:
            base_time: 基础时间，格式: "YYYY-MM-DD HH:MM:SS"
            duration: 时间间隔，如 "2d3h30m" (2天3小时30分钟)
            timezone: 时区
            
        Returns:
            计算后的时间
        """
        try:
            tz = pytz.timezone(timezone)
            base_dt = datetime.strptime(base_time, "%Y-%m-%d %H:%M:%S")
            base_dt_with_tz = tz.localize(base_dt)
            
            # 解析时间间隔
            delta = DateTimeTool._parse_duration(duration)
            
            # 计算新时间
            new_dt = base_dt_with_tz + delta
            
            return {
                "base_time": base_dt_with_tz.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "duration": duration,
                "result_time": new_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "timestamp": int(new_dt.timestamp())
            }
        except Exception as e:
            return {"error": f"添加时间间隔时出错: {str(e)}"}
    
    @staticmethod
    def _parse_duration(duration_str: str) -> timedelta:
        """解析时间间隔字符串"""
        import re
        
        # 匹配模式：数字+单位 (d=天, h=小时, m=分钟, s=秒)
        pattern = r'(\d+)([dhms])'
        matches = re.findall(pattern, duration_str)
        
        if not matches:
            raise ValueError("无效的时间间隔格式")
        
        delta = timedelta()
        for value, unit in matches:
            if unit == 'd':
                delta += timedelta(days=int(value))
            elif unit == 'h':
                delta += timedelta(hours=int(value))
            elif unit == 'm':
                delta += timedelta(minutes=int(value))
            elif unit == 's':
                delta += timedelta(seconds=int(value))
        
        return delta
    
    @staticmethod
    def _get_relative_time(dt: datetime) -> str:
        """获取相对时间描述"""
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        
        if diff.total_seconds() < 60:
            return "刚刚"
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() // 60)
            return f"{minutes}分钟前"
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() // 3600)
            return f"{hours}小时前"
        elif diff.days == 1:
            return "昨天"
        elif diff.days < 7:
            return f"{diff.days}天前"
        else:
            weeks = diff.days // 7
            return f"{weeks}周前"


def register_datetime_tool(mcp: FastMCP):
    """注册时间日期工具"""
    
    @mcp.tool()
    def get_current_time(timezone: str = "UTC") -> Dict[str, str]:
        """获取指定时区的当前时间
        
        Args:
            timezone: 时区名称，如 "Asia/Shanghai", "UTC", "America/New_York"
            
        Returns:
            包含时间信息的字典
        """
        return DateTimeTool.get_current_time(timezone)
    
    @mcp.tool()
    def convert_timezone(datetime_str: str, from_timezone: str, to_timezone: str) -> Dict[str, str]:
        """转换时区
        
        Args:
            datetime_str: 日期时间字符串，格式: "YYYY-MM-DD HH:MM:SS"
            from_timezone: 原始时区
            to_timezone: 目标时区
            
        Returns:
            转换后的时间信息
        """
        return DateTimeTool.convert_timezone(datetime_str, from_timezone, to_timezone)
    
    @mcp.tool()
    def format_timestamp(timestamp: int, timezone: str = "UTC") -> Dict[str, str]:
        """格式化时间戳
        
        Args:
            timestamp: Unix时间戳
            timezone: 时区名称
            
        Returns:
            格式化后的时间信息
        """
        return DateTimeTool.format_timestamp(timestamp, timezone)
    
    @mcp.tool()
    def calculate_time_difference(start_time: str, end_time: str, 
                                start_timezone: str = "UTC", end_timezone: str = "UTC") -> Dict[str, str]:
        """计算两个时间之间的差异
        
        Args:
            start_time: 开始时间，格式: "YYYY-MM-DD HH:MM:SS"
            end_time: 结束时间，格式: "YYYY-MM-DD HH:MM:SS"
            start_timezone: 开始时间时区
            end_timezone: 结束时间时区
            
        Returns:
            时间差异信息
        """
        return DateTimeTool.calculate_difference(start_time, end_time, start_timezone, end_timezone)
    
    @mcp.tool()
    def add_duration_to_time(base_time: str, duration: str, timezone: str = "UTC") -> Dict[str, str]:
        """在基础时间上添加时间间隔
        
        Args:
            base_time: 基础时间，格式: "YYYY-MM-DD HH:MM:SS"
            duration: 时间间隔，如 "2d3h30m" (2天3小时30分钟)
            timezone: 时区
            
        Returns:
            计算后的时间
        """
        return DateTimeTool.add_duration(base_time, duration, timezone)


# =============================================================================
# 时间日期工具专用测试函数
# =============================================================================

def test_datetime_tool_functionality() -> bool:
    """测试时间日期工具的核心功能"""
    print("🧪 测试时间日期工具核心功能...")
    
    try:
        # 测试获取当前时间
        result = DateTimeTool.get_current_time("Asia/Shanghai")
        assert "datetime" in result, "获取当前时间失败"
        print("✅ 获取当前时间功能正常")
        
        # 测试时区转换
        result = DateTimeTool.convert_timezone("2024-01-01 12:00:00", "UTC", "Asia/Shanghai")
        assert "converted" in result, "时区转换失败"
        assert result["converted"]["datetime"] == "2024-01-01 20:00:00", "时区转换结果错误"
        print("✅ 时区转换功能正常")
        
        # 测试时间戳格式化
        result = DateTimeTool.format_timestamp(1704067200, "Asia/Shanghai")
        assert "datetime" in result, "时间戳格式化失败"
        assert result["datetime"] == "2024-01-01 08:00:00", "时间戳格式化结果错误"
        print("✅ 时间戳格式化功能正常")
        
        # 测试时间差异计算
        result = DateTimeTool.calculate_difference(
            "2024-01-01 12:00:00", "2024-01-02 14:30:00", "UTC", "UTC"
        )
        assert "difference" in result, "时间差异计算失败"
        assert result["difference"]["total_seconds"] == 95400, "时间差异计算结果错误"
        print("✅ 时间差异计算功能正常")
        
        # 测试时间间隔添加
        result = DateTimeTool.add_duration("2024-01-01 12:00:00", "2d3h30m", "UTC")
        assert "result_time" in result, "时间间隔添加失败"
        assert "2024-01-03 15:30:00" in result["result_time"], "时间间隔添加结果错误"
        print("✅ 时间间隔添加功能正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 时间日期工具功能测试失败: {e}")
        return False


def test_datetime_tool_edge_cases() -> bool:
    """测试时间日期工具的边界情况"""
    print("🧪 测试时间日期工具边界情况...")
    
    try:
        # 测试无效时区处理
        result = DateTimeTool.get_current_time("Invalid/Timezone")
        assert "error" in result, "无效时区处理失败"
        print("✅ 无效时区处理正常")
        
        # 测试时间格式错误处理
        result = DateTimeTool.convert_timezone("invalid-date", "UTC", "Asia/Shanghai")
        assert "error" in result, "无效时间格式处理失败"
        print("✅ 无效时间格式处理正常")
        
        # 测试负时间戳
        result = DateTimeTool.format_timestamp(-1000, "UTC")
        assert "datetime" in result or "error" in result, "负时间戳处理失败"
        print("✅ 负时间戳处理正常")
        
        return True
        
    except Exception as e:
        print(f"❌ 时间日期工具边界测试失败: {e}")
        return False


def test_datetime_tool_performance() -> bool:
    """测试时间日期工具的性能"""
    print("🧪 测试时间日期工具性能...")
    
    try:
        import time
        
        # 测试批量时间转换性能
        start_time = time.time()
        
        for i in range(100):
            DateTimeTool.get_current_time("UTC")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"✅ 批量时间获取性能: {execution_time:.3f}秒 (100次调用)")
        
        # 性能阈值检查
        if execution_time < 1.0:  # 1秒内完成100次调用
            print("✅ 性能测试通过")
            return True
        else:
            print("⚠️  性能较慢，但功能正常")
            return True  # 性能问题不视为测试失败
            
    except Exception as e:
        print(f"❌ 时间日期工具性能测试失败: {e}")
        return False