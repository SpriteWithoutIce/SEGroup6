#!/bin/bash

# 配置项
SERVER_USER="ubuntu"
SERVER_IP="101.42.36.160"
REQUIREMENTS_PATH="SEGroup6/requirements.txt"
FRONTEND_PATH="SEGroup6/猫猫就诊/Project/frontend/dist"  # 前端静态文件的部署路径
BACKEND_PATH="SEGroup6/猫猫就诊/Project/backend"    # 后端代码的部署路径
UWSGI_SERVICE_NAME="uwsgi"  # uWSGI 服务名
NGINX_SERVICE_NAME="nginx"  # Nginx 服务名
SSH_PASSWORD="22371468Se"  # SSH 密码

# 安装 sshpass 工具
sudo apt-get update && sudo apt-get install -y sshpass

# 前端部署
echo "Starting requirement deployment"
sshpass -p "$SSH_PASSWORD" scp -o StrictHostKeyChecking=no ./requirements.txt $SERVER_USER@$SERVER_IP:$REQUIREMENTS_PATH
echo "Starting front-end deployment..."
sshpass -p "$SSH_PASSWORD" scp -o StrictHostKeyChecking=no -r ./猫猫就诊/Project/frontend/dist/* $SERVER_USER@$SERVER_IP:$FRONTEND_PATH

# 后端部署
echo "Starting back-end deployment..."
sshpass -p "$SSH_PASSWORD" scp -o StrictHostKeyChecking=no -r ./猫猫就诊/Project/backend/* $SERVER_USER@$SERVER_IP:$BACKEND_PATH

# SSH 到服务器上，执行后续命令
echo "Connecting to server to finalize deployment..."
sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP << EOF
    # 进入后端项目目录
    cd $BACKEND_PATH

    # 激活虚拟环境
    source venv/bin/activate

    # 安装后端依赖
    pip install -r requirements.txt
    
    # 迁移数据库（如果使用 Django）
    python manage.py migrate --noinput
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    
    # 收集静态文件（如果使用 Django）
    python manage.py collectstatic --noinput

    # 确保 uWSGI 已安装
    pip install uwsgi

    # 创建 uWSGI 服务单元文件（如果不存在）
    if [ ! -f /etc/systemd/system/$UWSGI_SERVICE_NAME.service ]; then
        echo "Creating uWSGI service unit file..."
        sudo tee /etc/systemd/system/$UWSGI_SERVICE_NAME.service << EOL
[Unit]
Description=uWSGI instance to serve myproject
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$BACKEND_PATH
ExecStart=/usr/local/bin/uwsgi --ini $BACKEND_PATH/uwsgi.ini

[Install]
WantedBy=multi-user.target

EOL
        sudo systemctl daemon-reload
        sudo systemctl enable $UWSGI_SERVICE_NAME
    fi

    # 启动或重启 uWSGI 和 Nginx 服务
    sudo systemctl restart $UWSGI_SERVICE_NAME
    sudo systemctl restart $NGINX_SERVICE_NAME

    echo "Deployment completed successfully!"
EOF
