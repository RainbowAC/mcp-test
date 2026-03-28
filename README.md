# 🚀 MCP 工具管理服务器

一个基于 MCP (Model Context Protocol) 协议的工具管理服务器，提供安全的工具注册、管理和执行功能。

## 🎯 核心特性

### 🔧 工具管理
- **安全工具执行**: 内置安全计算器，防止代码注入
- **动态工具发现**: 自动发现和注册MCP工具
- **分散式测试架构**: 测试用例与工具模块同位置管理
- **模块化设计**: 清晰的架构设计，易于扩展

### 🗄️ 数据管理
- **MySQL 数据库支持**: 完整的数据库连接池管理
- **连接池优化**: 智能连接池管理，支持重试机制
- **数据模型**: 完整的工具数据模型和CRUD操作

### 📊 系统监控
- **性能监控**: 实时系统性能指标监控
- **健康检查**: 内置健康检查端点
- **缓存系统**: 高性能缓存机制

### 🧪 测试系统
- **动态测试发现**: 自动发现分散的测试函数
- **交互式测试**: 支持命令行和交互式测试模式
- **测试分类**: 按功能分类的测试管理

---

## 🏗️ 系统架构

### 设计原则

#### 1. 模块化设计
- **单一职责**: 每个模块专注于特定功能
- **松耦合**: 模块间通过清晰接口通信
- **高内聚**: 相关功能集中在同一模块

#### 2. 分层架构
- **表现层**: MCP协议接口和HTTP端点
- **业务层**: 工具逻辑和业务规则
- **数据层**: 数据库操作和持久化

#### 3. 可扩展性
- **插件化**: 工具模块可动态加载
- **配置化**: 系统行为通过配置控制
- **标准化**: 统一的接口和协议

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP工具管理服务器架构                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐  │
│  │  客户端应用   │◄──►│   MCP协议接口    │◄──►│  工具注册中心  │  │
│  │ (AI助手等)   │    │                 │    │             │  │
│  └─────────────┘    └─────────────────┘    └─────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   业务逻辑层                            │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │  │
│  │  │  时间工具    │  │  计算器工具   │  │   工具管理器     │  │  │
│  │  │             │  │             │  │                │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   数据访问层                            │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │  │
│  │  │  连接管理    │  │  数据模型    │  │   缓存系统       │  │  │
│  │  │             │  │             │  │                │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   基础设施层                            │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │  │
│  │  │  MySQL数据库  │  │   配置管理    │  │   日志系统       │  │  │
│  │  │             │  │             │  │                │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 核心模块说明

#### 1. 配置管理模块 (`src/core/config.py`)
**职责**: 统一管理应用配置，支持环境变量和默认值

```python
class DevelopmentConfig:
    """开发环境配置类"""
    
    # 服务器配置
    SERVER_HOST: str = os.getenv("SERVER_HOST", "localhost")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "3000"))
    
    # 数据库配置
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "3306"))
    
    @property
    def DATABASE_URL(self) -> str:
        """动态生成数据库连接URL"""
        return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
```

#### 2. 服务器主入口 (`src/core/server.py`)
**职责**: 创建和配置MCP服务器实例

```python
def create_server() -> FastMCP:
    """创建并配置MCP服务器"""
    
    # 1. 创建服务器实例
    mcp = FastMCP(config.SERVER_NAME)
    
    # 2. 初始化数据库
    db_manager = DatabaseManager(config.DATABASE_URL)
    
    # 3. 注册工具
    register_all_tools(mcp, db_manager)
    
    # 4. 配置健康检查
    @mcp.resource("mcp://health")
    def health_check() -> dict:
        return {"status": "healthy"}
    
    return mcp
```

#### 3. 数据库连接管理 (`src/database/connection.py`)
**职责**: 管理数据库连接池和会话

```python
class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, database_url: str):
        # 创建连接引擎
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW
        )
        
        # 创建会话工厂
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
```

#### 4. 工具注册中心 (`src/tools/registry.py`)
**职责**: 统一管理工具注册过程

```python
def register_all_tools(mcp: FastMCP, db_manager: DatabaseManager) -> None:
    """注册所有工具"""
    
    # 注册简单工具（无依赖）
    register_echo_tool(mcp)
    register_calculator_tool(mcp)
    register_datetime_tool(mcp)
    
    # 注册管理工具（依赖数据库）
    register_tool_manager_tools(mcp, db_manager)
```

---

## 📦 项目结构

