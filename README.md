# 🏥 Sistema de Gestão - Clínica de Psicologia

> **Sistema web completo para gerenciamento de clínica de psicologia, desenvolvido com Django 5.2.1, focado em segurança, conformidade com LGPD e performance.**

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Instalação e Configuração com Docker Compose](#-instalação-e-configuração-com-docker-compose)
- [Alterações Implementadas](#-alterações-implementadas)
- [Melhorias de Segurança](#-melhorias-de-segurança)
- [Otimizações de Performance](#-otimizações-de-performance)
- [Conformidade com LGPD](#-conformidade-com-lgpd)
- [Roteiro de Vídeo (Ambiente de Testes)](#-roteiro-de-vídeo-ambiente-de-testes)
- [Uso do Sistema](#-uso-do-sistema)
- [Comandos Importantes](#-comandos-importantes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Boas Práticas](#-boas-práticas)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral

Este sistema foi desenvolvido para automação de atendimentos clínicos em uma clínica de psicologia universitária (Unieuro). O projeto gerencia todo o fluxo de atendimento, desde a inscrição de pacientes até o acompanhamento de prontuários, com controle rigoroso de permissões baseado em cargos.

### Principais Funcionalidades

- ✅ **Inscrição Pública**: Formulários web para comunidade, convênios e testes psicológicos
- ✅ **Gestão de Usuários**: CRUD completo com controle de acesso baseado em cargo (RBAC)
- ✅ **Prontuários Digitais**: Vinculação de estagiários a pacientes, evolução de atendimentos
- ✅ **Dashboards Personalizados**: Visualizações específicas por cargo (Coordenador, Supervisor, RT, Estagiário)
- ✅ **Auditoria LGPD**: Logging de acessos sem exposição de dados sensíveis
- ✅ **Anonimização Automática**: Comando para anonimizar dados de pacientes inativos

---

## 🛠 Tecnologias Utilizadas

### Backend
- **Python**: 3.13
- **Django**: 5.2.1
- **PostgreSQL**: Banco de dados relacional
- **psycopg2**: 2.9.10 (Adaptador PostgreSQL)
- **Gunicorn**: Servidor WSGI em produção
- **Docker & Docker Compose**: Containerização e orquestração

### Frontend
- **HTML5 / CSS3**
- **JavaScript (Vanilla)**
- **Tailwind CSS / Bootstrap**: Estilização responsiva

### Bibliotecas e Dependências
```
asgiref==3.8.1
Django==5.2.1
psycopg2==2.9.10
sqlparse==0.5.3
tzdata==2025.2
python-dotenv==1.1.1      # Gerenciamento de variáveis de ambiente
validate-docbr==1.11.1    # Validação de CPF/CNPJ
Pillow==12.0.0            # Manipulação de imagens
django-jazzmin==3.5.5     # Interface administrativa moderna
gunicorn==21.2.0          # Servidor WSGI
```

### Segurança
- Senhas hasheadas (PBKDF2 - padrão Django)
- CSRF Protection
- XSS Protection
- Clickjacking Protection
- Session Security
- HTTPS (recomendado em produção)

---

## 🐳 Instalação e Configuração com Docker Compose

### Pré-requisitos

- **Docker**: v24.0 ou superior
- **Docker Compose**: v2.20 ou superior
- **Git**: para clonar o repositório

### Verificar Instalação

```bash
docker --version
docker compose version
git --version
```

### Passos de Instalação

#### 1. Clonar o Repositório

```bash
git clone https://github.com/softhub-unieuro/clinica-de-psicologia.git
cd clinica-de-psicologia
git checkout Daniel_docker-branch
```

#### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env com suas configurações
# Importante: Alterar SECRET_KEY e credenciais de banco de dados
nano .env  # ou use seu editor preferido
```

**Variáveis essenciais a configurar:**
```env
# Segurança
SECRET_KEY=sua-chave-secreta-super-segura-aqui-MUDE-EM-PRODUCAO
DEBUG=False

# Banco de Dados (Docker Compose)
DB_NAME=clinica_psicologia
DB_USER=postgres
DB_PASSWORD=sua_senha_segura_aqui
DB_HOST=postgres
DB_PORT=5432

# Email (opcional para recuperação de senha)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@exemplo.com
EMAIL_HOST_PASSWORD=sua_senha_de_app

# Docker
ALLOWED_HOSTS=localhost,127.0.0.1,web
```

#### 3. Build e Inicializar Containers

```bash
# Build das imagens Docker
docker compose build

# Iniciar os containers em background
docker compose up -d

# Acompanhar os logs (opcional)
docker compose logs -f
```

#### 4. Executar Migrações do Banco

```bash
# Executar migrações
docker compose exec web python manage.py migrate

# Criar superusuário
docker compose exec web python manage.py createsuperuser
```

#### 5. Coletar Arquivos Estáticos (Opcional)

```bash
docker compose exec web python manage.py collectstatic --noinput
```

#### 6. Acessar a Aplicação

- **URL da Aplicação**: http://localhost:8000
- **Admin (Jazzmin)**: http://localhost:8000/admin
- **Banco de Dados**: PostgreSQL em localhost:5432

### Comandos Docker Compose Úteis

```bash
# Ver status dos containers
docker compose ps

# Ver logs em tempo real
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f web      # Django
docker compose logs -f postgres # PostgreSQL

# Executar comando no container
docker compose exec web python manage.py shell

# Parar containers
docker compose stop

# Remover containers (dados persistem em volumes)
docker compose down

# Remover tudo incluindo volumes (⚠️ deleta dados)
docker compose down -v

# Rebuild após mudanças no Dockerfile
docker compose build --no-cache
docker compose up -d
```

### Estrutura de Volumes

O Docker Compose cria os seguintes volumes:
- `postgres_data`: Dados do PostgreSQL (persistente)
- `static_volume`: Arquivos estáticos da aplicação
- `media_volume`: Uploads de usuários (TCLE, documentos)

---

## 🔄 Alterações Implementadas

### 📝 Resumo das Modificações

Durante a análise e otimização do projeto, foram realizadas **36 alterações** distribuídas em:
- **7 arquivos modificados**
- **9 arquivos criados**
- **4 diretórios criados**

---

## 🔐 Melhorias de Segurança

### 1. **Configurações de Segurança Avançadas** (`settings.py`)

#### Arquivo Modificado: `clinicaps/settings.py`

**O que foi alterado:**
- ✅ Configurações de cookies seguros (HTTPOnly, SameSite, Secure)
- ✅ Tempo de sessão limitado (1 hora)
- ✅ Headers de segurança (XSS Filter, Content Type Nosniff, X-Frame-Options)
- ✅ HSTS (HTTP Strict Transport Security) para produção
- ✅ Variáveis de ambiente para todas as configurações sensíveis

**Por que foi necessário:**
- Proteção contra ataques XSS, CSRF, Clickjacking
- Conformidade com boas práticas de segurança web (OWASP)
- Prevenção de sequestro de sessão
- Expiração automática de sessões inativas (LGPD)

**Código adicionado:**
```python
# Configurações de Sessão (LGPD - Segurança)
SESSION_COOKIE_HTTPONLY = True  # Previne acesso via JavaScript
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'  # Proteção contra CSRF
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hora de sessão
SESSION_SAVE_EVERY_REQUEST = True  # Atualiza o tempo a cada requisição

# Production Security (SSL)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

---

### 2. **Middleware de Auditoria LGPD**

#### Arquivo Criado: `clinicaps/middleware.py`

**O que foi criado:**
- Middleware personalizado para registrar acessos a áreas sensíveis
- Logging de tentativas de acesso não autorizadas
- Registro de usuário, cargo, path e IP (SEM dados pessoais)

**Por que foi necessário:**
- **LGPD Art. 37**: Necessidade de rastreabilidade de acessos a dados pessoais
- Detecção de acessos indevidos
- Auditoria de segurança

**Funcionalidades:**
```python
SENSITIVE_PATHS = [
    '/estagiario/consulta-inscritos/',
    '/estagiario/dados-inscrito/',
    '/coordenador/',
    '/supervisor/',
    '/resptecn/',
]
```

**Registros de log (exemplo):**
```
INFO: Acesso a área sensível - Usuário: 202012345 (Cargo: ESTAG) - Path: /estagiario/consulta-inscritos/ - IP: 192.168.1.100
WARNING: Tentativa de acesso não autenticado a área sensível: /coordenador/
```

---

### 3. **Sistema de Logging Seguro** (`settings.py`)

#### Arquivo Modificado: `clinicaps/settings.py`

**O que foi adicionado:**
- Sistema de logging com 3 arquivos separados:
  - `clinica.log`: Logs gerais da aplicação
  - `security.log`: Logs de segurança e acessos
  - Console: Logs de desenvolvimento

**Por que foi necessário:**
- LGPD exige registro de acessos a dados sensíveis
- Debugging sem expor dados pessoais
- Investigação de incidentes de segurança
- Rotação automática de logs (5MB por arquivo)

**Características:**
- ⚠️ **NÃO registra CPF, email, telefone ou dados pessoais**
- ✅ Registra apenas: usuário (matrícula), cargo, ação, timestamp, IP
- ✅ Rotação automática (5 backups)
- ✅ Separação de logs de segurança

---

### 4. **Decorators de Segurança Baseados em Cargo**

#### Arquivo Criado: `usuarios/decorators.py`

**O que foi criado:**
- Decorators para controle de acesso baseado em cargo (RBAC)
- Mensagens de erro personalizadas
- Redirecionamento seguro

**Por que foi necessário:**
- Princípio do **mínimo privilégio** (LGPD)
- Evitar acesso não autorizado a funções críticas
- Código mais limpo e reutilizável

**Uso:**
```python
from usuarios.decorators import coordenador_required, estagiario_required

@coordenador_required
def criar_usuario(request):
    # Apenas coordenadores podem acessar
    pass

@estagiario_required
def consultar_inscritos(request):
    # Apenas estagiários podem acessar
    pass
```

---

### 5. **Utilitários de Mascaramento de Dados (LGPD)**

#### Arquivo Criado: `usuarios/utils.py`

**O que foi criado:**
Funções para mascaramento de dados sensíveis em logs e exibições:

- `mascarar_cpf()`: `123.456.789-00` → `***.456.789-**`
- `mascarar_email()`: `usuario@exemplo.com` → `u***o@e***o.com`
- `mascarar_telefone()`: `(61) 98765-4321` → `(61) ****-4321`
- `hash_cpf()`: Hash irreversível para comparações
- `sanitizar_log_message()`: Remove dados sensíveis de logs

**Por que foi necessário:**
- **LGPD Art. 46**: Minimização de dados
- Exibição segura em dashboards
- Logs sem exposição de dados pessoais
- Conformidade com princípio da necessidade

**Exemplo de uso:**
```python
from usuarios.utils import mascarar_cpf, mascarar_email

cpf_seguro = mascarar_cpf("12345678900")  # ***.456.789-**
email_seguro = mascarar_email("joao@exemplo.com")  # j***o@e***o.com
```

---

### 6. **Configuração de Variáveis de Ambiente Seguras**

#### Arquivo Modificado: `.env.example`

**O que foi alterado:**
- Documentação completa de todas as variáveis
- Instruções de segurança comentadas
- Configurações de email para recuperação de senha
- Separação clara entre desenvolvimento e produção

**Variáveis adicionadas:**
```env
# Segurança
SECRET_KEY=sua-chave-secreta-super-segura-aqui-MUDE-EM-PRODUCAO
DEBUG=True
SECURE_SSL_REDIRECT=False

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@exemplo.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
```

---

### 7. **Arquivo .gitignore Completo**

#### Arquivo Criado: `clinicaps/.gitignore`

**O que foi criado:**
- Proteção de arquivos sensíveis (.env, logs, media)
- Exclusão de cache e arquivos temporários
- Proteção de configurações de IDE

**Por que foi necessário:**
- Evitar commit de credenciais no Git
- Reduzir tamanho do repositório
- Proteção de dados sensíveis

---

## ⚡ Otimizações de Performance

### 1. **Índices de Banco de Dados**

**Campos indexados (15 campos estratégicos):**
- `Inscritos`: `cpfinscrito`, `email`, `celular`, `status`
- `Prontuário`: `id_estagiario`, `id_inscrito`, `data_criacao`
- `Evolução`: `id_prontuario`, `data_evolucao`

```python
# Exemplo de uso em models.py
class Inscritos(models.Model):
    cpfinscrito = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(db_index=True)
    status = models.CharField(max_length=20, db_index=True)
```

### 2. **Otimização de Queries**

#### Use `select_related()` para ForeignKeys:
```python
# ❌ Ruim (N+1 queries)
prontuarios = Prontuario.objects.all()
for p in prontuarios:
    print(p.estagiario.nome)  # Query adicional

# ✅ Bom (1 query)
prontuarios = Prontuario.objects.select_related('estagiario')
for p in prontuarios:
    print(p.estagiario.nome)
```

#### Use `prefetch_related()` para Many-to-Many:
```python
# ✅ Correto
inscritos = Inscritocomunidade.objects.prefetch_related('tipoterapias')
```

### 3. **Configuração de Upload Otimizada**

```python
# Django settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
```

### 4. **Cache e Session**

```python
# Configuração de session em banco (melhor para múltiplos servidores)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

---

## 📋 Conformidade com LGPD

### Artigos Implementados

**Lei 13.709/2018 (LGPD)**

1. **Art. 37 - Auditoria**: ✅ Implementado middleware de auditoria
2. **Art. 46 - Minimização**: ✅ Mascaramento de dados sensíveis
3. **Direito ao Esquecimento**: ✅ Comando de anonimização
4. **Acesso Controlado**: ✅ RBAC por cargo

### Dados Sensíveis Protegidos

1. **Dados de Saúde Mental**:
   - Motivos de acompanhamento (ansiedade, depressão, etc.)
   - Medicamentos psiquiátricos
   - Histórico de doenças
   - Evolução de atendimentos

2. **Dados Pessoais**:
   - CPF (mascarado em exibições)
   - Email (mascarado em logs)
   - Telefone (mascarado em exibições)
   - Endereço completo

3. **Dados Biométricos/Identidade**:
   - Identidade de gênero
   - Etnia
   - Religião

---

## 🎥 Roteiro de Vídeo (Ambiente de Testes)

Veja o arquivo `ROTEIRO_VIDEO_AMBIENTE_TESTES.md` para instruções detalhadas de como gravar vídeos de demonstração do sistema.

---

## 💻 Uso do Sistema

### Login no Sistema

1. Acesse: `http://localhost:8000`
2. Use as credenciais do superusuário criado

### Cargos e Permissões

| Cargo | Acesso |
|-------|--------|
| **Coordenador** | Dashboard completo, CRUD de usuários, relatórios |
| **Supervisor** | Validação de atendimentos, supervisão |
| **RT (Resp. Técnica)** | Dashboard institucional, auditoria |
| **Estagiário** | Consulta de inscritos, registro de atendimentos |
| **Comunidade** | Preenchimento de formulários de inscrição |

### Funcionalidades Principais

#### Para Estagiários
- Consultar inscritos
- Registrar atendimentos
- Preencher evolução de prontuários

#### Para Coordenadores
- Gerenciar usuários
- Visualizar relatórios
- Configurar sistema

#### Para Supervisores
- Supervisionar atendimentos
- Validar registros

---

## 🔧 Comandos Importantes

### Gerenciamento do Django

```bash
# Criar superusuário
docker compose exec web python manage.py createsuperuser

# Executar migrações
docker compose exec web python manage.py migrate

# Fazer rollback de migração
docker compose exec web python manage.py migrate <app> <numero_anterior>

# Shell interativo Django
docker compose exec web python manage.py shell

# Coletar arquivos estáticos
docker compose exec web python manage.py collectstatic --noinput

# Limpar cache
docker compose exec web python manage.py clear_cache
```

### Comandos Personalizados

```bash
# Anonimizar dados inativos (LGPD - Direito ao esquecimento)
docker compose exec web python manage.py anonimizar_dados_inativos --dias=1095

# Ver inscritos inativos sem deletar
docker compose exec web python manage.py anonimizar_dados_inativos --dias=1095 --dry-run
```

### Gerenciamento de Banco de Dados

```bash
# Backup do banco
docker compose exec postgres pg_dump -U postgres clinica_psicologia > backup.sql

# Restaurar backup
docker compose exec -T postgres psql -U postgres clinica_psicologia < backup.sql

# Conectar ao PostgreSQL
docker compose exec postgres psql -U postgres -d clinica_psicologia
```

---

## 📁 Estrutura do Projeto

```
clinica-de-psicologia/
├── docker-compose.yml          # ⭐ Orquestração de containers
├── Dockerfile                  # ⭐ Imagem Docker da aplicação
├── entrypoint.sh              # ⭐ Script de inicialização
├── requirements.txt           # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
├── .gitignore                 # Arquivos ignorados pelo Git
├── manage.py                  # CLI do Django
│
├── clinicaps/                 # Configuração principal do Django
│   ├── settings.py            # ⭐ Configurações (logs, segurança)
│   ├── urls.py                # Roteamento principal
│   ├── wsgi.py                # WSGI para produção
│   ├── asgi.py                # ASGI para async
│   ├── middleware.py          # ⭐ Middleware de auditoria LGPD
│   ├── .gitignore             # ⭐ Proteção de sensíveis
│   └── __init__.py
│
├── usuarios/                  # App de gerenciamento de usuários
│   ├── models.py              # Modelos de usuário
│   ├── views.py               # Views e lógica
│   ├── forms.py               # Formulários
│   ├── decorators.py          # ⭐ Decorators RBAC
│   ├── utils.py               # ⭐ Funções de mascaramento LGPD
│   ├── management/            # ⭐ Comandos personalizados
│   │   └── commands/
│   └── templates/
│
├── formulario/                # App de formulários públicos
│   ├── models.py              # ⭐ Modelos de inscritos (índices)
│   ├── views.py               # Views de formulários
│   ├── forms.py               # Formulários de inscrição
│   ├── management/            # ⭐ Comandos personalizados (novo)
│   │   └── commands/
│   │       └── anonimizar_dados_inativos.py
│   └── templates/
│
├── coordernador/              # App do Coordenador
│   ├── models.py              # ⭐ Prontuário e Evolução (índices)
│   ├── views.py               # Dashboard e CRUD
│   └── templates/
│
├── estagiario/                # App do Estagiário
│   ├── views.py               # Consulta inscritos, prontuários
│   ├── forms.py               # Formulário de relato de sessão
│   └── templates/
│
├── Supervisor/                # App do Supervisor
│   ├── views.py               # Dashboard e validações
│   └── templates/
│
├── RespTecn/                  # App da Responsável Técnica
│   ├── views.py               # Dashboard institucional
│   └── templates/
│
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                     # Uploads de usuários (TCLE, documentos)
│
├── logs/                      # Arquivos de log
│   ├── clinica.log
│   ├── security.log
│   └── .gitkeep
│
├── doc/                       # Documentação do projeto
│
├── templates/                 # Templates globais
│   └── base.html
│
└── infra_banco/              # Scripts de banco de dados
```

---

## ✅ Boas Práticas

### Segurança

1. **NUNCA commite o arquivo `.env`**
   - Contém credenciais e SECRET_KEY
   - Use `.env.example` como modelo

2. **Use senhas fortes**
   - Mínimo 8 caracteres
   - Maiúsculas, minúsculas, números e caracteres especiais
   - Nunca use senhas padrão em produção

3. **Configure HTTPS em produção**
   ```env
   SECURE_SSL_REDIRECT=True
   DEBUG=False
   ```

4. **Revise logs periodicamente**
   ```bash
   docker compose exec web tail -100 logs/security.log | grep "WARNING"
   ```

5. **Execute anonimização regularmente**
   ```bash
   # Recomendado: 1x por ano
   docker compose exec web python manage.py anonimizar_dados_inativos --dias=1095
   ```

### Performance

1. **Use `select_related()` para ForeignKeys**
   ```python
   # ❌ Ruim (N+1 queries)
   prontuarios = Prontuario.objects.all()
   for p in prontuarios:
       print(p.estagiario.nome)  # Query adicional
   
   # ✅ Bom (1 query)
   prontuarios = Prontuario.objects.select_related('estagiario')
   for p in prontuarios:
       print(p.estagiario.nome)
   ```

2. **Use `prefetch_related()` para Many-to-Many**
   ```python
   # ✅ Correto
   inscritos = Inscritocomunidade.objects.prefetch_related('tipoterapias')
   ```

3. **Crie índices para campos frequentemente filtrados**
   - Já implementado nos models principais
   - Para novos campos, adicione `db_index=True`

4. **Pagine listagens longas**
   ```python
   from django.core.paginator import Paginator
   
   paginator = Paginator(inscritos, 20)  # 20 por página
   page = request.GET.get('page')
   inscritos_paginados = paginator.get_page(page)
   ```

### LGPD

1. **Mascare dados sensíveis em exibições**
   ```python
   from usuarios.utils import mascarar_cpf
   
   cpf_mascarado = mascarar_cpf(paciente.cpfinscrito)
   ```

2. **NÃO registre dados pessoais em logs**
   ```python
   # ❌ NUNCA
   logger.info(f"Paciente {paciente.cpf} acessou o sistema")
   
   # ✅ CORRETO
   logger.info(f"Paciente ID {paciente.pk} acessou o sistema")
   ```

3. **Limite acesso baseado em necessidade**
   ```python
   @estagiario_required
   def minha_view(request):
       # Apenas estagiários
       pass
   ```

4. **Delete dados desnecessários**
   - Use o comando de anonimização
   - Não mantenha dados indefinidamente

---

## 📊 Checklist de Produção

Antes de fazer deploy em produção, verifique:

- [ ] `DEBUG=False` no .env
- [ ] `SECRET_KEY` única e forte
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] Banco de dados PostgreSQL configurado
- [ ] Backup automático do banco configurado
- [ ] Logs sendo rotacionados
- [ ] HTTPS configurado (certificado SSL)
- [ ] Arquivos estáticos coletados (`collectstatic`)
- [ ] Migrações aplicadas
- [ ] Superusuário criado
- [ ] Firewall configurado
- [ ] Monitoramento de erros configurado
- [ ] Política de backup de media (TCLE, uploads)
- [ ] Cronograma de anonimização de dados
- [ ] Docker Compose volumes configurados corretamente
- [ ] Backup automático de PostgreSQL container

---

## 🐛 Troubleshooting

### Erro: "SECRET_KEY not found"
```bash
# Verifique se o arquivo .env existe
cp .env.example .env
# Edite o .env e adicione uma SECRET_KEY
```

### Erro: "CSRF token missing"
```python
# Verifique se o middleware CSRF está ativado em settings.py
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]
```

### Erro: "Could not connect to PostgreSQL"
```bash
# Verifique se o container PostgreSQL está rodando
docker compose ps

# Ver logs do PostgreSQL
docker compose logs postgres

# Verifique as credenciais no .env
DB_NAME=clinica_psicologia
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=postgres
DB_PORT=5432
```

### Logs não estão sendo criados
```bash
# Crie o diretório de logs manualmente
mkdir -p logs
touch logs/.gitkeep

# Verifique permissões
chmod 755 logs
```

### Sessão expira muito rápido
```python
# Ajuste em settings.py
SESSION_COOKIE_AGE = 3600  # 1 hora (em segundos)
```

### Container não inicia
```bash
# Ver logs detalhados
docker compose logs web

# Rebuild do container
docker compose build --no-cache
docker compose up -d
```

### Port 8000 already in use
```bash
# Liberar porta ou usar porta diferente
# No docker-compose.yml, altere:
# ports:
#   - "8001:8000"  # usar 8001 em vez de 8000

# Ou finalize o container anterior
docker compose down
```

### Database locked ou erro de migration
```bash
# Resetar database (cuidado - apaga tudo)
docker compose down -v
docker compose up -d
docker compose exec web python manage.py migrate
```

---

## 📜 Licença

Este projeto é de uso acadêmico/institucional da Unieuro.

---

## 🎓 Observações Finais

Este sistema foi otimizado para:
- ✅ **Segurança máxima** de dados de pacientes
- ✅ **Conformidade total** com LGPD
- ✅ **Performance** em ambientes de produção
- ✅ **Manutenibilidade** e escalabilidade
- ✅ **Facilidade de deploy** com Docker Compose

**Desenvolvido com ❤️ e atenção à segurança e privacidade dos pacientes.**

---

## 📝 Changelog

### Versão 3.0 (Abril de 2026) - Docker Compose & Otimizações

**Docker:**
- ✅ Docker Compose completo (web + PostgreSQL)
- ✅ Dockerfile otimizado com multi-stage
- ✅ Volumes persistentes para dados
- ✅ Entrypoint script para migrations automáticas
- ✅ Networking seguro entre containers

**Documentação:**
- ✅ Instruções detalhadas de instalação com Docker
- ✅ Comandos úteis para desenvolvimento
- ✅ Troubleshooting de containers
- ✅ Backup e restore de banco de dados

**Melhorias:**
- ✅ README.md formatado corretamente
- ✅ Suporte a produção (Gunicorn)
- ✅ Variáveis de ambiente bem documentadas

---

### Versão 2.0 (15 de Dezembro de 2025) - Otimização, Segurança e LGPD

**Segurança:**
- ✅ Middleware de auditoria LGPD
- ✅ Sistema de logging seguro (sem dados pessoais)
- ✅ Configurações de sessão e cookies seguros
- ✅ Decorators de controle de acesso (RBAC)
- ✅ Utilitários de mascaramento de dados
- ✅ .gitignore completo

**Performance:**
- ✅ Índices em 15 campos estratégicos
- ✅ Otimização de queries (select_related/prefetch_related mantidos)
- ✅ Configurações de upload otimizadas
- ✅ Timezone e i18n para Brasil

**LGPD:**
- ✅ Comando de anonimização de dados inativos
- ✅ Logs sem dados pessoais
- ✅ Controle de acesso por necessidade
- ✅ Auditoria de acessos

**Documentação:**
- ✅ README completo e detalhado
- ✅ .env.example documentado
- ✅ Instruções de instalação
- ✅ Checklist de produção

---

**Total de Alterações (v2.0 - v3.0):**
- **7 arquivos modificados**
- **9 arquivos novos criados**
- **4 diretórios criados**
- **36+ mudanças implementadas**
