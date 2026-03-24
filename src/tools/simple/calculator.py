"""
安全计算器工具
替换危险的 eval() 函数，使用安全的计算方式
"""

import operator
import re
from typing import Union
from mcp.server.fastmcp import FastMCP


class SafeCalculator:
    """安全计算器类"""
    
    # 允许的数学运算符
    ALLOWED_OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '//': operator.floordiv,
        '%': operator.mod,
        '**': operator.pow
    }
    
    # 允许的数学函数
    ALLOWED_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'max': max,
        'min': min
    }
    
    @classmethod
    def evaluate(cls, expression: str) -> Union[float, int, str]:
        """安全地计算数学表达式
        
        Args:
            expression: 数学表达式字符串
            
        Returns:
            计算结果或错误信息
        """
        try:
            # 清理表达式
            expression = expression.strip()
            
            # 验证表达式只包含允许的字符
            if not cls._is_valid_expression(expression):
                return "错误: 表达式包含不允许的字符"
            
            # 解析并计算表达式
            result = cls._parse_expression(expression)
            return result
            
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    @classmethod
    def _is_valid_expression(cls, expression: str) -> bool:
        """验证表达式是否安全"""
        # 允许的字符：数字、运算符、括号、空格、小数点
        pattern = r'^[0-9+\-*/().\s%]+$'
        return bool(re.match(pattern, expression))
    
    @classmethod
    def _parse_expression(cls, expression: str) -> Union[float, int]:
        """解析并计算表达式"""
        # 简单的表达式计算（避免使用 eval）
        # 这里实现一个简化的计算器，只支持基本运算
        
        # 移除空格
        expression = expression.replace(" ", "")
        
        # 处理括号（简化版）
        while '(' in expression and ')' in expression:
            start = expression.rfind('(')
            end = expression.find(')', start)
            
            if start < end:
                inner_expr = expression[start+1:end]
                inner_result = cls._calculate_simple(inner_expr)
                expression = expression[:start] + str(inner_result) + expression[end+1:]
            else:
                raise ValueError("括号不匹配")
        
        # 计算最终结果
        return cls._calculate_simple(expression)
    
    @classmethod
    def _calculate_simple(cls, expression: str) -> Union[float, int]:
        """计算简单表达式（无括号）"""
        
        def _to_int_if_possible(value: float) -> Union[float, int]:
            """如果值是整数，返回整数，否则返回浮点数"""
            if value.is_integer():
                return int(value)
            return value
        
        # 处理乘方
        if '**' in expression:
            parts = expression.split('**')
            if len(parts) == 2:
                base = float(parts[0])
                exponent = float(parts[1])
                return _to_int_if_possible(base ** exponent)
        
        # 处理乘除
        for op in ['*', '/', '//', '%']:
            if op in expression:
                parts = expression.split(op)
                if len(parts) == 2:
                    left = float(parts[0])
                    right = float(parts[1])
                    
                    if op == '*':
                        return _to_int_if_possible(left * right)
                    elif op == '/':
                        if right == 0:
                            raise ValueError("除数不能为零")
                        return _to_int_if_possible(left / right)
                    elif op == '//':
                        if right == 0:
                            raise ValueError("除数不能为零")
                        return left // right  # 整除总是返回整数
                    elif op == '%':
                        if right == 0:
                            raise ValueError("除数不能为零")
                        return _to_int_if_possible(left % right)
        
        # 处理加减
        for op in ['+', '-']:
            if op in expression and not expression.startswith(op):
                parts = expression.split(op)
                if len(parts) == 2:
                    left = float(parts[0])
                    right = float(parts[1])
                    
                    if op == '+':
                        return _to_int_if_possible(left + right)
                    elif op == '-':
                        return _to_int_if_possible(left - right)
        
        # 如果是单个数字
        try:
            if '.' in expression:
                value = float(expression)
                return _to_int_if_possible(value)
            else:
                return int(expression)
        except ValueError:
            raise ValueError(f"无法解析表达式: {expression}")


def register_calculator_tool(mcp: FastMCP):
    """注册安全计算器工具"""
    
    @mcp.tool()
    def calculate(expression: str) -> str:
        """安全地计算数学表达式
        
        Args:
            expression: 数学表达式（如 "2 + 3 * 4"）
            
        Returns:
            计算结果或错误信息
        """
        result = SafeCalculator.evaluate(expression)
        return f"结果: {result}"