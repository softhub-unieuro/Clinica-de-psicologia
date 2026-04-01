import os
import sys
import django
from datetime import date

# Adicionar o diretório clinicaps ao path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clinicaps'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinicaps.settings')
django.setup()

from formulario.models import Inscritocomunidade, Inscritoconvenio, Endereco, Disponibilidade, Doencafisica

def seed_inscritos():
    # Criar inscritos na comunidade
    comunidade_data = [
        {
            'nomeinscrito': 'João Silva',
            'dtnascimento': date(1990, 5, 15),
            'nomeresp': 'Maria Silva',
            'grauresp': 'Mãe',
            'cpfresp': '123.456.789-00',
            'estadocivilresp': 'Casado',
            'tellcellresp': '61 99999-0001',
            'emailresp': 'maria@example.com',
            'estadocivilinscrito': 'Solteiro',
            'cpfinscrito': '987.654.321-00',
            'tellcellinscrito': '61 99999-0002',
            'contatourgencia': '61 99999-0003',
            'nomecontatourgencia': 'Pedro Silva',
            'emailinscrito': 'joao@example.com',
            'identidadegenero': 'Masculino',
            'etnia': 'Branca',
            'religiao': 'Católico',
            'confirmlgpd': True,
        },
        {
            'nomeinscrito': 'Ana Santos',
            'dtnascimento': date(1985, 8, 20),
            'estadocivilinscrito': 'Casado',
            'cpfinscrito': '111.222.333-44',
            'tellcellinscrito': '61 99999-0004',
            'contatourgencia': '61 99999-0005',
            'nomecontatourgencia': 'Carlos Santos',
            'emailinscrito': 'ana@example.com',
            'identidadegenero': 'Feminino',
            'etnia': 'Parda',
            'religiao': 'Evangélico',
            'confirmlgpd': True,
        },
    ]

    for data in comunidade_data:
        inscrito, created = Inscritocomunidade.objects.get_or_create(
            cpfinscrito=data['cpfinscrito'],
            defaults=data
        )
        if created:
            print(f"Inscrito comunidade {inscrito.nomeinscrito} criado.")
        else:
            print(f"Inscrito comunidade {inscrito.nomeinscrito} já existe.")

    # Criar inscritos por convênio
    convenio_data = [
        {
            'nomeinscrito': 'Carlos Oliveira',
            'dtnascimento': date(1975, 3, 10),
            'testavpsico': True,
            'tipoencaminhamento': 'Médico',
            'cpfinscrito': '555.666.777-88',
            'tellcellinscrito': '61 99999-0006',
            'emailinscrito': 'carlos@example.com',
        },
        {
            'nomeinscrito': 'Fernanda Lima',
            'dtnascimento': date(1980, 12, 5),
            'testavpsico': False,
            'tipoencaminhamento': 'Psicólogo',
            'cpfinscrito': '999.888.777-66',
            'tellcellinscrito': '61 99999-0007',
            'emailinscrito': 'fernanda@example.com',
        },
    ]

    for data in convenio_data:
        inscrito, created = Inscritoconvenio.objects.get_or_create(
            cpfinscrito=data['cpfinscrito'],
            defaults=data
        )
        if created:
            print(f"Inscrito convênio {inscrito.nomeinscrito} criado.")
        else:
            print(f"Inscrito convênio {inscrito.nomeinscrito} já existe.")

if __name__ == '__main__':
    seed_inscritos()
    print("Seed de inscritos concluído!")