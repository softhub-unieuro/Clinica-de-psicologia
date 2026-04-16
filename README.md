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
- [Uso do Sistema](#-uso-do-sistema)
- [Estrutura do Projeto](#-estrutura-do-projeto)

---

## 🎯 Visão Geral

Este sistema foi desenvolvido para automação de atendimentos clínicos em uma clínica de psicologia universitária (Unieuro). O projeto gerencia todo o fluxo de atendimento, desde a inscrição de pacientes até o acompanhamento de prontuários.

### Principais Funcionalidades

- ✅ **Inscrição Pública**: Formulários web para comunidade e convênios.
- ✅ **Gestão de Usuários**: Controle de acesso baseado em cargo (RBAC).
- ✅ **Prontuários Digitais**: Evolução de atendimentos e prontuários digitais.
- ✅ **Auditoria LGPD**: Logging de acessos sem exposição de dados sensíveis.

---

## 🛠 Tecnologias Utilizadas

### Backend
- **Python**: 3.13 / **Django**: 5.2.1
- **PostgreSQL**: Banco de dados relacional

### Bibliotecas e Dependências
```text
asgiref==3.8.1
Django==5.2.1
psycopg2==2.9.10
python-dotenv==1.1.1
django-jazzmin==3.5.5
🔄 Alterações Implementadas
📝 Resumo das Modificações
Durante a análise e otimização do projeto, foram realizadas 36 alterações distribuídas em:

📂 7 arquivos modificados

📂 9 arquivos criados

📂 4 diretórios criados

🔐 Melhorias de Segurança
1. Configurações de Segurança (settings.py)
✅ Cookies seguros (HTTPOnly, SameSite, Secure)

✅ Tempo de sessão limitado (1 hora)

✅ Headers de segurança e HSTS para produção

Python
# Exemplo de Configuração de Sessão
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600 
2. Middleware de Auditoria LGPD
Criado para registrar acessos a áreas sensíveis como prontuários e dados de inscritos, registrando apenas o ID do usuário e IP.

⚡ Otimizações de Performance
1. Índices de Banco de Dados
Adicionados índices estratégicos para acelerar buscas por CPF, cargo e matrícula.

Python
indexes = [
    models.Index(fields=['cargo'], name='idx_usuario_cargo'),
    models.Index(fields=['cpf'], name='idx_usuario_cpf'),
]
🛡 Conformidade com LGPD
Comando de Anonimização
Identifica dados inativos há mais de 3 anos e remove identificadores pessoais, mantendo apenas dados estatísticos.

Bash
python manage.py anonimizar_dados_inativos --dias=1095 --dry-run
📦 Instalação e Configuração
Passo 1: Clone e Pasta
Bash
git clone https://github.com/softhub-unieuro/Clinica-de-psicologia.git
cd Clinica-de-psicologia
Passo 2: Ambiente e Banco
Bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
📁 Estrutura do Projeto
Plaintext
clinica-de-psicologia/
└── clinicaps/
    ├── clinicaps/ (Settings, Middleware)
    ├── logs/ (clinica.log, security.log)
    ├── usuarios/ (RBAC, Utils LGPD)
    └── formulario/ (Inscrições, Anonimização)
📊 Checklist de Produção
[ ] DEBUG=False no .env

[ ] SECRET_KEY única e forte

[ ] SECURE_SSL_REDIRECT=True

[ ] HTTPS configurado (SSL)

📜 Licença
Este projeto é de uso acadêmico/institucional da Unieuro.
