#!/usr/bin/env bash
# ============================================================
# subir.sh — Clínica de Psicologia
# Script principal para subir o ambiente com docker-compose
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${SCRIPT_DIR}/ops/subir_ambiente.sh"
