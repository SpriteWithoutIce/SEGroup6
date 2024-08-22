# 设置基础镜像
FROM nginx
# 将dist文件中的内容复制到 /usr/share/nginx/html/ 这个目录下面
RUN npm install
COPY . /app
RUN npm run build
COPY dist  /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
COPY uwsgi_params /etc/nginx/uwsgi_params
EXPOSE 80