import os
import sys
import django

# Adicionar o diretório clinicaps ao path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clinicaps'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinicaps.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def seed_users():
    # Criar usuários de teste
    users_data = [
        {'matricula': 'admin', 'nome_completo': 'Administrador', 'cpf': '00000000191', 'email': 'admin@example.com', 'password': 'admin123', 'is_superuser': True, 'is_staff': True},
        {'matricula': 'user1', 'nome_completo': 'Usuario Um', 'cpf': '00000000202', 'email': 'user1@example.com', 'password': 'user123', 'is_superuser': False, 'is_staff': False},
        {'matricula': 'user2', 'nome_completo': 'Usuario Dois', 'cpf': '00000000303', 'email': 'user2@example.com', 'password': 'user123', 'is_superuser': False, 'is_staff': False},
    ]

    for user_data in users_data:
        user, created = User.objects.get_or_create(
            matricula=user_data['matricula'],
            defaults={
                'nome_completo': user_data['nome_completo'],
                'cpf': user_data['cpf'],
                'email': user_data['email'],
                'is_superuser': user_data['is_superuser'],
                'is_staff': user_data['is_staff'],
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Usuário {user.matricula} criado.")
        else:
            print(f"Usuário {user.matricula} já existe.")

if __name__ == '__main__':
    seed_users()
    print("Seed de usuários concluído!")