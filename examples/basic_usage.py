# examples/basic_usage.py
"""
基础使用示例
演示 ToolManager 的基本操作
"""

import os
import sys

# 添加项目根目录到路径
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from tools_module import ToolManager


def main():
    # 创建工具管理器实例
    manager = ToolManager()
    
    print("=" * 50)
    print("1. 列出所有工具")
    print("=" * 50)
    tools = manager.list_all()
    print(f"共有 {tools['count']} 个工具:")
    for tool in tools['tools']:
        print(f"  - {tool['name']} (Level: {tool['level']}, {tool['category']})")
    
    print("\n" + "=" * 50)
    print("2. 按类别筛选工具 (Programming)")
    print("=" * 50)
    prog_tools = manager.list_by_category("Programming")
    print(f"Programming 类别有 {prog_tools['count']} 个工具:")
    for tool in prog_tools['tools']:
        print(f"  - {tool['name']} (Level: {tool['level']})")
    
    print("\n" + "=" * 50)
    print("3. 获取特定工具")
    print("=" * 50)
    python_tool = manager.get_tool("Python")
    if python_tool['found']:
        tool = python_tool['tool']
        print(f"找到工具：{tool['name']}, 等级：{tool['level']}, 类别：{tool['category']}")
    
    print("\n" + "=" * 50)
    print("4. 添加新工具")
    print("=" * 50)
    result = manager.add_tool("Machine Learning", 4, "AI")
    print(result['message'])
    
    print("\n" + "=" * 50)
    print("5. 更新工具等级")
    print("=" * 50)
    result = manager.update_tool("Machine Learning", level=5)
    print(result['message'])
    print(f"更新后的等级：{result['tool']['level']}")
    
    print("\n" + "=" * 50)
    print("6. 获取所有类别")
    print("=" * 50)
    categories = manager.get_categories()
    print(f"共有 {categories['count']} 个类别：{', '.join(categories['categories'])}")
    
    print("\n" + "=" * 50)
    print("7. 获取统计信息")
    print("=" * 50)
    stats = manager.get_statistics()
    print(f"总工具数：{stats['total_tools']}")
    print(f"平均等级：{stats['average_level']}")
    print("按类别统计:")
    for category, data in stats['by_category'].items():
        print(f"  {category}: {data['count']} 个工具，平均等级 {data['avg_level']}")
    
    print("\n" + "=" * 50)
    print("8. 删除工具")
    print("=" * 50)
    result = manager.delete_tool("Machine Learning")
    print(result['message'])
    
    print("\n" + "=" * 50)
    print("9. 验证删除")
    print("=" * 50)
    result = manager.get_tool("Machine Learning")
    print(f"查找结果：{result['message']}")


if __name__ == "__main__":
    main()
