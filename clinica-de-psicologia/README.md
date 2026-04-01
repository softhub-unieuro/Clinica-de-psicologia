# Clínica de Psicologia

Sistema web para gestão de inscrições em clínica psicológica, desenvolvido com Django.

## 🚀 Como Executar

### Pré-requisitos
- Python 3.13+
- PostgreSQL 12+
- Git

### Instalação e Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/devops-softhub/clinica-de-psicologia.git
   cd clinica-de-psicologia/clinica-de-psicologia
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco PostgreSQL**:
   ```sql
   CREATE DATABASE clinica_psicologia;
   CREATE USER postgres WITH PASSWORD 'sua_senha';
   GRANT ALL PRIVILEGES ON DATABASE clinica_psicologia TO postgres;
   ```

5. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite o .env com suas configurações
   ```

6. **Execute as migrações**:
   ```bash
   python clinicaps/manage.py makemigrations
   python clinicaps/manage.py migrate
   ```

7. **Crie um superusuário**:
   ```bash
   python clinicaps/manage.py createsuperuser
   ```

8. **Popule o banco (opcional)**:
   ```bash
   python seed_users.py
   python seed_inscritos.py
   ```

9. **Execute o servidor**:
   ```bash
   python clinicaps/manage.py runserver
   ```

10. **Acesse a aplicação**:
    - Página inicial: http://127.0.0.1:8000
    - Admin: http://127.0.0.1:8000/admin
    - Formulários: http://127.0.0.1:8000/formulario/

## 📁 Estrutura do Projeto

```
clinica-de-psicologia/
├── clinicaps/                 # Configurações principais
│   ├── clinicaps/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── formulario/           # App de formulários
│   ├── usuarios/             # App de usuários (em desenvolvimento)
│   └── templates/            # Templates HTML
├── requirements.txt          # Dependências Python
├── .env.example             # Exemplo de variáveis de ambiente
├── seed_users.py            # Script para popular usuários
├── seed_inscritos.py        # Script para popular inscritos
└── ROTEIRO_VIDEO_AMBIENTE_TESTES.md  # Guia para configuração
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2
- **Banco de Dados**: PostgreSQL
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Validação**: Validate-docbr

## 📋 Funcionalidades

- ✅ Inscrição na comunidade terapêutica
- ✅ Inscrição por convênio médico
- ✅ Validação de CPF e dados brasileiros
- ✅ Interface administrativa
- ✅ Sistema de autenticação

## 🔧 Comandos Úteis

```bash
# Verificar configurações
python clinicaps/manage.py check

# Executar testes
python clinicaps/manage.py test

# Criar novas migrações
python clinicaps/manage.py makemigrations

# Aplicar migrações
python clinicaps/manage.py migrate

# Coletar arquivos estáticos
python clinicaps/manage.py collectstatic
```

## 🚨 Solução de Problemas

### Erro de Conexão com Banco
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`

### Porta Já em Uso
```bash
python clinicaps/manage.py runserver 8001
```

### Dependências Não Instaladas
```bash
pip install -r requirements.txt
```

## 📖 Documentação Adicional

- [Documentação Django](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.