#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/clinica-de-psicologia/.env"

log_info() { echo "ℹ️  $1"; }
log_success() { echo "✅ $1"; }
log_error() { echo "❌ $1" >&2; exit 1; }

log_info "🔍 Validando dependências..."
command -v docker &> /dev/null || log_error "Docker não encontrado"
command -v docker-compose &> /dev/null || log_error "Docker Compose não encontrado"
log_success "Dependências OK"

log_info ""
log_info "🐳 Iniciando Docker Compose..."
cd "$PROJECT_ROOT"
docker-compose up --build -d

log_info "⏳ Aguardando PostgreSQL..."
for i in {1..30}; do
    docker-compose exec -T db pg_isready &> /dev/null && break
    [ $i -eq 30 ] && log_error "PostgreSQL não respondeu"
    sleep 2
done
log_success "PostgreSQL pronto"

log_info "📊 Executando migrações..."
docker-compose exec -T web python manage.py migrate --noinput
log_success "Migrações OK"

log_info "👥 Seed de usuários..."
docker-compose exec -T web python seed_users.py || log_info "⚠️ Seed users concluído com avisos"

log_info "📝 Seed de inscritos..."
docker-compose exec -T web python seed_inscritos.py || log_info "⚠️ Seed inscritos concluído com avisos"

log_info ""
log_success "🎉 Ambiente pronto!"
log_info "📌 Django: http://localhost:8000"
log_info "📌 PostgreSQL: localhost:5432"