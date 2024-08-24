#!/bin/bash

# 配置项
SERVER_USER="root"
SERVER_IP="47.95.172.141"
REQUIREMENTS_PATH="SEGroup6/requirements.txt"
FRONTEND_PATH="SEGroup6/猫猫就诊/Project/frontend/dist"  # 前端静态文件的部署路径
BACKEND_PATH="SEGroup6/猫猫就诊/Project/django"    # 后端代码的部署路径
UWSGI_SERVICE_NAME="uwsgi"  # uWSGI 服务名
NGINX_SERVICE_NAME="nginx"  # Nginx 服务名
UWSGI_INI_PATH="uwsgi.ini"  # uWSGI 的 ini 文件路径
SSH_PASSWORD="22373005Se"  # 

# 安装 sshpass 工具

# echo "checkout branch"
# sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP << EOF
#     cd SEGroup6
#     git reset --hard
#     git clean -fd
#     git checkout mic_lyx
#     cd ..
# EOF

# sudo apt-get update && sudo apt-get install -y sshpass
echo "Copying Other files"
#sshpass -p "$SSH_PASSWORD" scp -o StrictHostKeyChecking=no  ./猫猫就诊/Project/uwsgi.ini $SERVER_USER@$SERVER_IP:/home/ubuntu/Project/uwsgi.ini
# 前端部署
#sshpass -p "$SSH_PASSWORD" scp -o StrictHostKeyChecking=no -r ./猫猫就诊/Project/frontend/dist/* $SERVER_USER@$SERVER_IP:$FRONTEND_PATH
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/frontend/dist/ $SERVER_USER@$SERVER_IP:$FRONTEND_PATH
# 后端部署
echo "Starting back-end deployment..."
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/administrator_service/ $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/administrator_service
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/doctor_service/ $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/doctor_service
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/user_service/ $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/user_service
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/patient_service/ $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/patient_service
echo "传dockerfile和配置文件"
# sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/doctor_service/Dockerfile $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/doctor_service/Dockerfile
# sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/user_service/Dockerfile $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/user_service/Dockerfile
# sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/patient_service/Dockerfile $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/patient_service/Dockerfile
# sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/administrator_service/Dockerfile $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/administrator_service/Dockerfile
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/Dockerfile $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/Dockerfile
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/requirements.txt $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/requirements.txt
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/frontend/Dockerfile $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/frontend/Dockerfile
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/frontend/nginx.conf $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/frontend/nginx.conf
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/frontend/default.conf $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/frontend/default.conf
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/frontend/uwsgi_params $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/frontend/uwsgi_params
sshpass -p "$SSH_PASSWORD" rsync -avz -e "ssh -o StrictHostKeyChecking=no" --progress ./猫猫就诊/Project/docker-compose.yml $SERVER_USER@$SERVER_IP:SEGroup6/猫猫就诊/Project/docker-compose.yml
# SSH 到服务器上，执行后续命令
echo "Connecting to server to finalize deployment..."
sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP << EOF
    # 进入后端项目目录

    cd SEGroup6/猫猫就诊/Project
    ls
    # echo "$SSH_PASSWORD" | sudo killall -9 uwsgi
    # echo "$SSH_PASSWORD" | sudo killall -9 nginx
    echo "$SSH_PASSWORD" | docker-compose down
    echo "$SSH_PASSWORD" | docker build -t my-django-app .
    echo "$SSH_PASSWORD" | docker-compose build --no-cache
    echo "$SSH_PASSWORD" | docker-compose up -d --remove-orphans




    # 重启 uWSGI 和 Nginx 服务
    #echo "启动 uWSGI 和nginx服务..."
    #echo "$SSH_PASSWORD" | sudo -S killall -9 uwsgi
    #pwd
    #ls
    
    #echo "$SSH_PASSWORD" | sudo uwsgi --ini uwsgi.ini
    #echo "$SSH_PASSWORD" | sudo nginx -s reload

    #sudo /etc/init.d/uwsgi restart
    #sudo systemctl restart $NGINX_SERVICE_NAME
    #echo "Deployment completed successfully!"
EOF