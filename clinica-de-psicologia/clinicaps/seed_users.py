import os
import django

# Configurar Django antes de usar models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinicaps.settings')
django.setup()

from usuarios.models import Usuario
from django.db import IntegrityError

users_data = [
    {
        'matricula': 'COORD999',
        'nome_completo': 'Coordenador Geral',
        'email': 'coord@clinica.com',
        'cpf': '000.000.000-01',
        'cargo': 'COORD',
        'password': '123',
        'telefone': '61999999999'
    },
    {
        'matricula': 'RESP999',
        'nome_completo': 'Responsável Técnica',
        'email': 'resp@clinica.com',
        'cpf': '000.000.000-02',
        'cargo': 'RESP_TEC',
        'password': '123',
        'telefone': '61999999999',
        'crp': '12345/DF'
    },
    {
        'matricula': 'SUPER999',
        'nome_completo': 'Supervisor Docente',
        'email': 'super@clinica.com',
        'cpf': '000.000.000-03',
        'cargo': 'SUPER',
        'password': '123',
        'telefone': '61999999999',
        'crp': '67890/DF'
    },
    {
        'matricula': 'SEC999',
        'nome_completo': 'Secretária Atendimento',
        'email': 'sec@clinica.com',
        'cpf': '000.000.000-04',
        'cargo': 'SEC',
        'password': '123',
        'telefone': '61999999999'
    },
    {
        'matricula': 'ESTAG999',
        'nome_completo': 'Estagiário Aluno',
        'email': 'estag@clinica.com',
        'cpf': '000.000.000-05',
        'cargo': 'ESTAG',
        'password': '123',
        'telefone': '61999999999',
        'semestre': '9',
        'nivel_estagio': 'AVANCADO'
    }
]

created_users = {}

print("--- Criando Usuários ---")
for data in users_data:
    try:
        # Check if exists
        if Usuario.objects.filter(matricula=data['matricula']).exists():
            print(f"Usuário {data['matricula']} já existe. Atualizando senha...")
            user = Usuario.objects.get(matricula=data['matricula'])
            user.set_password(data['password'])
            user.save()
            created_users[data['cargo']] = user
        else:
            user = Usuario.objects.create_user(**data)
            print(f"Usuário {data['matricula']} criado com sucesso.")
            created_users[data['cargo']] = user
    except Exception as e:
        print(f"Erro ao criar {data['matricula']}: {e}")

# Vincular Estagiário ao Supervisor
if 'ESTAG' in created_users and 'SUPER' in created_users:
    estag = created_users['ESTAG']
    supervisor = created_users['SUPER']
    estag.supervisor_vinculado = supervisor
    estag.save()
    print(f"VÍNCULO: {estag.nome_completo} vinculado ao supervisor {supervisor.nome_completo}")

print("\n--- Credenciais de Acesso ---")
for data in users_data:
    print(f"Cargo: {data['cargo']:<10} | Login (RA): {data['matricula']:<10} | Senha: {data['password']}")
