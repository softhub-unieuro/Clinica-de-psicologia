# 🔐 Guia Completo de Variáveis de Ambiente

> **Referência detalhada para configurar `.env` em produção com explicações de cada variável.**

---

## 📝 Estrutura do Arquivo `.env`

O arquivo `.env` é carregado pelo `python-dotenv` na inicialização do Django. Deve estar em:

```
/var/www/clinica/clinica-de-psicologia/clinicaps/.env
```

Permissões obrigatórias:
```bash
chmod 600 .env
chown clinica:clinica .env
```

---

## 📋 Variáveis de Configuração

### Seção 1: Django Core Settings

```env
# ============================================
# DJANGO CORE SETTINGS
# ============================================

# DEBUG MODE (CRITICAL: Must be False in production)
# FALSE = Modo produção (não expõe stack trace de erros)
# TRUE = Modo desenvolvimento (expõe detalhes, NUNCA em produção!)
DEBUG=False

# SECRET_KEY (Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# Mínimo 50 caracteres, caracteres especiais, aleatório
# NUNCA compartilhe essa chave!
# NUNCA use a chave padrão em produção!
SECRET_KEY=gerar-uma-chave-segura-e-aleatoria-com-50plus-caracteres-aqui!@#$%

# ALLOWED_HOSTS (Domínios que podem servir a aplicação)
# Separados por vírgula, sem espaços
# Incluir IP do servidor para acesso de emergência
# Exemplo: ALLOWED_HOSTS=clinica-psicologia.com.br,www.clinica-psicologia.com.br,192.168.1.100
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,IP_DO_SERVIDOR

# LANGUAGE_CODE (Localização de linguagem)
LANGUAGE_CODE=pt-br

# TIME_ZONE (Fuso horário)
TIME_ZONE=America/Sao_Paulo

# USE_I18N (Internacionalização)
USE_I18N=True

# USE_TZ (Suporte a timezone)
USE_TZ=True
```

---

### Seção 2: PostgreSQL Database Configuration

```env
# ============================================
# BANCO DE DADOS POSTGRESQL
# ============================================

# DATABASE ENGINE (Sempre PostgreSQL)
DATABASE_ENGINE=django.db.backends.postgresql

# DATABASE_NAME (Nome do banco de dados)
# Recomendação: clinica_prod ou clinica_produção
# Deve corresponder ao banco criado no PostgreSQL
DATABASE_NAME=clinica_prod

# DATABASE_USER (Usuário PostgreSQL)
# Recomendação: clinica_user (não usar postgres)
# Deve ter privilégios apenas sobre database_name
DATABASE_USER=clinica_user

# DATABASE_PASSWORD (Senha do usuário PostgreSQL)
# IMPORTANTE: Senha forte com:
# - Mínimo 16 caracteres
# - Números (0-9)
# - Letras maiúsculas (A-Z)
# - Letras minúsculas (a-z)
# - Caracteres especiais (!@#$%^&*)
# - SEM espaços
# Exemplo de senha forte: Clínica@Prod2024!xK9m7
DATABASE_PASSWORD=SenhaForteAqui123!@#$

# DATABASE_HOST (Servidor PostgreSQL)
# localhost = BD na mesma máquina
# nome_do_servidor ou IP = BD em servidor diferente
# Para Docker: nome_do_container_postgres
DATABASE_HOST=localhost

# DATABASE_PORT (Porta PostgreSQL)
# Padrão: 5432
# Se customizado, use a porta configurada
DATABASE_PORT=5432

# DATABASE_CONN_MAX_AGE (Pool de conexões em segundos)
# 600 = 10 minutos (padrão, ótimo para produção)
# Aumentar para 1800 (30 min) se houver muitas conexões
DATABASE_CONN_MAX_AGE=600

# DATABASE_SSL_REQUIRE (Exigir SSL para BD)
# False = conexão sem SSL (apenas localhost)
# True = exigir SSL (caminho para certificado)
DATABASE_SSL_REQUIRE=False

# DATABASE_SSL_MODE (Modo SSL para PostgreSQL)
# Valores válidos: disable, allow, prefer, require, verify-ca, verify-full
# prefer = tenta SSL, se falhar usa TCP normal
# require = obrigatório SSL
DATABASE_SSL_MODE=prefer

# DATABASE_SSL_CERT (Caminho para certificado cliente)
# Vazio se DATABASE_SSL_REQUIRE=False
DATABASE_SSL_CERT=/etc/ssl/certs/client-cert.pem

# DATABASE_SSL_KEY (Caminho para chave privada cliente)
# Vazio se DATABASE_SSL_REQUIRE=False
DATABASE_SSL_KEY=/etc/ssl/private/client-key.pem

# DATABASE_SSL_ROOT_CERT (Caminho para certificado raiz CA)
# Vazio se DATABASE_SSL_REQUIRE=False
DATABASE_SSL_ROOT_CERT=/etc/ssl/certs/ca-cert.pem
```

