# test_mcp_pytest.py
import asyncio
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

class TestMCPServer:
    """MCP Server 测试类"""
    
    def _get_server_params(self):
        """获取服务器参数"""
        return StdioServerParameters(
            command="python",
            args=["server.py"]
        )
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """测试工具列表"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                response = await session.list_tools()
                tools = response.tools
                assert len(tools) >= 8
                tool_names = [t.name for t in tools]
                assert "echo" in tool_names
                assert "calculate" in tool_names
                assert "list_tools" in tool_names
                assert "add_tool" in tool_names
                assert "get_tool_level" in tool_names
                assert "update_tool" in tool_names
                assert "delete_tool" in tool_names
                assert "get_categories" in tool_names
                assert "get_statistics" in tool_names
    
    @pytest.mark.asyncio
    async def test_echo_tool(self):
        """测试 echo 工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool(
                    name="echo",
                    arguments={"message": "Hello MCP"}
                )
                assert len(result.content) > 0
                assert "Hello MCP" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_calculate_tool(self):
        """测试计算工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool(
                    name="calculate",
                    arguments={"expression": "2 + 3 * 4"}
                )
                assert len(result.content) > 0
                assert "14" in result.content[0].text
    
    # ==================== Tools 模块测试 ====================
    
    @pytest.mark.asyncio
    async def test_list_tools_all(self):
        """测试列出所有工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("list_tools", {})
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert "tools" in data
                assert "count" in data
                assert data["count"] >= 4
    
    @pytest.mark.asyncio
    async def test_list_tools_by_category(self):
        """测试按类别筛选工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("list_tools", {"category": "Programming"})
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert "tools" in data
                for tool in data["tools"]:
                    assert tool["category"] == "Programming"
    
    @pytest.mark.asyncio
    async def test_get_tool_level_found(self):
        """测试获取存在的工具等级"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("get_tool_level", {"tool_name": "Python"})
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert data["found"] is True
                assert "tool" in data
                assert data["tool"]["name"] == "Python"
    
    @pytest.mark.asyncio
    async def test_get_tool_level_not_found(self):
        """测试获取不存在的工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("get_tool_level", {"tool_name": "NonExistentTool"})
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert data["found"] is False
                assert "not found" in data["message"].lower()
    
    @pytest.mark.asyncio
    async def test_add_tool_success(self):
        """测试添加成功"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("add_tool", {
                    "name": "Test Tool",
                    "level": 3,
                    "category": "Testing"
                })
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert data["success"] is True
                assert "added successfully" in data["message"]
    
    @pytest.mark.asyncio
    async def test_add_tool_duplicate(self):
        """测试添加重复工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # 先添加一个工具
                await session.call_tool("add_tool", {
                    "name": "Duplicate Test",
                    "level": 2,
                    "category": "Test"
                })
                
                # 再次添加同名工具
                result = await session.call_tool("add_tool", {
                    "name": "Duplicate Test",
                    "level": 3,
                    "category": "Test"
                })
                data = json.loads(result.content[0].text)
                assert data["success"] is False
                assert "already exists" in data["message"]
    
    @pytest.mark.asyncio
    async def test_update_tool_success(self):
        """测试更新工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # 先添加工具
                await session.call_tool("add_tool", {
                    "name": "Update Test",
                    "level": 2,
                    "category": "Test"
                })
                
                # 更新工具等级
                result = await session.call_tool("update_tool", {
                    "name": "Update Test",
                    "level": 5
                })
                data = json.loads(result.content[0].text)
                assert data["success"] is True
                assert data["tool"]["level"] == 5
    
    @pytest.mark.asyncio
    async def test_update_tool_not_found(self):
        """测试更新不存在的工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("update_tool", {
                    "name": "NonExistent",
                    "level": 3
                })
                data = json.loads(result.content[0].text)
                assert data["success"] is False
                assert "not found" in data["message"].lower()
    
    @pytest.mark.asyncio
    async def test_delete_tool_success(self):
        """测试删除工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # 先添加工具
                await session.call_tool("add_tool", {
                    "name": "Delete Test",
                    "level": 2,
                    "category": "Test"
                })
                
                # 删除工具
                result = await session.call_tool("delete_tool", {
                    "name": "Delete Test"
                })
                data = json.loads(result.content[0].text)
                assert data["success"] is True
                assert "deleted successfully" in data["message"].lower()
    
    @pytest.mark.asyncio
    async def test_delete_tool_not_found(self):
        """测试删除不存在的工具"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("delete_tool", {
                    "name": "NonExistent"
                })
                data = json.loads(result.content[0].text)
                assert data["success"] is False
                assert "not found" in data["message"].lower()
    
    @pytest.mark.asyncio
    async def test_get_categories(self):
        """测试获取所有类别"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("get_categories", {})
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert "categories" in data
                assert "count" in data
                assert len(data["categories"]) >= 2
                assert "Programming" in data["categories"]
                assert "DevOps" in data["categories"]
    
    @pytest.mark.asyncio
    async def test_get_statistics(self):
        """测试获取统计信息"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.call_tool("get_statistics", {})
                assert len(result.content) > 0
                data = json.loads(result.content[0].text)
                assert "total_tools" in data
                assert "average_level" in data
                assert "by_category" in data
                assert data["total_tools"] >= 4
    
    # =======================================================
    
    @pytest.mark.asyncio
    async def test_list_resources(self):
        """测试资源列表"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                response = await session.list_resources()
                resources = response.resources
                assert len(resources) >= 1
                uris = [str(r.uri) for r in resources]
                assert "test://data/sample" in uris
    
    @pytest.mark.asyncio
    async def test_read_resource(self):
        """测试资源读取"""
        server_params = self._get_server_params()
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                result = await session.read_resource("test://data/sample")
                assert len(result.contents) > 0
                assert "sample data" in result.contents[0].text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])