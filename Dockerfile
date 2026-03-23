# 使用官方Python运行时作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目源代码
COPY . .

# 暴露端口
EXPOSE 3000

# 设置默认环境变量
ENV ENVIRONMENT=production
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=3000

# 启动命令
CMD ["python", "server.py"]