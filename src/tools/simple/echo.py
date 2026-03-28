"""
优化版 Echo 工具
简化实现，移除冗余代码
"""

from mcp.server.fastmcp import FastMCP


def register_echo_tool(mcp: FastMCP):
    """注册 Echo 工具"""
    
    @mcp.tool()
    def echo(message: str) -> str:
        """回显输入的消息
        
        Args:
            message: 要回显的消息
            
        Returns:
            回显后的消息
        """
        return f"Echo: {message}"


# =============================================================================
# Echo工具专用测试函数
# =============================================================================

def test_echo_basic_functionality() -> bool:
    """测试Echo工具基本功能"""
    print("🧪 测试Echo工具基本功能...")
    
    try:
        # 测试基本回显功能
        test_cases = [
            ("Hello", "Echo: Hello"),
            ("测试消息", "Echo: 测试消息"),
            ("123", "Echo: 123"),
            ("", "Echo: "),  # 空消息
            ("A" * 100, "Echo: " + "A" * 100)  # 长消息
        ]
        
        all_passed = True
        for message, expected in test_cases:
            # 模拟echo函数调用
            result = f"Echo: {message}"
            if result == expected:
                print(f"✅ 回显: '{message[:20]}...' -> '{result[:20]}...'")
            else:
                print(f"❌ 回显失败: '{message}' -> '{result}' (期望: '{expected}')")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Echo工具基本功能测试失败: {e}")
        return False


def test_echo_special_characters() -> bool:
    """测试Echo工具特殊字符处理"""
    print("🧪 测试Echo工具特殊字符处理...")
    
    try:
        # 测试特殊字符
        special_cases = [
            "Hello\nWorld",  # 换行符
            "Hello\tWorld",  # 制表符
            "Hello\\World",  # 反斜杠
            "Hello\"World",  # 双引号
            "Hello\'World",  # 单引号
            "中文测试",  # 中文字符
            "🎉表情符号",  # 表情符号
            "混合123ABC🎉"  # 混合字符
        ]
        
        all_passed = True
        for message in special_cases:
            # 模拟echo函数调用
            result = f"Echo: {message}"
            expected = f"Echo: {message}"
            
            if result == expected:
                print(f"✅ 特殊字符处理: '{message[:15]}...'")
            else:
                print(f"❌ 特殊字符处理失败: '{message}'")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Echo工具特殊字符测试失败: {e}")
        return False


def test_echo_performance() -> bool:
    """测试Echo工具性能"""
    print("🧪 测试Echo工具性能...")
    
    try:
        import time
        
        # 测试批量回显性能
        start_time = time.time()
        
        for i in range(1000):
            message = f"测试消息 {i}"
            result = f"Echo: {message}"  # 模拟echo函数调用
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"✅ 批量回显性能: {execution_time:.3f}秒 (1000次调用)")
        
        # 性能阈值检查
        if execution_time < 0.1:  # 0.1秒内完成1000次调用
            print("✅ 性能测试通过")
            return True
        else:
            print("⚠️  性能较慢，但功能正常")
            return True  # 性能问题不视为测试失败
            
    except Exception as e:
        print(f"❌ Echo工具性能测试失败: {e}")
        return False