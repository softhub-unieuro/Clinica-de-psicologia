# ✅ Checklist de Deploy em Produção

> **Checklist pré-deploy: Use este documento para verificar todos os itens antes de colocar a aplicação em produção.**

---

## 📋 Fase 1: Preparação do Servidor

- [ ] Sistema operacional atualizado (`sudo apt update && sudo apt upgrade -y`)
- [ ] Python 3.13 instalado (`python3.13 --version`)
- [ ] Git instalado e configurado
- [ ] PostgreSQL 16+ instalado
- [ ] Nginx instalado
- [ ] Firewall configurado (UFW)
  - [ ] SSH (22/tcp) permitido
  - [ ] HTTP (80/tcp) permitido
  - [ ] HTTPS (443/tcp) permitido
- [ ] Usuário de aplicação criado (`clinica`)
- [ ] Diretórios de aplicação criados com permissões corretas

---

## 📋 Fase 2: Banco de Dados

- [ ] Banco de dados criado (`clinica_prod`)
- [ ] Usuário PostgreSQL criado (`clinica_user`)
- [ ] Privilégios concedidos ao usuário
- [ ] Arquivo `.env` com credenciais de BD criado
- [ ] Permissões do `.env` ajustadas (600)
- [ ] Conexão SSL/TLS configurada (opcional mas recomendado)
- [ ] Teste de conexão bem-sucedido: `psql -U clinica_user -d clinica_prod`

---

## 📋 Fase 3: Aplicação Django

- [ ] Repositório clonado em `/var/www/clinica`
- [ ] Virtual environment criado (`python3.13 -m venv venv`)
- [ ] Dependencies instaladas (`pip install -r requirements.txt`)
- [ ] Dependências de produção instaladas:
  - [ ] `gunicorn`
  - [ ] `whitenoise`
  - [ ] Outras conforme necessário
- [ ] Arquivo `.env` configurado com:
  - [ ] `DEBUG=False`
  - [ ] `SECRET_KEY` gerada e segura
  - [ ] `ALLOWED_HOSTS` com domínios corretos
  - [ ] Credenciais do BD
  - [ ] Configurações de segurança/SSL
  - [ ] Email settings (se necessário)
- [ ] Migrações executadas: `python manage.py migrate`
- [ ] Arquivos estáticos coletados: `python manage.py collectstatic --noinput`
- [ ] Superusuário criado: `python manage.py createsuperuser`
- [ ] Diretórios de logs criados com permissões corretas
- [ ] Diretórios de media e staticfiles criados com permissões corretas

---

## 📋 Fase 4: Gunicorn (Application Server)

- [ ] Arquivo de configuração Gunicorn criado (`gunicorn_config.py`)
- [ ] Workers configurados (CPU cores * 2 + 1)
- [ ] Timeout configurado apropriadamente
- [ ] Logging configurado
- [ ] Arquivo systemd service criado (`/etc/systemd/system/gunicorn_clinica.service`)
- [ ] Service ativado: `sudo systemctl enable gunicorn_clinica`
- [ ] Service iniciado: `sudo systemctl start gunicorn_clinica`
- [ ] Service rodando sem erros: `sudo systemctl status gunicorn_clinica`
- [ ] Logs verificados: `sudo journalctl -u gunicorn_clinica -n 50`

---

## 📋 Fase 5: Nginx (Reverse Proxy)

- [ ] Arquivo de configuração Nginx criado (`/etc/nginx/sites-available/clinica`)
- [ ] Virtual host vinculado: `sudo ln -s /etc/nginx/sites-available/clinica /etc/nginx/sites-enabled/clinica`
- [ ] Configuração testada: `sudo nginx -t`
- [ ] Servidor reiniciado: `sudo systemctl restart nginx`
- [ ] Headers de segurança configurados
- [ ] Proxy para Gunicorn configurado corretamente
- [ ] Static files servidos por Nginx
- [ ] Media files servidos por Nginx
- [ ] Client max body size ajustado (10M)
- [ ] Access logs configurados
- [ ] Error logs configurados

---

## 📋 Fase 6: SSL/TLS (HTTPS)

- [ ] Certbot instalado
- [ ] Domínio registrado e apontando para o servidor
- [ ] DNS resolvendo corretamente
- [ ] Certificado Let's Encrypt obtido: `sudo certbot certonly --nginx -d seudominio.com`
- [ ] Certificado em: `/etc/letsencrypt/live/seudominio.com/`
- [ ] Nginx configurado para usar certificado
- [ ] Redirecionamento HTTP → HTTPS funcionando
- [ ] HSTS headers configurado
- [ ] Renovação automática ativada: `sudo systemctl enable certbot.timer`
- [ ] Teste de renovação: `sudo certbot renew --dry-run`
- [ ] HTTPS funciona sem erros

---

## 📋 Fase 7: Segurança

- [ ] `DEBUG=False` no `.env` e settings.py
- [ ] `SECRET_KEY` forte e única gerada
- [ ] `ALLOWED_HOSTS` configurado corretamente
- [ ] CSRF protection ativado
- [ ] SQL injection mitigation verificado
- [ ] XSS protection headers ativados
- [ ] Clickjacking protection ativado (`X-Frame-Options: DENY`)
- [ ] Content Security Policy considerer
- [ ] SQL queries otimizadas para N+1 queries
- [ ] Rate limiting considerado
- [ ] CORS configurado se necessário
- [ ] Senhas de usuários hasheadas (Django padrão)
- [ ] Upload de arquivos validado e limitado (10MB)
- [ ] Arquivo `.env` tem permissões 600
- [ ] Media files não são publicamente acessíveis sem autenticação

