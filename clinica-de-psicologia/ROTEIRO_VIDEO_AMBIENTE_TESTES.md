# Roteiro de Vídeo: Ambiente de Testes - Clínica de Psicologia

## 🎬 Roteiro de Vídeo (Ambiente de Testes)
Para gravar ou seguir um passo a passo focado em preparação de ambiente para testes, consulte este roteiro.

### Pré-requisitos
- Python 3.13+
- PostgreSQL 12+
- Git

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/devops-softhub/clinica-de-psicologia.git
cd clinica-de-psicologia/clinica-de-psicologia
```

### Passo 2: Crie um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### Passo 3: Instale as Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configure o Banco de Dados PostgreSQL
No PostgreSQL, execute:
```sql
CREATE DATABASE clinica_psicologia;
CREATE USER postgres WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE clinica_psicologia TO postgres;
```

### Passo 5: Configure as Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

Arquivo .env (exemplo):
```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=clinica_psicologia
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### Passo 6: Execute as Migrações
```bash
python clinicaps/manage.py makemigrations
python clinicaps/manage.py migrate
```

### Passo 7: Crie os Índices de Performance
Os índices são criados automaticamente pelas migrações.
Verifique no PostgreSQL:
```bash
psql -d clinica_psicologia -c "\d+ inscritocomunidade"
```

### Passo 8: Crie um Superusuário
```bash
python clinicaps/manage.py createsuperuser
```

### Passo 9: Popule o Banco (Opcional)
Para dados de teste:
```bash
python seed_users.py
python seed_inscritos.py
```

### Passo 10: Execute o Servidor
```bash
python clinicaps/manage.py runserver
```
Acesse: http://127.0.0.1:8000

## 📋 Checklist para Gravação de Vídeo
- [ ] Mostrar instalação do Python
- [ ] Demonstrar criação do ambiente virtual
- [ ] Explicar instalação das dependências
- [ ] Configurar PostgreSQL
- [ ] Editar arquivo .env
- [ ] Executar migrações
- [ ] Criar superusuário
- [ ] Popular banco com dados de teste
- [ ] Iniciar servidor e acessar aplicação
- [ ] Testar formulários e admin

## 🔧 Comandos de Verificação
```bash
# Verificar Python
python --version

# Verificar PostgreSQL
psql --version

# Verificar Git
git --version

# Verificar ambiente virtual
which python  # Deve apontar para venv/bin/python

# Verificar migrações
python clinicaps/manage.py showmigrations

# Verificar banco
psql -d clinica_psicologia -c "SELECT * FROM inscritocomunidade LIMIT 5;"
```

## 🚨 Possíveis Problemas e Soluções
- **Erro de porta**: Mude para 8001
- **Erro de banco**: Verifique credenciais no .env
- **Erro de dependências**: Reinstale requirements.txt
- **Erro de migrações**: Execute makemigrations primeiro