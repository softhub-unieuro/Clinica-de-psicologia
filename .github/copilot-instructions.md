# GitHub Copilot Instructions for `clinica-de-psicologia`

You are an expert Django developer working on the `clinica-de-psicologia` project. This is a monolithic Django application for managing a psychology clinic, handling user roles, patient forms, and dashboards.

## 🏗 Project Architecture & Structure

- **Framework**: Django 5.x (Python).
- **Database**: PostgreSQL (running in Docker/Codespaces).
- **Key Apps**:
  - `clinicaps`: Project configuration (`settings.py`, `urls.py`).
  - `usuarios`: Custom authentication and user management.
  - `formulario`: Patient intake forms, health data, and availability.
  - `daashboard`: Reporting and visualization (currently in development).
- **Frontend**: Django Templates (`.html`) served by views. There is a `front/` directory with static mockups, but the active templates are within the apps or the root `templates/` folder.

## 🔐 Authentication & User Model

- **Custom User Model**: The project uses a custom user model `usuarios.Usuario`.
- **Identifier**: Users authenticate using `matricula` (Student/Employee ID), NOT `username` or `email`.
- **Roles**: Roles are defined in `Usuario.CARGOS_CHOICES` (e.g., `COORD`, `SUPER`, `ESTAG`, `SEC`).
- **Permissions**: Use standard Django permissions mixins (`PermissionsMixin`) but rely on the `cargo` field for role-based logic.

## 🗄 Database & Models

- **Legacy/Specific Schema**: The `formulario` app uses `managed = True` with explicit `db_table` names (e.g., `db_table = 'disponibilidade'`). Respect these table names when creating or modifying models in this app.
- **Foreign Keys**: Note the use of `db_column` in `ForeignKey` definitions to match specific schema requirements.

## 💻 Development Workflow

- **Environment**: The project runs in GitHub Codespaces with a Dockerized PostgreSQL database.
- **Configuration**: Environment variables are loaded from `.env` using `python-dotenv`.
- **Running the Server**: `python manage.py runserver`
- **Migrations**: Always check for model changes with `python manage.py makemigrations` and apply with `python manage.py migrate`.

## 🎨 Frontend & UI

- **Styling**: The project uses Bootstrap classes (e.g., `form-control`, `form-select`) directly in Django Forms widgets (`forms.py`).
- **Forms**: When creating forms, ensure widgets have the appropriate Bootstrap classes for consistent styling.
- **Templates**: Base template is likely `templates/base.html`. Extend this for new pages.

## 📝 Coding Conventions

- **Language**: Code comments and documentation should be in **Portuguese (pt-br)**.
- **Form Validation**: Implement complex validation in the `clean()` method of forms or models.
- **Type Hinting**: Use Python type hints where possible for better clarity.

# Contexto do Projeto: Sistema de Gestão para Clínica de Psicologia (Unieuro)

Estou desenvolvendo um sistema para automação de atendimentos clínicos. Abaixo estão as regras de negócio, stack tecnológica e funcionalidades prioritárias extraídas da documentação oficial. Use isso como base para gerar código e lógica.

## 1. Stack Tecnológica
- [cite_start]**Back-end:** Python 3.13.
- [cite_start]**Banco de Dados:** PostgreSQL.
- [cite_start]**Front-end:** HTML, CSS, JavaScript, Bootstrap.
- [cite_start]**Segurança:** Senhas criptografadas (hash), não armazenadas em texto plano[cite: 66].

## 2. Atores e Permissões (Role-Based Access Control)
O sistema possui hierarquia estrita de visualização e ações:
1.  **Coordenador:** "Super Admin". [cite_start]Pode ver, criar, editar e excluir todos os usuários do sistema (Supervisores, Responsáveis Técnicas, Estagiários, Secretárias)[cite: 35, 36, 37, 61, 397].
2.  [cite_start]**Responsável Técnica (RT):** Visualiza **todos** os Inscritos (com ou sem estagiário vinculado), pacientes, ocorrências e gera relatórios institucionais[cite: 379, 395].
3.  **Supervisor:** Visualiza Estagiários e Pacientes/Inscritos sob supervisão. [cite_start]Valida arquivamentos e documentos[cite: 361].
4.  [cite_start]**Estagiário:** Visualiza inscritos disponíveis, "adota" inscritos, gerencia prontuários e agenda salas[cite: 253, 315].
5.  [cite_start]**Inscrito/Comunidade:** Acesso apenas ao formulário público de inscrição (sem login)[cite: 28, 67].

## 3. Funcionalidades Prioritárias para Implementação

### A. Módulo de Inscrição (Formulários Públicos)
[cite_start]Deve haver 3 tipos de formulários de inscrição distintos, com validação de campos obrigatórios[cite: 28, 29, 30]:
1.  [cite_start]**Inscrição Comunidade:** Dados pessoais completos, endereço, responsável legal (se menor de idade), tipos de terapia, contato de urgência [cite: 67-117].
2.  [cite_start]**Inscrição Convênio:** Similar ao anterior, mas focado em parcerias[cite: 118].
3.  [cite_start]**Inscrição Testes Psicológicos:** Focado apenas em avaliação[cite: 185].
*Regra:* O sistema deve calcular a idade automaticamente. [cite_start]Se menor de 18, exigir dados do responsável[cite: 68].

### B. CRUD de Usuários (Back-office)
- O **Coordenador** deve ter telas para criar contas de Estagiários, Supervisores e RTs.
- [cite_start]Login deve ser via CPF ou RA (para estagiários) e Senha[cite: 65].

### C. Fluxo de Vinculação (Estagiário -> Inscrito -> Paciente)
Esta é a funcionalidade central. O fluxo deve ser:
1.  [cite_start]**Listagem:** O Estagiário visualiza uma lista de "Inscritos Disponíveis"[cite: 32, 253].
2.  **Seleção:** O Estagiário seleciona um inscrito para iniciar o atendimento.
3.  **Vinculação e Conversão:**
    - O sistema deve permitir anexar o **TCLE (Termo de Consentimento)** assinado.
    - [cite_start]Ao confirmar e anexar o TCLE, o sistema deve converter o "Inscrito" automaticamente em "Paciente", criando o Prontuário.
4.  [cite_start]**Geração de PDF:** O estagiário deve ter um botão para gerar um arquivo PDF contendo todos os dados preenchidos na ficha de inscrição daquele inscrito/paciente.

### D. Dashboards de Visualização (Regras de Filtro)
- **View do Estagiário:** Vê apenas seus pacientes vinculados e a lista geral de disponíveis.
- **View do Supervisor:** Vê a lista de estagiários e os pacientes vinculados a eles.
- [cite_start]**View da Responsável Técnica:** Deve ter uma tabela geral de Inscritos com filtros: "Aguardando Triagem", "Em Atendimento" (com estagiário) e "Sem Estagiário"[cite: 380].
- **View do Coordenador:** Acesso total à lista de usuários internos.

## 4. Requisitos de Dados Específicos
- [cite_start]Endereços devem ser estruturados (Rua, Bairro, Cidade-DF, CEP)[cite: 69].
- [cite_start]Prontuários devem permitir upload de arquivos (PDF/DOCX/Imagem) até 10MB[cite: 261].