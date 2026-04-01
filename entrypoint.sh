#!/bin/sh
# ============================================================
# entrypoint.sh — Script de inicialização do container web
# Executado automaticamente antes do Gunicorn iniciar
# ============================================================

set -e

echo "⏳ Aguardando banco de dados ficar pronto..."
# Pequena espera extra como garantia (o healthcheck do compose já cuida disso)
sleep 2

echo "🔄 Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Inicialização concluída. Iniciando Gunicorn..."
exec gunicorn clinicaps.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