---

### Seção 3: Django Security Settings

```env
# ============================================
# DJANGO SECURITY SETTINGS
# ============================================

# SECURE_SSL_REDIRECT (Redirecionar HTTP para HTTPS)
# True = redireciona toda requisição HTTP para HTTPS
# False = permite HTTP (apenas development)
SECURE_SSL_REDIRECT=True

# SESSION_COOKIE_SECURE (Cookie de sessão somente HTTPS)
# True = cookie transmitido apenas por HTTPS
# False = transmitido por HTTP também (inseguro)
SESSION_COOKIE_SECURE=True

# CSRF_COOKIE_SECURE (Cookie CSRF somente HTTPS)
CSRF_COOKIE_SECURE=True

# SESSION_COOKIE_HTTPONLY (Cookie não acessível por JavaScript)
# True = protege contra XSS
# False = JavaScript pode acessar (inseguro)
SESSION_COOKIE_HTTPONLY=True

# CSRF_COOKIE_HTTPONLY (CSRF cookie não acessível por JavaScript)
CSRF_COOKIE_HTTPONLY=True

# SESSION_COOKIE_SAMESITE (Proteção contra CSRF e rastreamento)
# Strict = enviado apenas em requisições same-site
# Lax = modo mais permissivo mas seguro
# None = enviado em todas, exige SECURE=True
SESSION_COOKIE_SAMESITE=Strict

# CSRF_COOKIE_SAMESITE
CSRF_COOKIE_SAMESITE=Strict

# SESSION_COOKIE_AGE (Tempo de sessão em segundos)
# 3600 = 1 hora (recomendado para clínica)
# 1800 = 30 minutos (mais seguro)
# 7200 = 2 horas
SESSION_COOKIE_AGE=3600

# SESSION_SAVE_EVERY_REQUEST (Atualizar tempo de sessão a cada requisição)
# True = estende sessão com cada acesso (recomendado)
# False = sessão expira mesmo com atividade
SESSION_SAVE_EVERY_REQUEST=True

# SECURE_HSTS_SECONDS (HTTP Strict Transport Security em segundos)
# 31536000 = 1 ano (padrão seguro)
# Instrui browser a sempre usar HTTPS
SECURE_HSTS_SECONDS=31536000

# SECURE_HSTS_INCLUDE_SUBDOMAINS (Aplicar HSTS a subdomínios)
# True = todas as subdomínios usarão HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# SECURE_HSTS_PRELOAD (Incluir em HSTS preload list do browser)
# True = mais seguro, mas difícil de remover depois
SECURE_HSTS_PRELOAD=True

# X_FRAME_OPTIONS (Proteção contra Clickjacking)
# DENY = não pode ser embutido em iframe
# SAMEORIGIN = apenas in same origin
X_FRAME_OPTIONS=DENY

# SECURE_CONTENT_TYPE_NOSNIFF (Prevenir MIME type sniffing)
# True = força Content-Type correto
SECURE_CONTENT_TYPE_NOSNIFF=True

# SECURE_BROWSER_XSS_FILTER (XSS Protection header)
# True = ativa proteção XSS do browser
SECURE_BROWSER_XSS_FILTER=True

# CSRF_TRUSTED_ORIGINS (Origens confiáveis para CSRF)
# Lista de URLs que podem fazer requisições
# Separadas por espaço, incluir domínio e subdomínios
# Exemplo: CSRF_TRUSTED_ORIGINS=https://clinica.com https://www.clinica.com
CSRF_TRUSTED_ORIGINS=https://seudominio.com https://www.seudominio.com
```