```
mcp-test/
├── src/                          # 源代码目录
│   ├── core/                     # 核心模块
│   │   ├── config.py            # 配置管理 - 环境变量和默认配置
│   │   └── server.py            # 服务器主入口 - MCP服务器创建和启动
│   ├── database/                # 数据库模块
│   │   ├── connection.py        # 连接管理 - 数据库连接池和会话管理
│   │   ├── models.py            # 数据模型 - ORM模型定义
│   │   └── operations.py        # 数据库操作 - CRUD操作封装
│   ├── tools/                   # 工具模块
│   │   ├── simple/              # 简单工具（无依赖）
│   │   │   ├── calculator.py    # 安全计算器 - 数学表达式计算
│   │   │   ├── datetime_tool.py # 时间日期工具 - 多时区时间处理
│   │   │   └── echo.py          # 回显工具 - 消息回显功能
│   │   ├── management/          # 管理工具（依赖数据库）
│   │   │   └── tool_manager.py  # 工具管理器 - 工具CRUD操作
│   │   └── registry.py          # 工具注册中心 - 统一工具注册
│   └── utils/                   # 工具类
│       ├── cache.py             # 缓存系统 - 高性能缓存机制
│       └── monitor.py           # 性能监控 - 系统性能指标
├── test.py                      # 主测试脚本 - 分散式测试架构
├── start.py                     # 启动脚本 - 服务器启动入口
├── init_mysql.py                # 数据库初始化 - 数据库表创建
└── requirements.txt             # 依赖管理 - Python包依赖
```

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+
- 虚拟环境支持

### 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置环境

复制 `.env.example` 文件并配置您的环境变量：

```bash
# 服务器配置
SERVER_HOST=localhost
SERVER_PORT=3000
SERVER_NAME=mcp-tool-server-dev

# MySQL 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=123456
DATABASE_NAME=mcp_dev

# 应用配置
DEBUG=true
LOG_LEVEL=DEBUG
SECRET_KEY=dev-secret-key-for-development
```

### 数据库初始化

```bash
# 初始化数据库
python init_mysql.py
```

### 启动服务器

```bash
# 开发环境启动
python start.py

# 或者直接运行
python -m src.core.server
```

---

## 🔧 可用工具

### 内置工具

#### 1. **安全计算器** (`calculator`)
- **功能**: 安全的数学表达式计算
- **特性**: 防止代码注入攻击，支持基本运算和复杂表达式
- **位置**: `src/tools/simple/calculator.py`

#### 2. **时间日期工具** (`datetime_tool`)
- **功能**: 多时区时间转换、时间戳格式化、时间差异计算
- **特性**: 支持全球主要时区，精确的时间计算
- **位置**: `src/tools/simple/datetime_tool.py`

#### 3. **回显工具** (`echo`)
- **功能**: 简单的消息回显
- **特性**: 特殊字符处理，性能优化
- **位置**: `src/tools/simple/echo.py`

#### 4. **工具管理器** (`tool_manager`)
- **功能**: 工具CRUD操作、搜索和统计
- **特性**: 数据库依赖，分类管理
- **位置**: `src/tools/management/tool_manager.py`

### 扩展工具

项目支持动态工具发现，新增工具只需在 `src/tools/` 目录下创建相应模块即可自动注册。

---

## 🧪 测试系统

项目采用先进的分散式测试架构，测试用例与工具模块同位置管理。

### 运行测试

```bash
# 运行所有测试
python test.py --all

# 运行指定工具测试
python test.py --test datetime_tool calculator

# 按分类运行测试
python test.py --category 工具功能

# 交互式测试模式
python test.py --interactive
```

### 测试特性

- **动态发现**: 自动发现工具模块中的测试函数
- **分散管理**: 测试用例与工具代码在一起
- **详细报告**: 完整的测试结果汇总
- **性能测试**: 内置性能基准测试

---

## 🔧 工具开发指南

### 开发原则

#### 1. 单一职责原则
- 每个工具专注于特定功能领域
- 避免工具功能过于复杂或重叠
- 保持工具接口简洁明了

#### 2. 接口一致性原则
- 遵循统一的工具注册模式
- 使用标准的参数和返回值格式
- 保持错误处理的一致性

#### 3. 测试驱动原则
- 工具与测试代码同位置管理
- 编写全面的测试用例
- 确保测试覆盖核心功能

### 开发流程

#### 1. 确定工具类型

**简单工具** (无外部依赖)
- 位置: `src/tools/simple/`
- 特点: 纯计算、无状态、无数据库依赖
- 示例: 计算器、时间工具、回显工具

