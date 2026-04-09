# 🔒 Configuração de Segurança do Banco de Dados PostgreSQL

## ✅ Implementado

Foi adicionado suporte para **conexões SSL/TLS seguras** com o banco de dados PostgreSQL, incluindo:

- ✅ Pool de conexões (CONN_MAX_AGE)
- ✅ SSL configurável por ambiente
- ✅ Timeout de conexão
- ✅ Múltiplos modos SSL (disable, prefer, require, verify-ca, verify-full)

---

## 📋 Configuração do Arquivo `.env`

### 1. **Copiar o arquivo de exemplo**

```bash
cd clinica-de-psicologia/clinicaps
cp .env.example .env
```

### 2. **Editar as variáveis no arquivo `.env`**

Abra o arquivo `.env` e configure:

```env
# ============================================
# BANCO DE DADOS POSTGRESQL
# ============================================

DATABASE_NAME=clinica_db          # Nome do banco
DATABASE_USER=postgres             # Usuário do PostgreSQL
DATABASE_PASSWORD=sua_senha_123    # Senha do PostgreSQL
DATABASE_HOST=localhost            # Host (localhost ou nome do container Docker)
DATABASE_PORT=5432                 # Porta padrão do PostgreSQL

# ============================================
# SEGURANÇA DO BANCO DE DADOS (SSL)
# ============================================

DATABASE_CONN_MAX_AGE=600          # Pool de conexões (10 minutos)
DATABASE_SSL_REQUIRE=False         # True para produção, False para desenvolvimento
DATABASE_SSL_MODE=prefer           # Modo SSL (prefer, require, verify-ca, verify-full)
```

---

## 🎯 Modos SSL Disponíveis

| Modo           | Descrição                                          | Uso Recomendado |
|----------------|-----------------------------------------------------|-----------------|
| `disable`      | Sem SSL                                             | Desenvolvimento local apenas |
| `prefer`       | Tenta SSL, aceita sem SSL se falhar (padrão)       | Desenvolvimento |
| `require`      | SSL obrigatório, mas não verifica certificado      | Produção básica |
| `verify-ca`    | SSL obrigatório com verificação de CA              | Produção segura |
| `verify-full`  | SSL obrigatório com verificação completa           | Produção máxima segurança |

---

## 🛠️ Configuração por Ambiente

### **Desenvolvimento Local**

```env
DEBUG=True
DATABASE_HOST=localhost
DATABASE_PASSWORD=senha_dev
DATABASE_SSL_REQUIRE=False
DATABASE_SSL_MODE=prefer
```

### **Codespace/Docker**

```env
DEBUG=True
DATABASE_HOST=postgres-codespace
DATABASE_NAME=clinica_db
DATABASE_USER=postgres
DATABASE_PASSWORD=senha123
DATABASE_SSL_REQUIRE=False
DATABASE_SSL_MODE=prefer
```

### **Produção (AWS RDS, Azure, Google Cloud)**

```env
DEBUG=False
DATABASE_HOST=seu-banco.rds.amazonaws.com
DATABASE_NAME=clinica_db
DATABASE_USER=admin_db
DATABASE_PASSWORD=senha_super_segura
DATABASE_SSL_REQUIRE=True
DATABASE_SSL_MODE=require
SECURE_SSL_REDIRECT=True
```

---

## 🔐 Pool de Conexões (CONN_MAX_AGE)

O `CONN_MAX_AGE` mantém conexões abertas para reutilização:

- **Valor**: Tempo em segundos (600 = 10 minutos)
- **Benefício**: Reduz overhead de criar novas conexões
- **Produção**: 600 - 3600 (10 min - 1 hora)
- **Desenvolvimento**: 0 ou 300 (fecha após cada request ou 5 min)

```env
DATABASE_CONN_MAX_AGE=600  # Recomendado para produção
```

---

## 🐳 Configurando SSL no PostgreSQL Docker

### **Opção 1: Docker Sem SSL (Desenvolvimento)**

```bash
docker run --name postgres-codespace \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=clinica_db \
  -p 5432:5432 \
  -d postgres
```

Arquivo `.env`:
```env
DATABASE_SSL_REQUIRE=False
DATABASE_SSL_MODE=disable
```

### **Opção 2: Docker Com SSL Habilitado**

1. **Criar certificados SSL** (auto-assinados para dev):

```bash
# Dentro do container
docker exec -it postgres-codespace bash

# Gerar certificado auto-assinado
openssl req -new -x509 -days 365 -nodes \
  -text -out /var/lib/postgresql/data/server.crt \
  -keyout /var/lib/postgresql/data/server.key \
  -subj "/CN=localhost"

# Ajustar permissões
chmod 600 /var/lib/postgresql/data/server.key
chown postgres:postgres /var/lib/postgresql/data/server.*
```

2. **Reiniciar container com SSL**:

```bash
docker run --name postgres-ssl \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=clinica_db \
  -p 5432:5432 \
  -d postgres \
  postgres -c ssl=on \
  -c ssl_cert_file=/var/lib/postgresql/data/server.crt \
  -c ssl_key_file=/var/lib/postgresql/data/server.key
```

3. **Configurar `.env`**:

```env
DATABASE_SSL_REQUIRE=True
DATABASE_SSL_MODE=require
```

---

## ✅ Testar a Configuração

### 1. **Verificar se o Django conecta ao banco**

```bash
cd clinica-de-psicologia/clinicaps
source venv/bin/activate
python manage.py check --database default
```

**Saída esperada**:
```
System check identified no issues (0 silenced).
```

### 2. **Testar migração**

```bash
python manage.py migrate
```

### 3. **Verificar SSL no PostgreSQL**

Conecte no banco:
```bash
psql -h localhost -U postgres -d clinica_db
```

Dentro do `psql`, execute:
```sql
SHOW ssl;
```

- **on** = SSL habilitado
- **off** = SSL desabilitado

---

## 🚨 Troubleshooting

### **Erro: "could not connect to server"**

**Causa**: Variáveis do `.env` não carregadas ou host/porta incorretos

**Solução**:
1. Verifique se o arquivo `.env` existe em `clinica-de-psicologia/clinicaps/`
2. Confirme que `DATABASE_HOST` e `DATABASE_PORT` estão corretos
3. Teste a conexão manualmente:

```bash
psql -h localhost -U postgres -d clinica_db
```

### **Erro: "SSL connection is required"**

**Causa**: Banco exige SSL mas `DATABASE_SSL_REQUIRE=False`

**Solução**:
```env
DATABASE_SSL_REQUIRE=True
DATABASE_SSL_MODE=require
```

### **Erro: "server does not support SSL"**

**Causa**: PostgreSQL não está configurado para SSL

**Solução**:
```env
DATABASE_SSL_REQUIRE=False
DATABASE_SSL_MODE=disable
```

---

## 📚 Referências

- [Django Database Settings](https://docs.djangoproject.com/en/5.2/ref/settings/#databases)
- [PostgreSQL SSL Support](https://www.postgresql.org/docs/current/ssl-tcp.html)
- [psycopg2 SSL Options](https://www.psycopg.org/docs/module.html#psycopg2.connect)

---

## ✨ Resumo

✅ **Desenvolvimento**: `DATABASE_SSL_REQUIRE=False` + `DATABASE_SSL_MODE=prefer`

✅ **Produção**: `DATABASE_SSL_REQUIRE=True` + `DATABASE_SSL_MODE=require`

✅ **Pool de Conexões**: `DATABASE_CONN_MAX_AGE=600` (10 minutos)

✅ **Sempre use `.env`** para variáveis sensíveis (nunca commite no Git!)
