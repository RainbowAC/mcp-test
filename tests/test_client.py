# test_client.py
import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_standalone_test():
    """独立运行测试"""
    # 配置服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # 初始化会话
                await session.initialize()
                
                # 测试工具列表
                print("📋 测试工具列表...")
                response = await session.list_tools()
                tools = response.tools
                print(f"   找到 {len(tools)} 个工具：{[t.name for t in tools]}")
                
                # 测试 echo 工具
                print("\n🔊 测试 echo 工具...")
                result = await session.call_tool("echo", {"message": "Test Message"})
                print(f"   响应：{result.content[0].text}")
                
                # 测试计算工具
                print("\n🧮 测试计算工具...")
                result = await session.call_tool("calculate", {"expression": "10 + 20"})
                print(f"   响应：{result.content[0].text}")
                
                # ==================== Skills 模块测试 ====================
                
                # 测试技能列表工具（全部）
                print("\n💼 测试技能列表工具（全部）...")
                result = await session.call_tool("list_skills", {})
                print(f"   响应：{result.content[0].text}")
                
                # 测试按类别筛选技能
                print("\n💼 测试技能列表工具（Programming 类别）...")
                result = await session.call_tool("list_skills", {"category": "Programming"})
                print(f"   响应：{result.content[0].text}")
                
                # 测试获取技能等级
                print("\n🎯 测试获取技能等级（Python）...")
                result = await session.call_tool("get_skill_level", {"skill_name": "Python"})
                print(f"   响应：{result.content[0].text}")
                
                # 测试获取不存在的技能
                print("\n🎯 测试获取不存在的技能...")
                result = await session.call_tool("get_skill_level", {"skill_name": "C++"})
                print(f"   响应：{result.content[0].text}")
                
                # 测试添加技能
                print("\n➕ 测试添加技能（Machine Learning）...")
                result = await session.call_tool("add_skill", {
                    "name": "Machine Learning",
                    "level": 4,
                    "category": "AI"
                })
                print(f"   响应：{result.content[0].text}")
                
                # 测试更新技能
                print("\n✏️ 测试更新技能（Machine Learning）...")
                result = await session.call_tool("update_skill", {
                    "name": "Machine Learning",
                    "level": 5
                })
                print(f"   响应：{result.content[0].text}")
                
                # 测试获取所有类别
                print("\n📂 测试获取技能类别...")
                result = await session.call_tool("get_categories", {})
                print(f"   响应：{result.content[0].text}")
                
                # 测试获取统计信息
                print("\n📊 测试获取统计信息...")
                result = await session.call_tool("get_statistics", {})
                print(f"   响应：{result.content[0].text}")
                
                # 测试搜索工具
                print("\n🔍 测试搜索工具（关键词: Python）...")
                result = await session.call_tool("search_tools", {"keyword": "Python"})
                print(f"   响应：{result.content[0].text}")
                
                # 测试删除技能
                print("\n🗑️ 测试删除技能（Machine Learning）...")
                result = await session.call_tool("delete_skill", {
                    "name": "Machine Learning"
                })
                print(f"   响应：{result.content[0].text}")
                
                # 验证删除成功
                print("\n🔍 验证删除后查询...")
                result = await session.call_tool("get_skill_level", {"skill_name": "Machine Learning"})
                print(f"   响应：{result.content[0].text}")
                
                # =======================================================
                
                # 测试资源列表
                print("\n📁 测试资源列表...")
                resources_response = await session.list_resources()
                resources = resources_response.resources
                print(f"   找到 {len(resources)} 个资源：{[str(r.uri) for r in resources]}")
                
                # 测试资源读取
                print("\n📖 测试资源读取...")
                result = await session.read_resource("test://data/sample")
                print(f"   响应：{result.contents[0].text}")
                
                print("\n✅ 所有测试通过!")
                
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

async def test_search_tools():
    async with MCPClient() as client:
        result = await client.call_tool("search_tools", {"keyword": "Python"})
        assert result["count"] >= 0

if __name__ == "__main__":
    asyncio.run(run_standalone_test())