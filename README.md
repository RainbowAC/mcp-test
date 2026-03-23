# MCP Production Server - 工具管理服务器

基于 FastMCP 构建的生产就绪技能管理 API 服务器，支持多种数据库后端和环境配置。

## 项目概述

本项目是一个基于 MCP (Model Context Protocol) 的技能管理服务器，提供了一套完整的工具管理和 API 接口。服务器支持多种数据库后端，具有灵活的配置选项，并可轻松部署到不同环境中。

## 功能特性

- 基于 FastMCP 框架构建
- 支持多种数据库后端（MySQL、SQLite 等）
- 灵活的环境配置管理
- 完整的工具管理系统
- 性能监控功能
- Docker 容器化部署支持
- RESTful API 接口

## 项目结构

```
mcp-test/
├── server.py             # 主服务器入口
├── config.py             # 配置管理
├── requirements.txt      # 项目依赖
├── Dockerfile           # Docker 构建文件
├── tools/               # 工具注册模块
│   ├── registry.py
│   └── ...              # 各种工具实现
├── tools_module/        # 工具管理模块
│   ├── __init__.py
│   ├── models.py        # 数据模型
│   ├── database.py      # 数据库操作
│   ├── manager.py       # 业务逻辑管理器
│   └── ...
├── .env.development     # 开发环境配置
├── .env.production      # 生产环境配置
├── install.sh           # Linux/Mac 安装脚本
├── install.bat          # Windows 安装脚本
├── start.bat            # Windows 启动脚本
└── mcp_dev.db           # SQLite 开发数据库
```

## 依赖项

- Python >= 3.8
- mcp >= 1.0.0
- PyMySQL >= 1.0.2
- SQLAlchemy >= 2.0.0
- psutil >= 5.8.0
- python-dotenv >= 1.0.0
- gunicorn >= 21.2.0 (生产环境)
- uvicorn >= 0.24.0

## 环境配置

### 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `ENVIRONMENT` | `development` | 运行环境 (`development`, `staging`, `production`) |
| `SERVER_HOST` | `0.0.0.0` | 服务器主机地址 |
| `SERVER_PORT` | `3000` | 服务器端口 |
| `DATABASE_HOST` | `localhost` | 数据库主机地址 |
| `DATABASE_PORT` | `3306` | 数据库端口 |
| `DATABASE_USER` | `root` | 数据库用户名 |
| `DATABASE_PASSWORD` | `123456` | 数据库密码 |
| `DATABASE_NAME` | `mcp_platform` | 数据库名称 |
| `DATABASE_URL_FORMAT` | `mysql+pymysql://...` | 数据库 URL 格式 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `DEBUG` | `False` | 调试模式开关 |
| `SECRET_KEY` | `dev-secret-key-...` | 密钥 (生产环境需修改) |
| `POOL_SIZE` | `10` | 连接池大小 |
| `MAX_OVERFLOW` | `20` | 连接池溢出数量 |

## 安装与启动

### 方法一：本地安装

1. 克隆或下载项目
2. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\\Scripts\\activate   # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 启动服务器：
   ```bash
   python server.py
   ```

### 方法二：使用安装脚本

- Linux/Mac:
  ```bash
  chmod +x install.sh
  ./install.sh
  ```

- Windows:
  ```cmd
  install.bat
  ```

### 方法三：Docker 部署

```bash
# 构建镜像
docker build -t mcp-production-server .

# 运行容器
docker run -d -p 3000:3000 mcp-production-server
```

## API 接口

服务器提供了以下主要接口：

- `mcp://data/sample` - 示例数据资源
- `mcp://health` - 健康检查接口，返回服务器状态信息
- 各种工具管理接口（通过注册的工具提供）

## 工具管理功能

服务器集成了完整的工具管理系统，包括：

- 工具列表查询
- 工具添加/更新/删除
- 工具搜索功能
- 统计信息获取
- 性能监控
- 分类管理

## 配置说明

项目支持三种环境配置：

1. **开发环境** (`DevelopmentConfig`)
   - 启用调试模式
   - 使用 SQLite 作为默认数据库
   - 更详细的日志输出

2. **预发布环境** (`StagingConfig`)
   - 关闭调试模式
   - 中等详细度的日志输出
   - 可自定义预发布数据库配置

3. **生产环境** (`ProductionConfig`)
   - 强制要求设置 `SECRET_KEY`
   - 关闭调试模式
   - 较少的日志输出
   - 优化的性能配置

## 安全注意事项

- 在生产环境中务必更改默认的 `SECRET_KEY`
- 不要在版本控制中提交敏感的环境配置文件
- 使用强密码保护数据库访问
- 限制服务器的网络访问权限

## 部署建议

1. 使用环境变量而非硬编码配置
2. 在生产环境中使用反向代理（如 Nginx）
3. 定期备份数据库
4. 监控服务器性能和资源使用情况
5. 使用进程管理器（如 systemd 或 supervisor）管理服务
