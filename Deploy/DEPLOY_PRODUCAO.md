# 🚀 Guia Completo de Deploy em Produção - Clínica de Psicologia

> **Documento detalhado para configurar e fazer deploy da aplicação Django em um ambiente de produção com segurança, performance e confiabilidade.**

---

## 📋 Índice

- [1. Pré-requisitos](#1-pré-requisitos)
- [2. Preparação do Servidor](#2-preparação-do-servidor)
- [3. Instalação de Dependências](#3-instalação-de-dependências)
- [4. Configuração do PostgreSQL](#4-configuração-do-postgresql)
- [5. Configuração de Variáveis de Ambiente](#5-configuração-de-variáveis-de-ambiente)
- [6. Configuração do Django para Produção](#6-configuração-do-django-para-produção)
- [7. Setup do Servidor Web (Nginx)](#7-setup-do-servidor-web-nginx)
- [8. Setup do Application Server (Gunicorn)](#8-setup-do-application-server-gunicorn)
- [9. Configuração de SSL/TLS (Let's Encrypt)](#9-configuração-de-ssltls-lets-encrypt)
- [10. Monitoramento e Logging](#10-monitoramento-e-logging)
- [11. Backups e Recuperação](#11-backups-e-recuperação)
- [12. Troubleshooting](#12-troubleshooting)

---

## 1. Pré-requisitos

### 1.1 Requisitos do Sistema

#### Recomendações de Hardware
- **CPU**: 2+ cores (mínimo 2 GHz)
- **RAM**: 4GB (mínimo), 8GB recomendado
- **Disco**: 50GB SSD (espaço suficiente para banco de dados e uploads)
- **Conexão**: Internet estável com IP fixo

#### Sistema Operacional Suportado
- Ubuntu 22.04 LTS ou 24.04 LTS (recomendado)
- Debian 12+
- CentOS 8+
- RHEL 8+

### 1.2 Software Necessário

```bash
# Verificar versões instaladas
python3 --version      # Python 3.13+
postgres --version      # PostgreSQL 12+
nginx -v               # Nginx 1.18+
git --version          # Git 2.0+
```

---

## 2. Preparação do Servidor

### 2.1 Atualizar Pacotes do Sistema

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes instalados
sudo apt upgrade -y

# Instalar ferramentas essenciais
sudo apt install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    htop \
    nano \
    vim \
    ufw
```

### 2.2 Configurar Firewall

```bash
# Ativar UFW (Uncomplicated Firewall)
sudo ufw enable

# Permitir SSH (importante!)
sudo ufw allow 22/tcp

# Permitir HTTP
sudo ufw allow 80/tcp

# Permitir HTTPS
sudo ufw allow 443/tcp

# Permitir PostgreSQL (apenas da máquina local)
sudo ufw allow from localhost to any port 5432

# Verificar status
sudo ufw status
```

### 2.3 Criar Usuário de Aplicação

```bash
# Criar usuário específico para a aplicação (sem acesso shell)
sudo useradd -m -s /bin/bash clinica

# Adicionar ao grupo sudo (opcional, para tarefas de manutenção)
sudo usermod -aG sudo clinica

# Criar diretório de aplicação
sudo mkdir -p /var/www/clinica
sudo chown -R clinica:clinica /var/www/clinica
sudo chmod -R 755 /var/www/clinica

# Trocar para usuário clinica
su - clinica
```

---

## 3. Instalação de Dependências

### 3.1 Instalar Python e Venv

```bash
# Verificar se Python 3.13 está disponível
python3 --version

# Se não estiver, instalar via deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.13 python3.13-venv python3.13-dev
```

### 3.2 Clonar Repositório

```bash
# Entrar no diretório de aplicação
cd /var/www/clinica

# Clonar o repositório
sudo git clone https://github.com/softhub-unieuro/Clinica-de-psicologia.git .

# Trocar para diretório da aplicação Django
cd clinica-de-psicologia/clinicaps

# Ajustar permissões
sudo chown -R clinica:clinica /var/www/clinica
```

### 3.3 Criar e Ativar Virtual Environment

```bash
# Criar virtual environment com Python 3.13
python3.13 -m venv venv

# Ativar virtual environment
source venv/bin/activate

# Verificar se o pip está atualizado
pip install --upgrade pip setuptools wheel

# Instalar dependências do projeto
pip install -r requirements.txt

# Adicionar dependências de produção (opcionais mas recomendados)
pip install \
    gunicorn \
    django-cors-headers \
    django-ratelimit \
    django-axes \
    whitenoise  # Servir arquivos estáticos de forma eficiente
```

---

## 4. Configuração do PostgreSQL

### 4.1 Instalar PostgreSQL Server

```bash
# Adicionar repositório oficial PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Atualizar pacotes
sudo apt update

# Instalar PostgreSQL 16 (versão mais recente)
sudo apt install -y postgresql postgresql-contrib

# Verificar status
sudo systemctl status postgresql
```

### 4.2 Criar Banco de Dados e Usuário

```bash
# Acessar como superusuário PostgreSQL
sudo -u postgres psql

# Dentro do psql, executar os comandos:

-- Criar database
CREATE DATABASE clinica_prod
    OWNER postgres
    ENCODING 'UTF8'
    LC_COLLATE 'pt_BR.UTF-8'
    LC_CTYPE 'pt_BR.UTF-8';

-- Criar usuário específico
CREATE USER clinica_user WITH PASSWORD 'SENHA_SUPER_SEGURA_AQUI_2024!';

-- Configurar privilégios
ALTER ROLE clinica_user SET client_encoding TO 'utf8';
ALTER ROLE clinica_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE clinica_user SET default_transaction_deferrable TO on;
ALTER ROLE clinica_user SET default_transaction_level TO 'read committed';

-- Conceder privilégios no banco de dados
GRANT ALL PRIVILEGES ON DATABASE clinica_prod TO clinica_user;

-- Conectar ao banco e conceder privilégios no schema
\c clinica_prod

-- Conceder privilégios no schema public
GRANT ALL ON SCHEMA public TO clinica_user;

-- Conceder privilégios em todas as tabelas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO clinica_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO clinica_user;

-- Sair do psql
\q
```

### 4.3 Configurar PostgreSQL para Conectividade Remota (Opcional)

Se a aplicação estiver em servidor diferente do banco:

```bash
# Editar arquivo postgresql.conf
sudo nano /etc/postgresql/16/main/postgresql.conf

# Encontrar e descomentar a linha (aprox. linha 60):
listen_addresses = 'localhost,IP_DO_SERVIDOR'

# Editar arquivo pg_hba.conf para aceitar conexões
sudo nano /etc/postgresql/16/main/pg_hba.conf

# Adicionar linha (substitua IP_DA_APP):
host    clinica_prod    clinica_user    IP_DA_APP/32    md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### 4.4 Configurar SSL/TLS no PostgreSQL

```bash
# Gerar certificado auto-assinado (dev/produção inicial)
sudo -u postgres openssl req -new -text -out /etc/postgresql/16/main/server.req \
    -keyout /etc/postgresql/16/main/private/server.key -subj "/C=BR/ST=DF/L=Brasilia/O=Clinica/CN=db-prod"

# Converter para certificado
sudo -u postgres openssl req -x509 -in /etc/postgresql/16/main/server.req \
    -text -out /etc/postgresql/16/main/server.crt -signkey /etc/postgresql/16/main/private/server.key

# Ajustar permissões
sudo chmod 600 /etc/postgresql/16/main/server.key

# Habilitar SSL no postgresql.conf
echo "ssl = on" | sudo tee -a /etc/postgresql/16/main/postgresql.conf

# Reiniciar
sudo systemctl restart postgresql
```

---

## 5. Configuração de Variáveis de Ambiente

### 5.1 Criar Arquivo .env em Produção

```bash
# Entrar no diretório da aplicação
cd /var/www/clinica/clinica-de-psicologia/clinicaps

# Criar arquivo .env
sudo nano .env

# Copiar e adaptar o seguinte conteúdo:
```

```env
# ============================================
# DJANGO CORE SETTINGS
# ============================================
DEBUG=False
SECRET_KEY=GERAR_USANDO_COMANDO_ABAIXO
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,IP_DO_SERVIDOR

# ============================================
# BANCO DE DADOS POSTGRESQL
# ============================================
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=clinica_prod
DATABASE_USER=clinica_user
DATABASE_PASSWORD=SENHA_SUPER_SEGURA_AQUI_2024!
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_CONN_MAX_AGE=600

# ============================================
# SEGURANÇA (PRODUÇÃO)
# ============================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# SSL Banco de Dados
DATABASE_SSL_REQUIRE=True
DATABASE_SSL_MODE=require

# ============================================
# LOGGING E MONITORAMENTO
# ============================================
LOG_LEVEL=INFO
SENTRY_DSN=  # Opcional: Para monitoramento de erros

# ============================================
# EMAIL (para notificações)
# ============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app_google
DEFAULT_FROM_EMAIL=noreply@clinica-psicologia.com.br

# ============================================
# STATIC E MEDIA FILES
# ============================================
STATIC_URL=/static/
STATIC_ROOT=/var/www/clinica/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/clinica/media
```

### 5.2 Gerar SECRET_KEY Segura

```bash
# Dentro do venv ativo
python3 << 'EOF'
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
EOF

# Copiar a saída e adicionar no .env
```

### 5.3 Ajustar Permissões do .env

```bash
# Garantir que apenas o usuário clinica possa ler o arquivo
sudo chown clinica:clinica /var/www/clinica/clinica-de-psicologia/clinicaps/.env
sudo chmod 600 /var/www/clinica/clinica-de-psicologia/clinicaps/.env
```

---

## 6. Configuração do Django para Produção

### 6.1 Executar Migrações

```bash
# Ativar venv se não estiver
source /var/www/clinica/clinica-de-psicologia/clinicaps/venv/bin/activate

# Entrar no diretório correto
cd /var/www/clinica/clinica-de-psicologia/clinicaps

# Executar migrações
python manage.py migrate

# Criar superusuário (coordenador)
python manage.py createsuperuser

# Coletando arquivos estáticos
python manage.py collectstatic --noinput
```

### 6.2 Criar Diretórios de Arquivos

```bash
# Criar diretórios para static e media
mkdir -p /var/www/clinica/staticfiles
mkdir -p /var/www/clinica/media

# Ajustar permissões
sudo chown -R clinica:clinica /var/www/clinica/staticfiles
sudo chown -R clinica:clinica /var/www/clinica/media
sudo chmod -R 755 /var/www/clinica/staticfiles
sudo chmod -R 755 /var/www/clinica/media
```

### 6.3 Criar Diretório de Logs

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/clinica

# Ajustar permissões
sudo chown -R clinica:clinica /var/log/clinica
sudo chmod -R 755 /var/log/clinica
```

---

## 7. Setup do Servidor Web (Nginx)

### 7.1 Instalar Nginx

```bash
# Instalar nginx
sudo apt install -y nginx

# Ativar nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Verificar status
sudo systemctl status nginx
```

### 7.2 Criar Configuração Virtual Host

```bash
# Criar arquivo de configuração
sudo nano /etc/nginx/sites-available/clinica

# Adicionar o seguinte conteúdo:
```

```nginx
# Redirect HTTP para HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name seudominio.com www.seudominio.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server Block
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name seudominio.com www.seudominio.com;
    
    # SSL Certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;
    
    # SSL Configuration (Mozilla Recommendations)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Logging
    access_log /var/log/nginx/clinica_access.log;
    error_log /var/log/nginx/clinica_error.log;
    
    # Client Upload Size (10MB)
    client_max_body_size 10M;
    
    # Nginx Tuning
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Static Files
    location /static/ {
        alias /var/www/clinica/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files (uploads)
    location /media/ {
        alias /var/www/clinica/media/;
        expires 7d;
    }
    
    # Proxy para Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Websocket support (se necessário)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 7.3 Ativar Configuração

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/clinica /etc/nginx/sites-enabled/clinica

# Remover site default se desejado
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar nginx
sudo systemctl restart nginx
```

---

## 8. Setup do Application Server (Gunicorn)

### 8.1 Criar Arquivo de Configuração Gunicorn

```bash
# Criar arquivo de configuração
sudo nano /etc/gunicorn/clinica.py

# Ou criar no diretório da aplicação
nano /var/www/clinica/clinica-de-psicologia/clinicaps/gunicorn_config.py
```

```python
# Gunicorn Configuration File
import multiprocessing

# Bind
bind = '127.0.0.1:8000'
backlog = 2048

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 5

# Logging
accesslog = '/var/log/clinica/gunicorn_access.log'
errorlog = '/var/log/clinica/gunicorn_error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process Naming
proc_name = 'clinica-app'

# Server Mechanics
daemon = False
pidfile = '/var/run/gunicorn_clinica.pid'
umask = 0
user = 'clinica'
group = 'clinica'
tmp_upload_dir = None

# SSL (se precisar)
# keyfile = '/etc/ssl/private/key.pem'
# certfile = '/etc/ssl/certs/cert.pem'

# Application Settings
raw_env = ['DJANGO_SETTINGS_MODULE=clinicaps.settings']
```

### 8.2 Criar Systemd Service para Gunicorn

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/gunicorn_clinica.service
```

```ini
[Unit]
Description=Gunicorn application server for Clinica de Psicologia
After=network.target postgresql.service

[Service]
Type=notify
User=clinica
Group=clinica
WorkingDirectory=/var/www/clinica/clinica-de-psicologia/clinicaps
ExecStart=/var/www/clinica/clinica-de-psicologia/clinicaps/venv/bin/gunicorn \
    --config /var/www/clinica/clinica-de-psicologia/clinicaps/gunicorn_config.py \
    clinicaps.wsgi:application

# Restart Policy
Restart=always
RestartSec=10

# Environment Variables
EnvironmentFile=/var/www/clinica/clinica-de-psicologia/clinicaps/.env

# Security
ProtectSystem=full
ProtectHome=yes
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

### 8.3 Ativar e Iniciar Gunicorn

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Ativar na inicialização
sudo systemctl enable gunicorn_clinica

# Iniciar serviço
sudo systemctl start gunicorn_clinica

# Verificar status
sudo systemctl status gunicorn_clinica

# Ver logs em tempo real
sudo journalctl -u gunicorn_clinica -f
```

---

## 9. Configuração de SSL/TLS (Let's Encrypt)

### 9.1 Instalar Certbot

```bash
# Instalar certbot
sudo apt install -y certbot python3-certbot-nginx

# Verificar instalação
certbot --version
```

### 9.2 Obter Certificado SSL

```bash
# Antes: Certificar que o nginx está rodando
sudo systemctl start nginx

# Obter certificado (certbot fará validação DNS automaticamente)
sudo certbot certonly --nginx \
    -d seudominio.com \
    -d www.seudominio.com \
    --email seu_email@example.com \
    --agree-tos \
    --non-interactive

# Certificados serão salvos em: /etc/letsencrypt/live/seudominio.com/
```

### 9.3 Renovação Automática de Certificados

```bash
# Habilitar renovação automática
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Testar renovação
sudo certbot renew --dry-run

# Verificar status
sudo systemctl status certbot.timer
```

---

## 10. Monitoramento e Logging

### 10.1 Configurar Rotação de Logs

```bash
# Criar arquivo de configuração logrotate
sudo nano /etc/logrotate.d/clinica
```

```
# Logs da aplicação
/var/log/clinica/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 clinica clinica
    sharedscripts
    postrotate
        sudo systemctl reload gunicorn_clinica > /dev/null 2>&1 || true
    endscript
}

# Logs do nginx
/var/log/nginx/clinica_*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

### 10.2 Monitorar Recursos do Sistema

```bash
# Instalar ferramentas de monitoramento
sudo apt install -y htop iotop nethogs

# Visualizar uso em tempo real
htop

# Verificar conectividade
sudo netstat -tulpn | grep LISTEN

# Ver portas abertas
sudo ss -tulpn
```

### 10.3 Criar Script de Health Check

```bash
# Criar script
sudo nano /usr/local/bin/clinica_health_check.sh
```

```bash
#!/bin/bash

# Health Check Script para Clínica de Psicologia

APP_URL="https://seudominio.com"
TELEGRAM_WEBHOOK="SEU_WEBHOOK_AQUI"  # Opcional: Para notificações
LOG_FILE="/var/log/clinica/health_check.log"

echo "[$(date)] Iniciando health check..." >> $LOG_FILE

# Verificar se aplicação está respondendo
if curl -sf "$APP_URL/admin/login/" > /dev/null 2>&1; then
    echo "[$(date)] ✅ Aplicação respondendo normalmente" >> $LOG_FILE
else
    echo "[$(date)] ❌ FALHA: Aplicação não respondendo!" >> $LOG_FILE
    
    # Tentar reiniciar gunicorn
    sudo systemctl restart gunicorn_clinica
    echo "[$(date)] Gunicorn reiniciado" >> $LOG_FILE
fi

# Verificar PostgreSQL
if pg_isready -h localhost -U clinica_user -d clinica_prod > /dev/null 2>&1; then
    echo "[$(date)] ✅ PostgreSQL respondendo normalmente" >> $LOG_FILE
else
    echo "[$(date)] ❌ FALHA: PostgreSQL não respondendo!" >> $LOG_FILE
fi

# Verificar espaço em disco
DISK_USAGE=$(df /var/www/clinica | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "[$(date)] ⚠️ ALERTA: Uso de disco: ${DISK_USAGE}%" >> $LOG_FILE
fi

# Verificar memória
MEM_USAGE=$(free | awk 'NR==2 {print int($3/$2 * 100)}')
if [ $MEM_USAGE -gt 80 ]; then
    echo "[$(date)] ⚠️ ALERTA: Uso de memória: ${MEM_USAGE}%" >> $LOG_FILE
fi
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/clinica_health_check.sh

# Adicionar ao crontab (a cada 5 minutos)
*/5 * * * * /usr/local/bin/clinica_health_check.sh
```

---

## 11. Backups e Recuperação

### 11.1 Backup de Banco de Dados

```bash
# Criar diretório de backups
mkdir -p /var/backups/clinica/db
sudo chown -R clinica:clinica /var/backups/clinica

# Criar script de backup
nano /usr/local/bin/backup_clinica_db.sh
```

```bash
#!/bin/bash

# Variáveis
BACKUP_DIR="/var/backups/clinica/db"
DB_NAME="clinica_prod"
DB_USER="clinica_user"
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/clinica_${BACKUP_DATE}.sql.gz"
LOG_FILE="/var/log/clinica/backup.log"

# Retenção de backups (30 dias)
RETENTION_DAYS=30

echo "[$(date)] Iniciando backup do banco de dados..." | tee -a $LOG_FILE

# Fazer dump do banco
PGPASSWORD='SENHA_DO_BANCO' pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ Backup criado: $BACKUP_FILE" >> $LOG_FILE
    echo "Tamanho: $(du -h $BACKUP_FILE | cut -f1)" >> $LOG_FILE
else
    echo "[$(date)] ❌ FALHA ao criar backup!" >> $LOG_FILE
    exit 1
fi

# Remover backups antigos
find $BACKUP_DIR -name "clinica_*.sql.gz" -mtime +$RETENTION_DAYS -delete
echo "[$(date)] Backups antigos removidos" >> $LOG_FILE

# Upload para armazenamento remoto (optional)
# aws s3 cp $BACKUP_FILE s3://seu-bucket-backup/clinica/
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/backup_clinica_db.sh

# Agendar no crontab (diariamente às 2 da manhã)
0 2 * * * /usr/local/bin/backup_clinica_db.sh
```

### 11.2 Backup de Arquivos Estáticos e Media

```bash
# Script de backup de arquivos
nano /usr/local/bin/backup_clinica_files.sh
```

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/clinica/files"
APP_DIR="/var/www/clinica"
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/clinica_files_${BACKUP_DATE}.tar.gz"
LOG_FILE="/var/log/clinica/backup.log"
RETENTION_DAYS=30

echo "[$(date)] Iniciando backup de arquivos..." >> $LOG_FILE

# Compactar arquivos
tar -czf $BACKUP_FILE \
    --exclude='$APP_DIR/clinica-de-psicologia/clinicaps/venv' \
    --exclude='$APP_DIR/.git' \
    -C $APP_DIR .

if [ $? -eq 0 ]; then
    echo "[$(date)] ✅ Backup de arquivos criado: $BACKUP_FILE" >> $LOG_FILE
else
    echo "[$(date)] ❌ FALHA ao criar backup de arquivos!" >> $LOG_FILE
    exit 1
fi

# Remover backups antigos
find $BACKUP_DIR -name "clinica_files_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Backup de arquivos concluído" >> $LOG_FILE
```

```bash
# Tornar executável e agendar
sudo chmod +x /usr/local/bin/backup_clinica_files.sh

# Adicionar ao crontab (semanalmente, aos domingos)
0 3 * * 0 /usr/local/bin/backup_clinica_files.sh
```

### 11.3 Recuperar de Backup

```bash
# Restaurar banco de dados
gunzip < /var/backups/clinica/db/clinica_20240324_020000.sql.gz | \
    PGPASSWORD='SENHA' psql -U clinica_user -d clinica_prod

# Restaurar arquivos
cd /var/www/clinica
tar -xzf /var/backups/clinica/files/clinica_files_20240324_030000.tar.gz
```

---

## 12. Troubleshooting

### 12.1 Checklist de Diagnóstico

```bash
# Verificar status geral
echo "=== Status dos Serviços ==="
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status gunicorn_clinica

echo "=== Logs Recentes ==="
sudo tail -50 /var/log/clinica/gunicorn_error.log
sudo tail -50 /var/log/nginx/clinica_error.log

echo "=== Conectividade ==="
curl -v https://seudominio.com
sudo netstat -tulpn | grep -E ':(80|443|8000|5432)'

echo "=== Recursos do Sistema ==="
free -h
df -h /var/www/clinica
du -sh /var/www/clinica/*
```

### 12.2 Problemas Comuns e Soluções

#### Problema: "Connection refused" ao acessar aplicação

```bash
# Verificar se gunicorn está rodando
sudo systemctl status gunicorn_clinica

# Verificar logs
sudo journalctl -u gunicorn_clinica -n 50

# Reiniciar
sudo systemctl restart gunicorn_clinica

# Verificar se porta 8000 está em uso
sudo lsof -i :8000
```

#### Problema: Erro 502 Bad Gateway (Nginx)

```bash
# Verificar configuração nginx
sudo nginx -t

# Checar se gunicorn está respondendo
curl http://127.0.0.1:8000/

# Analisar logs
sudo tail -50 /var/log/nginx/clinica_error.log
```

#### Problema: Erro de conexão com PostgreSQL

```bash
# Testar conexão
psql -U clinica_user -d clinica_prod -h localhost

# Verificar status PostgreSQL
sudo systemctl status postgresql

# Ver logs
sudo tail -50 /var/log/postgresql/postgresql*.log

# Reiniciar
sudo systemctl restart postgresql
```

#### Problema: Erro de permissão em arquivo

```bash
# Verificar proprietário e permissões
ls -la /var/www/clinica/

# Corrigir permissões
sudo chown -R clinica:clinica /var/www/clinica
sudo chmod -R 755 /var/www/clinica
sudo chmod 600 /var/www/clinica/clinica-de-psicologia/clinicaps/.env
```

#### Problema: Certificado SSL inválido

```bash
# Verificar certificados
sudo ls -la /etc/letsencrypt/live/

# Testar renovação
sudo certbot renew --dry-run

# Forçar renovação
sudo certbot renew --force-renewal

# Validar configuração SSL
sudo openssl s_client -connect seudominio.com:443
```

### 12.3 Verificar Configuração de Produção

```bash
# Acessar django shell
cd /var/www/clinica/clinica-de-psicologia/clinicaps
source venv/bin/activate
python manage.py shell
```

```python
# Dentro do shell Django
from django.conf import settings

# Verificar configurações críticas
print(f"DEBUG: {settings.DEBUG}")  # Deve ser False
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")

# Sair
exit()
```

---

## 📚 Referências Adicionais

- [Documentação Django Deployment](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Basic Setup](https://nginx.org/en/docs/beginners_guide.html)
- [PostgreSQL Administration](https://www.postgresql.org/docs/current/admin.html)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)

---

## 🆘 Suporte e Contato

Caso encontre problemas não listados neste guia, entre em contato com a equipe de desenvolvimento:

- **Email**: desenvolvimento@clinica-psicologia.com.br
- **Issues**: [GitHub Issues](https://github.com/softhub-unieuro/Clinica-de-psicologia/issues)

---

**Última atualização:** Março de 2026  
**Versão Django:** 5.2.1  
**Versão PostgreSQL:** 16+
