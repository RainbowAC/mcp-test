# MCP Tool Management Service

一个基于 **MCP**（Modular Code Platform）的工具管理示例服务，支持通过 MCP 工具接口对"工具"进行增删改查、分类筛选与统计分析。

---

## ✅ 项目结构

```
mcp-test/
├── server.py               # MCP 服务器入口，注册工具和资源
├── tools/                  # 独立工具模块目录
│   ├── __init__.py         # 工具包初始化
│   ├── registry.py         # 工具注册中心
│   ├── echo.py             # Echo 工具
│   ├── calculate.py        # 计算工具
│   ├── list_tools.py       # 列出工具
│   ├── add_tool.py         # 添加工具
│   ├── get_tool_level.py   # 获取工具等级
│   ├── search_tools.py     # 搜索工具
│   ├── update_tool.py      # 更新工具
│   ├── delete_tool.py      # 删除工具
│   ├── get_categories.py   # 获取类别
│   └── get_statistics.py   # 获取统计信息
├── tools_module/           # 工具管理核心模块
│   ├── __init__.py         # 包含导出接口（ToolManager 等）
│   ├── models.py           # 数据模型（Tool、ToolStatistics）
│   ├── database.py         # 数据存储层（内存实现）
│   ├── manager.py          # 业务逻辑层/接口
│   └── utils.py            # 通用工具（格式化、统计、标准化等）
├── examples/               # 使用示例
│   └── basic_usage.py
└── tests/                  # 测试目录
    ├── conftest.py         # pytest 配置：添加项目根到 sys.path
    ├── test_client.py      # 通过 MCP 客户端测试业务功能
    ├── test_mcp_pytest.py  # pytest 异步自动化测试
    └── test_modular.py     # 直接测试 ToolManager 模块
```

---

## 🏗️ 工具模块化架构

项目采用模块化设计，每个工具都作为独立的 Python 文件：

### 工具注册机制
- **tools/registry.py**: 统一注册所有工具到 MCP 服务器
- **server.py**: 只负责服务器初始化和工具注册，不包含具体工具逻辑
- **tools/*.py**: 每个工具一个独立文件，便于维护和扩展

### 工具开发模式
```python
# tools/your_tool.py
from mcp.server.fastmcp import FastMCP
from tools_module import ToolManager

def register_your_tool_tool(mcp: FastMCP, tool_manager: ToolManager):
    @mcp.tool()
    def your_tool(param: str) -> dict:
        """Your tool description"""
        return tool_manager.your_business_logic(param)
```

然后在 `tools/registry.py` 中注册：
```python
from . import your_tool

def register_all_tools(mcp: FastMCP, tool_manager: ToolManager):
    your_tool.register_your_tool_tool(mcp, tool_manager)
    # ... 其他工具注册
```

---

## 🚀 快速开始

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 运行 MCP 服务器

```bash
python server.py
```

服务器启动后，你可以通过 MCP 客户端调用以下工具：

- `echo(message: str)`
- `calculate(expression: str)`
- `list_tools(category: str = None)`
- `add_tool(name: str, level: int, category: str)`
- `get_tool_level(tool_name: str)`
- `update_tool(name: str, level: int = None, category: str = None)`
- `delete_tool(name: str)`
- `get_categories()`
- `get_statistics()`

此外，还提供一个资源：
- `test://data/sample`

---

## 🧪 运行测试

```bash
pytest -q
```

> ✅ 所有测试应当通过（包括 MCP 工具端到端测试）。

---

## 🧩 代码使用示例（本地模块调用）

```python
from tools_module import ToolManager

manager = ToolManager()
print(manager.list_all())

manager.add_tool("Machine Learning", 5, "AI")
print(manager.get_statistics())
```

---

## 📌 说明 & 扩展方向

- 当前数据存储为内存实现，重启后数据会丢失
- 可扩展：增加持久化存储（JSON/SQLite/数据库）、权限控制、REST/HTTP 接口
- 联系方式：可在此项目基础上集成到更大的 MCP 服务中
