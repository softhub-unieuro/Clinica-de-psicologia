import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
django.setup()

from contas.models import Usuario

def verificar_usuarios():
    print("\n=== VERIFICANDO USUÁRIOS ===\n")
    
    # Todos os usuários
    todos = Usuario.objects.all()
    print(f"Total de usuários: {todos.count()}\n")
    
    for user in todos:
        print(f"ID: {user.id}")
        print(f"Nome: {user.nome_completo}")
        print(f"Cargo: '{user.cargo}'")
        print(f"Email: {user.email}")
        print("-" * 40)
    
    # Especificamente Lucas
    lucas = Usuario.objects.filter(nome_completo__icontains='lucas')
    if lucas:
        print(f"\n🔍 LUCAS ENCONTRADO:")
        for l in lucas:
            print(f"  - Cargo: '{l.cargo}'")
    else:
        print("\n❌ Nenhum usuário com 'lucas' no nome")

if __name__ == "__main__":
    verificar_usuarios()