# MCP 工具管理服务器

一个基于 MCP (Model Context Protocol) 协议的工具管理服务器，提供安全的工具注册、管理和执行功能。

## 🚀 特性

- **安全工具执行**: 内置安全计算器，防止代码注入
- **MySQL 数据库支持**: 完整的数据库连接池管理
- **性能监控**: 实时系统性能指标监控
- **连接池优化**: 智能连接池管理，支持重试机制
- **模块化设计**: 清晰的架构设计，易于扩展

## 📦 安装依赖

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

## ⚙️ 配置

### 环境变量配置

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

## 🚀 启动服务器

```bash
# 开发环境启动
python start.py

# 或者直接运行
python -m src.core.server
```

## 🧪 测试

```bash
# 运行所有测试
python -m pytest test.py -v

# 运行测试并生成覆盖率报告
python -m pytest test.py --cov=src --cov-report=html
```

## 📊 性能监控

服务器内置性能监控功能，可以通过以下方式访问：

- **健康检查**: `GET /health`
- **性能指标**: `GET /metrics`

## 🔧 开发工具

### 代码格式化

```bash
# 使用 black 格式化代码
black src/

# 使用 flake8 检查代码质量
flake8 src/

# 使用 mypy 进行类型检查
mypy src/
```

### 项目结构

```
src/
├── core/           # 核心模块
│   ├── config.py  # 配置管理
│   └── server.py  # 服务器入口
├── database/       # 数据库模块
│   ├── connection.py  # 数据库连接管理
│   ├── models.py      # 数据模型
│   └── operations.py  # 数据库操作
├── tools/          # 工具模块
│   ├── registry.py    # 工具注册
│   ├── simple/        # 简单工具
│   └── management/    # 工具管理
└── utils/          # 工具函数
    ├── cache.py    # 缓存管理
    └── monitor.py  # 性能监控
```

## 🔒 安全特性

- **输入验证**: 所有用户输入都经过严格验证
- **安全计算**: 计算器工具限制危险表达式执行
- **连接池安全**: 数据库连接池配置安全参数
- **错误处理**: 完善的错误处理和日志记录

## 📈 性能优化

- **连接池**: 智能连接池管理，支持连接复用
- **缓存**: 内存缓存系统，减少数据库访问
- **监控**: 实时性能监控和告警
- **重试机制**: 数据库操作失败自动重试

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License