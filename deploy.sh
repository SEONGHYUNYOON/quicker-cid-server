#!/bin/bash

# Ubuntu 서버 배포 스크립트
echo "=== Quicker CID Server 배포 시작 ==="

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 및 필수 패키지 설치
sudo apt install -y python3 python3-pip python3-venv nginx git

# 프로젝트 클론
cd /home/ubuntu
git clone https://github.com/[YOUR_USERNAME]/quicker-cid-server.git
cd quicker-cid-server

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
export FLASK_ENV=production
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')

# 데이터베이스 초기화
python3 -c "from main import app, db; app.app_context().push(); db.create_all()"

# Gunicorn 설치 및 실행 테스트
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 main:app --daemon

# systemd 서비스 등록
sudo tee /etc/systemd/system/quicker.service > /dev/null <<EOF
[Unit]
Description=Quicker CID Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/quicker-cid-server
Environment=PATH=/home/ubuntu/quicker-cid-server/venv/bin
Environment=FLASK_ENV=production
Environment=SECRET_KEY=$SECRET_KEY
ExecStart=/home/ubuntu/quicker-cid-server/venv/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable quicker
sudo systemctl start quicker

# Nginx 설정
sudo tee /etc/nginx/sites-available/quicker > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Nginx 활성화
sudo ln -sf /etc/nginx/sites-available/quicker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "=== 배포 완료 ==="
echo "접속 URL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "관리자 비밀번호: 4568" 