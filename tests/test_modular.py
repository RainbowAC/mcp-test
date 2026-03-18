# test_modular.py
"""
测试模块化重构是否成功
"""

import os
import sys

# 添加项目根目录到路径
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from tools_module import ToolManager


def main():
    print("=" * 50)
    print("测试模块化工具管理器")
    print("=" * 50)
    
    # 创建管理器实例
    manager = ToolManager()
    
    # 测试 1: 列出所有工具
    print("\n1. 列出所有工具")
    tools = manager.list_all()
    print(f"   共有 {tools['count']} 个工具")
    assert tools['count'] == 4, "初始应该有 4 个工具"
    
    # 测试 2: 添加工具
    print("\n2. 添加新工具 (Machine Learning)")
    result = manager.add_tool("Machine Learning", 4, "AI")
    print(f"   结果：{result['message']}")
    assert result['success'] is True
    
    # 测试 3: 获取统计信息
    print("\n3. 获取统计信息")
    stats = manager.get_statistics()
    print(f"   总工具数：{stats['total_tools']}")
    print(f"   平均等级：{stats['average_level']}")
    assert stats['total_tools'] == 5, "现在应该有 5 个工具"
    
    # 测试 4: 按类别筛选
    print("\n4. 按类别筛选 (Programming)")
    prog_tools = manager.list_by_category("Programming")
    print(f"   Programming 类别有 {prog_tools['count']} 个工具")
    assert prog_tools['count'] == 2, "Programming 应该有 2 个工具"
    
    # 测试 5: 更新工具
    print("\n5. 更新工具等级 (Machine Learning)")
    result = manager.update_tool("Machine Learning", level=5)
    print(f"   结果：{result['message']}")
    assert result['tool']['level'] == 5
    
    # 测试 6: 删除工具
    print("\n6. 删除工具 (Machine Learning)")
    result = manager.delete_tool("Machine Learning")
    print(f"   结果：{result['message']}")
    assert result['success'] is True
    
    # 测试 7: 验证删除
    print("\n7. 验证删除")
    result = manager.get_tool("Machine Learning")
    print(f"   结果：{result['message']}")
    assert result['found'] is False
    
    # 测试 8: 获取类别
    print("\n8. 获取所有类别")
    categories = manager.get_categories()
    print(f"   共有 {categories['count']} 个类别：{', '.join(categories['categories'])}")
    assert categories['count'] == 2, "应该有 2 个类别 (Programming, DevOps)"
    
    # 测试 9: 搜索工具
    print("\n9. 搜索工具 (关键词: Python)")
    result = manager.search_tools("Python")
    print(f"   找到 {result['count']} 个工具")
    assert result['count'] >= 0
    assert "tools" in result
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)


if __name__ == "__main__":
    main()
