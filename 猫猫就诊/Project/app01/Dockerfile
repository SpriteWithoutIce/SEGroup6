# 使用的是基于python3.8.2的Linux的镜像 该Python基于Linux-Debian系统
FROM python:3.8
# RUN 执行一个命令 在我们要构建的镜像里递归创建一个文件夹
RUN mkdir /data/prj/ginet -p
# 然后将当前Dockerfile位于的目录里的所有文件复制到之前在镜像里创建的那个文件里
COPY . /data/prj/ginet
# 指明面的命令的工作目录
WORKDIR /data/prj/ginet
# 更新pip版本
RUN pip install --upgrade pip
# 换成清华的镜像源 下载要快一些
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 安装requirements.txt文件里写的依赖项
RUN pip install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/
# 指明工作目录
WORKDIR /data/prj/ginet
# CMD在镜像启动时执行的命令 在这里就是以8000端口启动Django项目
CMD python manage.py runserver 0.0.0.0:8000




