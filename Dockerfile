# 构建阶段
FROM --platform=$BUILDPLATFORM python:3.11-slim AS builder

# 设置构建参数
ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETOS
ARG TARGETARCH

# 设置工作目录
WORKDIR /build

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 根据目标平台安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 最终阶段
FROM --platform=$TARGETPLATFORM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 设置环境变量
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

# 创建必要的目录
RUN mkdir -p data/config data/log

# 复制应用文件
COPY alist-sync-web.py .
COPY alist_sync.py .
COPY templates/ templates/
COPY static/ static/

# 暴露端口
EXPOSE 52441

# 启动命令
CMD ["uvicorn", "alist-sync-web:app", "--host", "0.0.0.0", "--port", "52441"] 