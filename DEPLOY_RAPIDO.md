# ⚡ Deploy em Produção - Guia Rápido (Fast Track)

> **Versão condensada para deploy rápido. Para guia completo, ver DEPLOY_PRODUCAO.md**

---

## 🚀 Setup Inicial do Servidor (Primeira vez - ~30 minutos)

### 1. Atualizar Sistema & Instalar Dependências

```bash
# SSH no servidor
ssh -i sua_chave.pem usuario@IP_DO_SERVIDOR

# Atualizar e instalar
sudo apt update && sudo apt upgrade -y

sudo apt install -y build-essential libpq-dev python3-dev \
    python3-pip python3-venv python3.13-venv git wget curl \
    nginx postgresql postgresql-contrib certbot python3-certbot-nginx ufw

# Habilitar firewall
sudo ufw enable
sudo ufw allow 22,80,443/tcp
```

### 2. Criar usuário & diretórios

```bash
sudo useradd -m -s /bin/bash clinica
sudo mkdir -p /var/www/clinica
sudo chown -R clinica:clinica /var/www/clinica
su - clinica
```

### 3. Clonar & Configurar Aplicação

```bash
cd /var/www/clinica
git clone https://github.com/softhub-unieuro/Clinica-de-psicologia.git .
cd clinica-de-psicologia/clinicaps

# Criar venv e instalar dependências
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn whitenoise
```

### 4. Configurar Banco de Dados

```bash
# Como root
sudo -s

# Acesso PostgreSQL
sudo -u postgres psql

# Dentro do psql:
CREATE DATABASE clinica_prod ENCODING 'UTF8' LC_COLLATE 'pt_BR.UTF-8' LC_CTYPE 'pt_BR.UTF-8';
CREATE USER clinica_user WITH PASSWORD 'SENHA_FORTE_123!@#$';
GRANT ALL PRIVILEGES ON DATABASE clinica_prod TO clinica_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO clinica_user;
\q
```

### 5. Configurar `.env`

```bash
# Como usuário clinica
exit  # Sair do root
su - clinica
cd /var/www/clinica/clinica-de-psicologia/clinicaps

# Criar .env
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,IP_SERVIDOR

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=clinica_prod
DATABASE_USER=clinica_user
DATABASE_PASSWORD=SENHA_FORTE_123!@#$
DATABASE_HOST=localhost
DATABASE_PORT=5432

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict
CSRF_COOKIE_SAMESITE=Strict
SESSION_COOKIE_AGE=3600
SESSION_SAVE_EVERY_REQUEST=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

STATIC_URL=/static/
STATIC_ROOT=/var/www/clinica/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/clinica/media

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=app_password_aqui
DEFAULT_FROM_EMAIL=noreply@clinica.com

LOG_LEVEL=INFO
EOF

# Ajustar permissões
chmod 600 .env
```

### 6. Executar Migrações & Coletar Statics

```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser  # Nome: admin, email: admin@clinica.com
python manage.py collectstatic --noinput

# Criar diretórios
mkdir -p /var/www/clinica/staticfiles
mkdir -p /var/www/clinica/media
mkdir -p /var/log/clinica
```

### 7. Configurar Gunicorn (systemd)

```bash
# Como root
sudo nano /etc/systemd/system/gunicorn_clinica.service
```

Adicionar:
```ini
[Unit]
Description=Gunicorn Clinica
After=network.target postgresql.service

[Service]
Type=notify
User=clinica
Group=clinica
WorkingDirectory=/var/www/clinica/clinica-de-psicologia/clinicaps
ExecStart=/var/www/clinica/clinica-de-psicologia/clinicaps/venv/bin/gunicorn \
    --workers 5 \
    --bind 127.0.0.1:8000 \
    --timeout 30 \
    --access-logfile /var/log/clinica/gunicorn_access.log \
    --error-logfile /var/log/clinica/gunicorn_error.log \
    clinicaps.wsgi:application

Restart=always
RestartSec=10
EnvironmentFile=/var/www/clinica/clinica-de-psicologia/clinicaps/.env

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_clinica
sudo systemctl start gunicorn_clinica
sudo systemctl status gunicorn_clinica
```

### 8. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/clinica
```

Adicionar (básico):
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /var/www/clinica/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/clinica/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar
sudo ln -s /etc/nginx/sites-available/clinica /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Certificado SSL (Let's Encrypt)

```bash
# Assumindo DNS já apontando para servidor
sudo certbot certonly --nginx -d seudominio.com -d www.seudominio.com \
    --email seu_email@gmail.com --agree-tos --non-interactive

# Nginx será atualizado automaticamente
```

---

## 🔄 Deploy de Atualização (Após código melhora - ~10 minutos)

```bash
# SSH
ssh -i chave.pem clinica@IP

# Parar gracefully
sudo systemctl stop gunicorn_clinica

# Backup
cd /var/www/clinica
sudo -u postgres pg_dump -U clinica_user clinica_prod | gzip > /var/backups/clinica/backup_pre_deploy_$(date +%s).sql.gz

# Pull código
git pull origin main
source venv/bin/activate

# Update dependências se mudou requirements.txt
pip install -r requirements.txt

# Migrações
python manage.py migrate

# Arquivos estáticos
python manage.py collectstatic --noinput

# Reiniciar
sudo systemctl start gunicorn_clinica
sleep 2
sudo systemctl status gunicorn_clinica

# Testar
curl https://seudominio.com/admin/
```

---

## 🚨 Emergência - Rollback Rápido

```bash
# Se algo quebrou durante update
sudo systemctl stop gunicorn_clinica

