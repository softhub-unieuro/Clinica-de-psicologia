# 🏥 Sistema de Gestão — Clínica de Psicologia

Sistema web desenvolvido em Django para gestão de clínica de psicologia.

---

## 🚀 Executando o projeto (com Docker)

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

> Apenas isso. Não é necessário instalar Python, PostgreSQL ou qualquer outra dependência local.

---

### 1. Clone o repositório

```bash
git clone https://github.com/softhub-unieuro/Clinica-de-psicologia.git
cd Clinica-de-psicologia
```

### 2. Configure as variáveis de ambiente

```bash
cp clinica-de-psicologia/.env.example clinica-de-psicologia/.env
```

Edite o arquivo `.env` com suas configurações:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

DB_NAME=clinica_db
DB_USER=clinica_user
DB_PASSWORD=clinica_pass
DB_HOST=db
DB_PORT=5432
```

> **Atenção:** O valor de `DB_HOST` deve ser `db` (nome do serviço no Docker), não `localhost`.

### 3. Suba os containers

```bash
docker-compose up -d
```

Pronto. O comando irá:
- Baixar as imagens necessárias
- Construir a imagem da aplicação
- Rodar as migrações automaticamente
- Coletar os arquivos estáticos
- Iniciar o servidor Gunicorn

### 4. Acesse a aplicação

```
http://localhost:8000
```

---

## 🛠 Comandos úteis

```bash
# Ver logs em tempo real
docker-compose logs -f web

# Acessar o shell do container da aplicação
docker-compose exec web bash

# Rodar comandos Django manualmente
docker-compose exec web python manage.py createsuperuser

# Parar os containers
docker-compose down

# Parar e remover volumes (apaga dados do banco)
docker-compose down -v
```

---

## 📁 Estrutura relevante

```
Clinica-de-psicologia/
├── Dockerfile                  # Receita da imagem da aplicação
├── docker-compose.yml          # Orquestração dos serviços
├── entrypoint.sh               # Script de inicialização do container
└── clinica-de-psicologia/      # Código-fonte Django
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    └── clinicaps/              # Módulo principal (settings, urls, wsgi)
```

---

## 👥 Contribuidores

Projeto desenvolvido por **softhub-unieuro**.
