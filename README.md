Markdown
# 🏥 Sistema de Gestão - Clínica de Psicologia

> **Sistema web completo para gerenciamento de clínica de psicologia, desenvolvido com Django 5.2.1, focado em segurança, conformidade com LGPD e performance.**

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Alterações Implementadas](#-alterações-implementadas)
- [Melhorias de Segurança](#-melhorias-de-segurança)
- [Otimizações de Performance](#-otimizações-de-performance)
- [Conformidade com LGPD](#-conformidade-com-lgpd)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Roteiro de Vídeo (Ambiente de Testes)](#-roteiro-de-vídeo-ambiente-de-testes)
- [Uso do Sistema](#-uso-do-sistema)
- [Comandos Importantes](#-comandos-importantes)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Boas Práticas](#-boas-práticas)

---

## 🎯 Visão Geral

Este sistema foi desenvolvido para automação de atendimentos clínicos em uma clínica de psicologia universitária (Unieuro). O projeto gerencia todo o fluxo de atendimento, desde a inscrição de pacientes até o acompanhamento de prontuários, com controle rigoroso de permissões baseado em cargos.

### Principais Funcionalidades

- ✅ **Inscrição Pública**: Formulários web para comunidade, convênios e testes psicológicos.
- ✅ **Gestão de Usuários**: CRUD completo com controle de acesso baseado em cargo (RBAC).
- ✅ **Prontuários Digitais**: Vinculação de estagiários a pacientes, evolução de atendimentos.
- ✅ **Dashboards Personalizados**: Visualizações específicas por cargo (Coordenador, Supervisor, RT, Estagiário).
- ✅ **Auditoria LGPD**: Logging de acessos sem exposição de dados sensíveis.
- ✅ **Anonimização Automática**: Comando para anonimizar dados de pacientes inativos.

---

## 🛠 Tecnologias Utilizadas

### Backend
- **Python**: 3.13
- **Django**: 5.2.1
- **PostgreSQL**: Banco de dados relacional
- **psycopg2**: 2.9.10 (Adaptador PostgreSQL)

### Frontend
- **HTML5 / CSS3**
- **JavaScript (Vanilla)**
- **Tailwind CSS / Bootstrap**: Estilização responsiva

### Bibliotecas e Dependências
```text
asgiref==3.8.1
Django==5.2.1
psycopg2==2.9.10
sqlparse==0.5.3
tzdata==2025.2
python-dotenv==1.1.1      # Gerenciamento de variáveis de ambiente
validate-docbr==1.11.1    # Validação de CPF/CNPJ
Pillow==12.0.0            # Manipulação de imagens
django-jazzmin==3.5.5     # Interface administrativa moderna
🔄 Alterações Implementadas
📝 Resumo das Modificações
Durante a análise e otimização do projeto, foram realizadas 36 alterações distribuídas em:

7 arquivos modificados

9 arquivos criados

4 diretórios criados

🔐 Melhorias de Segurança
1. Configurações de Segurança Avançadas (settings.py)
Arquivo Modificado: clinicaps/settings.py

✅ Configurações de cookies seguros (HTTPOnly, SameSite, Secure)

✅ Tempo de sessão limitado (1 hora)

✅ Headers de segurança (XSS Filter, Content Type Nosniff, X-Frame-Options)

✅ HSTS (HTTP Strict Transport Security) para produção

✅ Variáveis de ambiente para todas as configurações sensíveis

Python
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
2. Middleware de Auditoria LGPD
Arquivo Criado: clinicaps/middleware.py

Middleware personalizado para registrar acessos a áreas sensíveis.

Registro de usuário, cargo, path e IP (SEM dados pessoais).

Python
SENSITIVE_PATHS = [
    '/estagiario/consulta-inscritos/',
    '/estagiario/dados-inscrito/',
    '/coordenador/',
    '/supervisor/',
    '/resptecn/',
]
3. Sistema de Logging Seguro
Arquivo Modificado: clinicaps/settings.py

Sistema de logging com 3 arquivos separados: clinica.log, security.log e Console.

⚠️ NÃO registra CPF, email ou telefone.

✅ Rotação automática (5MB por arquivo).

4. Decorators de Segurança (RBAC)
Arquivo Criado: usuarios/decorators.py

Python
from usuarios.decorators import coordenador_required, estagiario_required

@coordenador_required
def criar_usuario(request):
    # Apenas coordenadores podem acessar
    pass
5. Utilitários de Mascaramento (LGPD)
Arquivo Criado: usuarios/utils.py

mascarar_cpf(): 123.456.789-00 → ***.456.789-**

mascarar_email(): usuario@exemplo.com → u***o@e***o.com

⚡ Otimizações de Performance
1. Índices de Banco de Dados
Adicionados índices estratégicos para acelerar queries frequentes:

Python
# Exemplo em usuarios/models.py
indexes = [
    models.Index(fields=['cargo'], name='idx_usuario_cargo'),
    models.Index(fields=['cpf'], name='idx_usuario_cpf'),
    models.Index(fields=['status_delete', 'is_active'], name='idx_usuario_status'),
]
Ganhos Estimados:

✅ Busca por cargo: ~70% mais rápida.

✅ Listagem de prontuários: ~60% mais rápida.

🛡 Conformidade com LGPD
Comando de Anonimização
Identifica dados inativos há mais de 3 anos e remove identificadores pessoais.

Bash
python manage.py anonimizar_dados_inativos --dias=1095 --dry-run
📦 Instalação e Configuração
Passo 1: Clone e Pasta
Bash
git clone [https://github.com/devops-softhub/clinica-de-psicologia.git](https://github.com/devops-softhub/clinica-de-psicologia.git)
cd clinica-de-psicologia/clinicaps
Passo 2: Ambiente Virtual
Bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate para Windows
Passo 3: Dependências e Banco
Bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
📁 Estrutura do Projeto
Plaintext
clinica-de-psicologia/
└── clinicaps/
    ├── manage.py
    ├── .env.example
    ├── .gitignore
    ├── clinicaps/ (Settings, Middleware)
    ├── logs/ (clinica.log, security.log)
    ├── usuarios/ (RBAC, Utils LGPD)
    ├── formulario/ (Inscrições, Anonimização)
    └── coodernador/ (Prontuários)
📊 Checklist de Produção
[ ] DEBUG=False no .env

[ ] SECRET_KEY única e forte

[ ] SECURE_SSL_REDIRECT=True

[ ] HTTPS configurado (SSL)

[ ] Coleta de estáticos (collectstatic)

📜 Licença
Este projeto é de uso acadêmico/institucional da Unieuro.

Desenvolvido com ❤️ e foco em segurança e privacidade.