---

### Seção 4: Static & Media Files

```env
# ============================================
# STATIC & MEDIA FILES
# ============================================

# STATIC_URL (URL pública para arquivos estáticos)
# Não alterar, padrão Django
STATIC_URL=/static/

# STATIC_ROOT (Caminho físico dos arquivos estáticos coletados)
# Absoluto, acessível pelo Nginx
# Executar: python manage.py collectstatic --noinput
STATIC_ROOT=/var/www/clinica/staticfiles

# MEDIA_URL (URL pública para uploads de usuários)
# Não alterar, padrão Django
MEDIA_URL=/media/

# MEDIA_ROOT (Caminho físico dos uploads)
# Absoluto, acessível pelo Nginx
# Criado automaticamente, servidor web precisa permissão write
MEDIA_ROOT=/var/www/clinica/media

# FILE_UPLOAD_MAX_MEMORY_SIZE (Tamanho máximo upload em bytes)
# 10485760 = 10MB (padrão para TCLE e documentos)
# Alterar apenas se necessário
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760

# DATA_UPLOAD_MAX_MEMORY_SIZE (Tamanho máximo de bytes em POST)
# 10485760 = 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE=10485760
```

---

### Seção 5: Email Configuration

```env
# ============================================
# EMAIL CONFIGURATION
# ============================================

# EMAIL_BACKEND (Qual backend usar para enviar emails)
# django.core.mail.backends.smtp.EmailBackend = Produção
# django.core.mail.backends.console.EmailBackend = Debug (imprime no console)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# EMAIL_HOST (Servidor SMTP)
# gmail.com, outlook.com, amazon-ses, digitalocean, etc.
# Exemplo: smtp.gmail.com (não esqueça "smtp.")
EMAIL_HOST=smtp.gmail.com

# EMAIL_PORT (Porta SMTP)
# 587 = TLS (recomendado e comum)
# 465 = SSL
# 25 = SMTP puro (inseguro, não usar)
EMAIL_PORT=587

# EMAIL_USE_TLS (Usar TLS para criptografia)
# True = use TLS
# False = sem TLS (apenas se usar SSL via porta 465)
EMAIL_USE_TLS=True

# EMAIL_USE_SSL (Usar SSL para criptografia)
# True = use SSL (porta 465)
# False = não use SSL (use TLS com porta 587)
EMAIL_USE_SSL=False

# EMAIL_HOST_USER (Usuário/email para SMTP)
# Para Gmail: seu_email@gmail.com
# Para SES: user da plataforma
EMAIL_HOST_USER=seu_email@gmail.com

# EMAIL_HOST_PASSWORD (Senha/token SMTP)
# Para Gmail: usar app password (2FA deve estar ativo)
# Para SES: use access key
# NUNCA usar senha Gmail normal
EMAIL_HOST_PASSWORD=sua_senha_app_aqui

# DEFAULT_FROM_EMAIL (Email padrão para envios)
# De qual endereço os emails da aplicação serão enviados
# Exemplo: noreply@clinica-psicologia.com.br
DEFAULT_FROM_EMAIL=noreply@clinica-psicologia.com.br

# SERVER_EMAIL (Email para notificações de erro do servidor)
# Para onde Django envia erros 500 (email de suporte)
SERVER_EMAIL=admin@clinica-psicologia.com.br

# EMAIL_TIMEOUT (Timeout em segundos para conexão SMTP)
EMAIL_TIMEOUT=10
```