---

## 📋 Fase 8: Performance e Otimização

- [ ] Gunicorn workers ajustados para CPU cores
- [ ] Conexões de BD em pool (`CONN_MAX_AGE=600`)
- [ ] Cache configurado (se necessário)
- [ ] Static files comprimidos (Gzip no Nginx)
- [ ] Database indexes criados
- [ ] Slow query log analisado
- [ ] Static files com versioning para cache busting
- [ ] Imagens otimizadas
- [ ] CDN considerado (opcional)

---

## 📋 Fase 9: Monitoramento e Logging

- [ ] Logging configurado no Django (INFO level)
- [ ] Rotação de logs configurada (`/etc/logrotate.d/clinica`)
- [ ] Health check script criado e agendado
- [ ] Alertas configurados (opcional)
- [ ] Crontab para health checks ativo
- [ ] Monitoramento de recursos (CPU, memória, disco)
- [ ] Ferramentas de diagnóstico instaladas (htop, iotop)

---

## 📋 Fase 10: Backups

- [ ] Script de backup de BD criado
- [ ] Script de backup de arquivos criado
- [ ] Backups agendados no crontab
  - [ ] BD: diariamente às 2 da manhã
  - [ ] Arquivos: semanalmente aos domingos
- [ ] Diretório de backups criado (`/var/backups/clinica/`)
- [ ] Permissões dos backups ajustadas
- [ ] Retenção de backups configurada (30 dias)
- [ ] Teste de restauração de backup realizado
- [ ] Armazenamento remoto considerado (AWS S3, Google Cloud, etc.)

---

## 📋 Fase 11: Testes Pré-Deploy

### Testes Funcionais
- [ ] Inscrição pública funciona
- [ ] Login de usuários funciona
- [ ] CRUD de usuários funciona
- [ ] Dashboard do coordenador funciona
- [ ] Dashboard do estagiário funciona
- [ ] Dashboard do supervisor funciona
- [ ] Dashboard da RT funciona
- [ ] Prontuários funciona
- [ ] Upload de arquivos funciona (< 10MB)
- [ ] Download de PDF funciona
- [ ] Relatórios funciona

### Testes de Segurança
- [ ] HTTPS forçado (redireciona de HTTP)
- [ ] SSL A+ rating (testado em https://www.ssllabs.com/ssltest/)
- [ ] Admin painel protegido
- [ ] Sem exposure de dados sensíveis em logs
- [ ] Senhas criptografadas (teste no banco)
- [ ] CSRF protection ativo
- [ ] XSS prevention testado
- [ ] SQL injection prevenido

### Testes de Performance
- [ ] Pagina carrega em < 2 segundos
- [ ] Database queries otimizadas
- [ ] Sem memory leaks (rodar stress test)
- [ ] Upload de arquivo > 10MB rejeitado
- [ ] Concurrent users testados (mínimo 50)

### Testes de Compatibilidade
- [ ] Chrome/Edge funciona
- [ ] Firefox funciona
- [ ] Safari funciona
- [ ] Mobile responsivo funciona
- [ ] Dark mode (se implementado) funciona

---

## 📋 Fase 12: Documentação e Handoff

- [ ] Documentação de deploy completa
- [ ] Documentação de troubleshooting criada
- [ ] Senhas e credenciais armazenadas em local seguro (Bitwarden/LastPass)
- [ ] Escalation contacts documentados
- [ ] Processo de rollback documentado
- [ ] Changelog atualizado
- [ ] Runbook para emergências criado
- [ ] Team treinado no novo ambiente

---

## 🚀 Deploy Final

### Pré-Deploy (24 horas antes)
- [ ] Backup completo do ambiente anterior
- [ ] Equipe de suporte em alerta
- [ ] Plano de rollback testado
- [ ] Mensagem de manutenção preparada (se necessário)

### Dia do Deploy
- [ ] Todos os testes passando ✅
- [ ] Equipe disponível
- [ ] Comunicação de status ativa
- [ ] Monitoramento ativo

### Deploy Steps
- [ ] Pausar cron jobs (se houver)
- [ ] Backup final de BD e arquivos
- [ ] Pull do código mais recente
- [ ] Rodar migrações
- [ ] Coletar static files
- [ ] Reiniciar Gunicorn
- [ ] Verificar status
- [ ] Testar funcionalidades críticas
- [ ] Monitorar por 30+ minutos

### Pós-Deploy
- [ ] Verificar logs por erros
- [ ] Verificar uptime/health checks
- [ ] Testar casos de uso críticos
- [ ] Comunicar sucesso ao time
- [ ] Documentar tempo de downtime (se houver)
- [ ] Atualizar runbooks com lições aprendidas

---

## 🆘 Rollback Plan

Se algo der errado durante o deploy:

1. [ ] Restaurar código anterior
2. [ ] Restaurar banco de dados anterior
3. [ ] Reiniciar serviços
4. [ ] Verificar funcionalidade
5. [ ] Investigar root cause
6. [ ] Aprender e corrigir
7. [ ] Tentar deploy novamente depois

---

## 📞 Contatos de Emergência

| Cargo | Nome | Telefone | Email |
|-------|------|----------|-------|
| DevOps Lead | | | |
| Backup DevOps | | | |
| DB Admin | | | |
| Security | | | |

---

**Impressionante! Você está pronto para produção! 🎉**

Lembre-se: **Um bom planejamento evita 10 emergências.**

---

*Data do checklist: ___/___/_____*  
*Responsável pelo deploy: ________________*  
*Aprovação: ________________*
