import os
import django
import random
from datetime import date

# Configurar Django antes de usar models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinicaps.settings')
django.setup()

from formulario.models import Inscritocomunidade, Inscritoconvenio, Tipoterapia

def generate_cpf():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

def seed_inscritos():
    print("--- Inserindo Inscritos Comunidade ---")
    for i in range(10):
        try:
            inscrito = Inscritocomunidade.objects.create(
                nomeinscrito=f'Inscrito Comunidade {i+1}',
                dtnascimento=date(1990 + i, 1, 1),
                cpfinscrito=generate_cpf(),
                tellcellinscrito=f'619{random.randint(10000000, 99999999)}',
                contatourgencia='99999999',
                nomecontatourgencia='Contato Urgencia',
                emailinscrito=f'comunidade{i+1}@teste.com',
                identidadegenero='Masculino' if i % 2 == 0 else 'Feminino',
                etnia='Parda',
                religiao='Nenhuma',
                estadocivilinscrito='Solteiro',
                confirmlgpd=True
            )
            
            # Criar Tipo Terapia
            Tipoterapia.objects.create(
                idfichacomunidade=inscrito,
                individualadt=True, # Adulto
                individualift=False
            )
            print(f"Criado: {inscrito.nomeinscrito}")
        except Exception as e:
            print(f"Erro ao criar comunidade {i}: {e}")

    print("\n--- Inserindo Inscritos Convênio ---")
    for i in range(10):
        try:
            inscrito = Inscritoconvenio.objects.create(
                nomeinscrito=f'Inscrito Convenio {i+1}',
                dtnascimento=date(1985 + i, 5, 10),
                cpfinscrito=generate_cpf(),
                tellcellinscrito=f'619{random.randint(10000000, 99999999)}',
                contatourgencia='88888888',
                emailinscrito=f'convenio{i+1}@teste.com',
                identidadegenero='Feminino' if i % 2 == 0 else 'Masculino',
                etnia='Branca',
                religiao='Catolica',
                confirmlgpd=True,
                tipoencaminhamento='Médico',
                testavpsico=False
            )
            
            # Criar Tipo Terapia
            Tipoterapia.objects.create(
                idfichaconvenio=inscrito,
                individualift=True, # Infantil
                individualadt=False
            )
            print(f"Criado: {inscrito.nomeinscrito}")
        except Exception as e:
            print(f"Erro ao criar convenio {i}: {e}")

if __name__ == '__main__':
    seed_inscritos()

seed_inscritos()