---

### Seção 6: Logging & Monitoring

```env
# ============================================
# LOGGING & MONITORING
# ============================================

# LOG_LEVEL (Nível de log)
# DEBUG = Todos os logs (muitos dados)
# INFO = Apenas informações importantes (recomendado)
# WARNING = Apenas avisos e erros
# ERROR = Apenas erros
# CRITICAL = Apenas erros críticos
LOG_LEVEL=INFO

# SENTRY_DSN (Sentry error tracking - OPCIONAL)
# Vazio = desativado
# Com URL = envia erros para Sentry
# Obtenha em https://sentry.io
SENTRY_DSN=

# ALLOWED_ADMIN_IPS (IPs autorizados para /admin - OPCIONAL)
# Restringe acesso ao admin apenas a IPs específicos
# Separados por vírgula
ALLOWED_ADMIN_IPS=192.168.1.100,203.0.113.50

# ENABLE_DEBUG_TOOLBAR (Django Debug Toolbar - NUNCA em produção)
# True = ativa debug toolbar (apenas dev!)
# False = desativado (production)
ENABLE_DEBUG_TOOLBAR=False
```

---

### Seção 7: Application-Specific Settings

```env
# ============================================
# CONFIGURAÇÕES ESPECÍFICAS DA APLICAÇÃO
# ============================================

# MAXIMUM_FILE_SIZE_MB (Tamanho máximo de upload em MB)
# 10 = 10MB padrão
MAXIMUM_FILE_SIZE_MB=10

# SESSION_TIMEOUT_HOURS (Timeout de sessão em horas)
# 1 = 1 hora
SESSION_TIMEOUT_HOURS=1

# ENABLE_LDAP_AUTH (Autenticação LDAP - OPCIONAL)
# False = desativado
# True = habilitar autenticação via LDAP (Unieuro)
ENABLE_LDAP_AUTH=False

# LDAP_SERVER (Servidor LDAP da instituição)
LDAP_SERVER=ldap.unieuro.edu.br

# LDAP_PORT (Porta LDAP)
LDAP_PORT=389

# AUTO_ANONYMIZE_DAYS (Anonimizar dados após N dias)
# 365 = 1 ano sem atendimento = anonimizar dados
# 0 = desativado
AUTO_ANONYMIZE_DAYS=365

# BACKUP_RETENTION_DAYS (Manter backups por N dias)
# 30 = manter backup últimos 30 dias
BACKUP_RETENTION_DAYS=30
```

---

### Seção 8: Performance & Caching

```env
# ============================================
# PERFORMANCE & CACHING
# ============================================

# CACHE_BACKEND (Backend de cache)
# Vazio ou locmem = cache local em memória
# redis = Redis cache (melhor performance)
CACHE_BACKEND=locmem

# CACHE_LOCATION (Configuração do cache)
# Para locmem: vazio
# Para redis: redis://127.0.0.1:6379/1
CACHE_LOCATION=

# CACHE_TIMEOUT (Timeout de cache em segundos)
# 300 = 5 minutos
CACHE_TIMEOUT=300

# ENABLE_QUERY_OPTIMIZATION (Otimizar queries DB)
# True = prefetch_related, select_related automático
ENABLE_QUERY_OPTIMIZATION=True

# DATABASE_POOL_SIZE (Tamanho do pool de conexões)
# 5 = 5 conexões máximas simultâneas
DATABASE_POOL_SIZE=5

# DATABASE_POOL_TIMEOUT (Timeout pool conexão)
# 30 = 30 segundos
DATABASE_POOL_TIMEOUT=30
```

---

## 📝 Arquivo `.env` Completo para Produção

