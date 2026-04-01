# ============================================================
# Dockerfile — Clínica de Psicologia (softhub-unieuro)
# Imagem base leve com Python 3.13
# ============================================================

FROM python:3.13-slim

# Evita prompts interativos durante instalação de pacotes
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências de sistema para compilar psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências Python primeiro (aproveita cache do Docker)
COPY clinica-de-psicologia/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o código da aplicação
COPY clinica-de-psicologia/clinicaps/ .

# Copia e configura o script de inicialização
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Porta que o Gunicorn vai expor
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
