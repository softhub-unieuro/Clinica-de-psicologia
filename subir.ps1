# Clinica de Psicologia - Automacao de Ambiente

$ErrorActionPreference = "Stop"

$projectRoot = (Get-Item $PSScriptRoot).FullName
$envFile = "$projectRoot\clinica-de-psicologia\clinicaps\.env"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Clinica de Psicologia - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Validar dependencias
Write-Host "[1/7] Verificando dependencias..." -ForegroundColor Yellow
foreach ($cmd in @("docker", "docker-compose", "python")) {
    try {
        $null = & $cmd --version 2>$null
        Write-Host "  [OK] $cmd" -ForegroundColor Green
    } catch {
        Write-Host "  [ERRO] $cmd nao encontrado" -ForegroundColor Red
        exit 1
    }
}

# 2. Validar .env
Write-Host "[2/7] Validando .env..." -ForegroundColor Yellow
if (!(Test-Path $envFile)) {
    Write-Host "  [ERRO] Arquivo nao encontrado: $envFile" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Arquivo encontrado" -ForegroundColor Green

# 3. Docker Compose UP
Write-Host "[3/7] Iniciando containers Docker..." -ForegroundColor Yellow
Set-Location $projectRoot
& docker-compose up --build -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERRO] Falha ao iniciar containers" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Containers iniciados" -ForegroundColor Green

# 4. Aguardar PostgreSQL
Write-Host "[4/7] Aguardando PostgreSQL..." -ForegroundColor Yellow
$attempts = 0
$maxAttempts = 30
while ($attempts -lt $maxAttempts) {
    try {
        $result = & docker-compose exec -T db pg_isready 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] PostgreSQL pronto" -ForegroundColor Green
            break
        }
    } catch { }
    
    $attempts++
    if ($attempts -eq $maxAttempts) {
        Write-Host "  [ERRO] PostgreSQL nao respondeu" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  [Tentativa $attempts/$maxAttempts] Aguardando..."
    Start-Sleep -Seconds 2
}

# 5. Migrate
Write-Host "[5/7] Executando migrate..." -ForegroundColor Yellow
& docker-compose exec -T web python manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERRO] Falha no migrate" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Migrancoes aplicadas" -ForegroundColor Green

# 6. Seed Usuarios
Write-Host "[6/7] Executando seed de usuarios..." -ForegroundColor Yellow
& docker-compose exec -T web python seed_users.py
Write-Host "  [OK] Seed usuarios concluido" -ForegroundColor Green

# 7. Seed Inscritos
Write-Host "[7/7] Executando seed de inscritos..." -ForegroundColor Yellow
& docker-compose exec -T web python seed_inscritos.py
Write-Host "  [OK] Seed inscritos concluido" -ForegroundColor Green

# Conclusao
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "AMBIENTE PRONTO !" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Servicos disponveis:" -ForegroundColor Yellow
Write-Host "  - Django:     http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - PostgreSQL: localhost:5432" -ForegroundColor Cyan
Write-Host ""
Write-Host "Comandos uteis:" -ForegroundColor Yellow
Write-Host "  - docker-compose logs -f" -ForegroundColor Cyan
Write-Host "  - docker-compose down" -ForegroundColor Cyan
Write-Host "  - docker-compose restart" -ForegroundColor Cyan
Write-Host ""