```env
# ============================================
# DJANGO CORE
# ============================================
DEBUG=False
SECRET_KEY=generate_with_command_above_50plus_chars!@#$%^&*
ALLOWED_HOSTS=clinica-psicologia.com.br,www.clinica-psicologia.com.br,203.0.113.10
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
USE_I18N=True
USE_TZ=True

# ============================================
# POSTGRESQL DATABASE
# ============================================
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=clinica_prod
DATABASE_USER=clinica_user
DATABASE_PASSWORD=SenhaForte123!@#$%^&*xyZ
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_CONN_MAX_AGE=600
DATABASE_SSL_REQUIRE=False
DATABASE_SSL_MODE=prefer

# ============================================
# SECURITY SETTINGS
# ============================================
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
X_FRAME_OPTIONS=DENY
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
CSRF_TRUSTED_ORIGINS=https://clinica-psicologia.com.br https://www.clinica-psicologia.com.br

# ============================================
# STATIC & MEDIA FILES
# ============================================
STATIC_URL=/static/
STATIC_ROOT=/var/www/clinica/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/clinica/media
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760
DATA_UPLOAD_MAX_MEMORY_SIZE=10485760

# ============================================
# EMAIL
# ============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_app_password_aqui
DEFAULT_FROM_EMAIL=noreply@clinica-psicologia.com.br
SERVER_EMAIL=admin@clinica-psicologia.com.br
EMAIL_TIMEOUT=10

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO
SENTRY_DSN=
ENABLE_DEBUG_TOOLBAR=False

# ============================================
# APPLICATION SPECIFIC
# ============================================
MAXIMUM_FILE_SIZE_MB=10
SESSION_TIMEOUT_HOURS=1
ENABLE_LDAP_AUTH=False
AUTO_ANONYMIZE_DAYS=365
BACKUP_RETENTION_DAYS=30

# ============================================
# PERFORMANCE
# ============================================
CACHE_BACKEND=locmem
CACHE_TIMEOUT=300
ENABLE_QUERY_OPTIMIZATION=True
DATABASE_POOL_SIZE=5
DATABASE_POOL_TIMEOUT=30
```

---

## 🔒 Boas Práticas de Segurança para `.env`

1. **Nunca commitar para Git**
   ```bash
   # Adicionar ao .gitignore
   echo ".env" >> .gitignore
   git rm --cached .env
   ```

2. **Permissões de Arquivo**
   ```bash
   chmod 600 .env
   chown clinica:clinica .env
   ```

3. **Backup Seguro**
   ```bash
   # Armazenar em local seguro (LastPass, Bitwarden, etc.)
   # Não armazenar em repositório Git
   # Criptografar se armazenar em cloud
   ```

4. **Rotação de Senhas**
   ```bash
   # Trocar SECRET_KEY:
   # 1. Gerar nova com comando acima
   # 2. Atualizar .env
   # 3. Restartar gunicorn
   # 4. Documentar no runbook
   ```

5. **Auditoria de Acesso**
   ```bash
   # Verificar quem acessou .env
   sudo tail -f /var/log/auth.log | grep .env
   ```

---

## 🧪 Verificar Variáveis em Produção

```bash
# Entrar no Django shell
cd /var/www/clinica/clinica-de-psicologia/clinicaps
source venv/bin/activate
python manage.py shell

# Verificar dentro do shell Python
from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DATABASE NAME: {settings.DATABASES['default']['NAME']}")
print(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
```

---

## 📞 Troubleshooting de Variáveis

### "ImproperlyConfigured" Error
- Verificar se `.env` existe no diretório correto
- Verificar sintaxe (sem espaços ao redor de `=`)
- Verificar se variável obrigatória está presente

### Conexão com BD falha
- Testrar: `psql -U $DATABASE_USER -d $DATABASE_NAME -h $DATABASE_HOST`
- Verificar senha no `.env`
- Verificar privilégios no PostgreSQL

### Email não funciona
- Testrar: `python manage.py shell` e depois `send_mail(...)`
- Verificar credenciais SMTP
- Verificar se firewall permite porta 587

---

**Versão:** 1.2  
**Última atualização:** Março 2026  
**Django:** 5.2.1