# Voltar código anterior
cd /var/www/clinica
git revert HEAD --no-edit

# Voltar BD
gnzip < /var/backups/clinica/backup_pre_deploy_TIMESTAMP.sql.gz | \
    PGPASSWORD='senha' psql -U clinica_user -d clinica_prod

# Reiniciar
source clinica-de-psicologia/clinicaps/venv/bin/activate
cd clinica-de-psicologia/clinicaps
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl start gunicorn_clinica
```

---

## 📊 Monitoramento Rápido

```bash
# Ver status tudo
sudo systemctl status gunicorn_clinica nginx postgresql

# Ver logs (últimos 30 linhas)
sudo tail -30 /var/log/clinica/gunicorn_error.log
sudo tail -30 /var/log/nginx/clinica_error.log

# Monitor em tempo real
ps aux | grep gunicorn
netstat -tulpn | grep LISTEN

# Recursos sistema
free -h
df -h /var/www/clinica

# Conectar BD
psql -U clinica_user -d clinica_prod -h localhost
```

---

## 🔐 Checklists Essenciais

### ✅ Antes de Colocar em Produção

- [ ] `DEBUG=False` no `.env`
- [ ] `SECRET_KEY` gerada e única
- [ ] `ALLOWED_HOSTS` correto
- [ ] BD criada e migrations executadas
- [ ] SSL/TLS ativado (HTTPS)
- [ ] Email configurado
- [ ] Gunicorn rodando
- [ ] Nginx redirecionando
- [ ] Backup automático configurado
- [ ] Firewall ativado

### ✅ Testando Aplicação

```bash
# Login como admin (senha criada no createsuperuser)
Acessar: https://seudominio.com/admin/

# Testar inscrição
https://seudominio.com/  # Página pública

# Ver status
Ativar: https://seudominio.com/admin/
```

---

## 🆘 Comandos Úteis para SOS

```bash
# Reiniciar tudo
sudo systemctl restart gunicorn_clinica nginx postgresql

# Ver último erro
sudo tail -1 /var/log/clinica/gunicorn_error.log

# Verificar porta 8000
sudo lsof -i :8000

# Matarprocesso problemático
sudo pkill -f gunicorn

# Espaço em disco
df -h

# Conectar ao BD direto
sudo -u postgres psql clinica_prod

# Ver conexões BD
SELECT * FROM pg_stat_activity;

# Criar novo superuser se perdeu
python manage.py createsuperuser

# Ver versão Django
python manage.py --version
```

---

## 📱 Acessos Importantes em Produção

| Recurso | URL | Login |
|---------|-----|-------|
| **Admin Panel** | https://seudominio.com/admin/ | admin / senha |
| **Inscrição Pública** | https://seudominio.com/ | sem login |
| **SSH** | ssh -i chave.pem clinica@IP | chave ssh |
| **PostgreSQL** | localhost:5432 | clinica_user / senha |
| **Gunicorn** | :8000 (bind local) | N/A |
| **Nginx** | 80, 443 | N/A |

---

## 📞 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| 502 Bad Gateway | `sudo systemctl restart gunicorn_clinica` |
| Timeout | Aumentar workers no gunicorn |
| BD offline | `sudo systemctl restart postgresql` |
| SSL inválido | `sudo certbot renew` |
| Espaço disco | `du -sh /var/www/clinica/* \| sort -h` |
| Memory leak | Reiniciar gunicorn: `sudo systemctl restart gunicorn_clinica` |
| Arquivo não sobe | Verificar `client_max_body_size` nginx |

---

## 🔄 Ciclo de Vida de Deploy

```
Desenvolvimento → Teste → Staging → PRODUÇÃO
                                      ↓
                            Monitorar & Suporte
                                      ↓
                            Backup & Disaster Recovery
```

---

## 📋 Node.js de Configuração em Arquivo

```bash
# Arquivo de referência rápida
cat > /tmp/clinica_prod_config.txt << 'EOF'
SERVIDOR: IP_DO_SERVIDOR
DOMINIO: seudominio.com
APP_DIR: /var/www/clinica
APP_USER: clinica
PYTHON_VERSION: 3.13
POSTGRES_VERSION: 16
NGINX_VERSION: Latest
GUNICORN_WORKERS: 5
BD_NAME: clinica_prod
BD_USER: clinica_user
EMAIL_DOMAIN: clinica-psicologia.com.br
SSL: LetsEncrypt (renovação automática)
BACKUP_FREQUENCY: Diária (BD) + Semanal (arquivos)
SESSION_TIMEOUT: 1 hora
MAX_UPLOAD: 10MB
EOF

cat /tmp/clinica_prod_config.txt
```

---

## 🎯 Próximos Passos

1. **Imediatamente após deploy:**
   - [ ] Testar login admin
   - [ ] Submeter inscrição teste
   - [ ] Verificar logs 30+ minutos

2. **Primeiras 24 horas:**
   - [ ] Monitorar CPU/Memória/Disco
   - [ ] Verificar alertas
   - [ ] Backup manual teste

3. **Primeira semana:**
   - [ ] Performance tuning
   - [ ] Comunicar produção ao time
   - [ ] Documentar lições aprendidas

---

**⚡ Tempo médio de deploy completo: 45 minutos**  
**⏱️ Tempo de deploy atualização: 10 minutos**  
**🔄 Tempo de rollback: 5 minutos**

Para guia completo, ver: [DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md)
