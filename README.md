# Clínica de Psicologia - Sistema unieuro

Sistema web Django para gestão de clínica de psicologia.

## 🚀 Pré-requisitos

- **Python 3.11+**
- **PostgreSQL 14+**
- **Git**

## 📦 Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/softhub-unieuro/Clinica-de-psicologia.git
cd Clinica-de-psicologia/clinica-de-psicologia
```

### 2. Crie o ambiente virtual

```bash
python -m venv env
```

### 3. Ative o ambiente virtual

- **Linux/macOS:**
  ```bash
  source env/bin/activate
  ```

- **Windows:**
  ```bash
  env\Scripts\activate
  ```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados

Crie o banco no PostgreSQL:

```sql
CREATE DATABASE clinica;
```

### 6. Configure as variáveis de ambiente

Edite o arquivo `clinicaps/.env`:

```env
# Django Settings
APP_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui

# Database Settings
DATABASE_NAME=clinica
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_CONN_MAX_AGE=600
DATABASE_SSL_REQUIRE=False
```

> ⚠️ **Importante:** Gere uma `SECRET_KEY` segura para produção. Você pode gerar uma em: [djsecretkey.com](https://djsecretkey.com)

### 7. Execute as migrações

```bash
cd clinicaps
python manage.py migrate
```

### 8. (Opcional) Seed de usuários

Para criar usuários iniciais de teste:

```bash
python manage.py seed_users
python manage.py seed_inscritos
```

### 9. Crie o superusuário

```bash
python manage.py createsuperuser
```

## ▶️ Executando o projeto

```bash
python manage.py runserver
```

Acesse:
- **Aplicação:** http://127.0.0.1:8000
- **Admin Django:** http://127.0.0.1:8000/admin

## 📁 Estrutura

```
clinica-de-psicologia/
├── clinicaps/              # Projeto Django
│   ├── .env               # Variáveis de ambiente
│   ├── clinicaps/         # Configurações Django
│   │   └── settings.py   # Settings principal
│   ├── manage.py         # CLI do Django
│   ├── usuarios/        # App de usuários
│   ├── formulario/      # App de formulários
│   ├── estagiario/      # App estagiário
│   ├── Supervisor/      # App Supervisor
│   ├── RespTecn/         # App Responsável Técnico
│   └── coodernador/      # App Coordenador
├── BD/
│   └── DDL.sql          # Schema do banco (referência)
├── requirements.txt     # Dependências Python
└── env/                # Ambiente virtual (gerado)
```

## 🔧 Comandos úteis

| Comando | Descrição |
|---------|------------|
| `python manage.py migrate` | Criar/migrar banco |
| `python manage.py makemigrations` | Criar novas migrações |
| `python manage.py createsuperuser` | Criar admin |
| `python manage.py seed_users` | Criar usuários teste |
| `python manage.py collectstatic` | Coletar static files |

## 🐳 Docker (Opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```bash
# Build e rode
docker build -t clinica-psicologia .
docker run -p 8000:8000 clinica-psicologia
```

## 📝 Licença

GPL-3.0 - SoftHub UniEuro