**管理工具** (依赖数据库)
- 位置: `src/tools/management/`
- 特点: 数据操作、状态管理、数据库依赖
- 示例: 工具管理器、用户管理

#### 2. 创建工具模块

**简单工具模板**

```python
"""
MCP工具管理服务器 - [工具名称]工具模块

[工具功能描述]
[特性说明]
[使用示例]
"""

from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP


class [ToolName]Tool:
    """
    [工具名称]工具类
    
    [类功能描述]
    [方法说明]
    """
    
    @staticmethod
    def [method_name](param1: type, param2: type) -> Dict[str, any]:
        """
        [方法功能描述]
        
        Args:
            param1 (type): [参数说明]
            param2 (type): [参数说明]
            
        Returns:
            Dict[str, any]: [返回值说明]
        """
        # 方法实现
        pass


def register_[tool_name]_tool(mcp: FastMCP) -> None:
    """
    注册[工具名称]工具到MCP服务器
    
    Args:
        mcp (FastMCP): FastMCP服务器实例
    """
    
    @mcp.tool()
    def [tool_function](param1: type, param2: type) -> Dict[str, any]:
        """[工具函数描述]"""
        return [ToolName]Tool.[method_name](param1, param2)
```

#### 3. 添加测试函数

```python
# =============================================================================
# [工具名称]工具专用测试函数
# =============================================================================

def test_[tool_name]_functionality() -> bool:
    """测试[工具名称]工具的核心功能"""
    print("🧪 测试[工具名称]工具核心功能...")
    
    try:
        # 测试用例实现
        result = [ToolName]Tool.[method_name](test_value)
        assert "expected_field" in result, "功能测试失败"
        
        print("✅ [功能名称]功能正常")
        return True
        
    except Exception as e:
        print(f"❌ [工具名称]工具功能测试失败: {e}")
        return False
```

### 开发最佳实践

#### 1. 参数验证

```python
@staticmethod
def safe_method(param: str) -> Dict[str, any]:
    """安全的方法实现"""
    
    # 参数类型验证
    if not isinstance(param, str):
        return {"error": "参数类型错误"}
    
    # 参数内容验证
    if not param.strip():
        return {"error": "参数不能为空"}
    
    # 正常处理逻辑
    # ...
```

#### 2. 错误处理

```python
@staticmethod
def robust_method(param: str) -> Dict[str, any]:
    """健壮的方法实现"""
    
    try:
        # 业务逻辑
        result = do_something(param)
        
        return {
            "success": True,
            "data": result,
            "message": "操作成功"
        }
        
    except Exception as e:
        # 错误处理
        return {
            "success": False,
            "error": f"操作失败: {str(e)}",
            "error_type": "internal_error"
        }
```

---

## 📊 系统监控

### 健康检查

访问健康检查端点获取系统状态：

```bash
# 健康检查
GET /health

# 响应示例
{
  "status": "healthy",
  "server": "mcp-tool-server-dev",
  "environment": "development"
}
```

### 性能指标

系统内置性能监控，可通过日志查看：

```bash
# 查看性能日志
tail -f logs/performance.log
```

---

## 🐛 故障排除

### 常见问题

#### 1. **数据库连接失败**
- **原因**: MySQL服务未运行或配置错误
- **解决**: 检查MySQL服务，验证数据库配置信息
- **命令**: `python init_mysql.py` 初始化数据库

#### 2. **工具注册失败**
- **原因**: 工具模块导入路径错误或函数实现问题
- **解决**: 检查工具模块的导入路径，验证 `register_*_tool` 函数实现
- **查看**: 日志文件获取详细错误信息

#### 3. **测试失败**
- **原因**: 测试依赖未安装或环境配置问题
- **解决**: 检查测试依赖是否安装，验证测试环境配置
- **调试**: 使用 `--interactive` 模式进行调试

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log

# 查看性能日志
tail -f logs/performance.log
```

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下指南：

### 贡献流程

1. **Fork 项目**: 在GitHub上fork项目到您的账户
2. **创建分支**: 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交更改**: 提交您的更改 (`git commit -m 'Add amazing feature'`)
4. **推送到分支**: 推送分支到远程仓库 (`git push origin feature/amazing-feature`)
5. **创建 Pull Request**: 在GitHub上创建Pull Request

### 开发规范

- **代码风格**: 遵循 PEP 8 代码风格
- **文档注释**: 添加适当的文档和注释
- **测试用例**: 编写完整的测试用例
- **提交信息**: 使用清晰的提交信息
- **README 更新**: 更新相关文档

---
