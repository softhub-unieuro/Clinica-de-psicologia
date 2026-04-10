#!/bin/bash
# ============================================================
# entrypoint.sh — Clínica de Psicologia
# Automação para setup inicial: migrate → seeds → runserver
# ============================================================

set -e

echo "=========================================="
echo "🚀 Iniciando Clínica de Psicologia"
echo "=========================================="

# Aguardar pelo menos 5 segundos para PostgreSQL inicializar
echo ""
echo "⏳ Aguardando PostgreSQL ficar pronto..."
sleep 5

# ============================================================
# 1. EXECUTAR MIGRAÇÕES DJANGO
# ============================================================
echo ""
echo "📊 Executando migrações do Django..."
python manage.py migrate --noinput

if [ $? -eq 0 ]; then
    echo "✅ Migrações aplicadas com sucesso!"
else
    echo "⚠️  Aviso: Possível erro ao aplicar migrações"
fi

# ============================================================
# 2. SEED USUÁRIOS
# ============================================================
echo ""
echo "👥 Populando usuários iniciais..."
python seed_users.py 2>&1 || echo "⚠️  Usuários já existem ou erro"

# ============================================================
# 3. SEED INSCRITOS
# ============================================================
echo ""
echo "📝 Populando inscritos iniciais..."
python seed_inscritos.py 2>&1 || echo "⚠️  Inscritos já existem ou erro"

# ============================================================
# 4. INICIAR SERVIDOR DJANGO
# ============================================================
echo ""
echo "=========================================="
echo "🎯 Iniciando servidor Django"
echo "=========================================="
echo "📌 Servidor disponível em: http://0.0.0.0:8000"
echo ""

exec python manage.py runserver 0.0.0.0:8000
