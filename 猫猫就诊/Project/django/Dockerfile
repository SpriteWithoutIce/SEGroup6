# 使用官方的 Python 镜像作为基础镜像
FROM python:3.8

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
# # 设置工作目录
WORKDIR /app
# 设置 pip 使用清华源
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# 将当前目录下的所有文件复制到工作目录
COPY . /app/

# 安装项目所需的依赖
RUN pip install django-cors-headers
RUN pip install Pillow
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将容器内的端口暴露出来，这里使用 Django 默认的端口 8000
EXPOSE 8000

# 启动 Django 项目
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
