# 使用官方的 Python 镜像作为基础镜像
FROM python:3.8

# 设置 pip 使用清华源
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt /app/

# 安装项目所需的依赖
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app