from django.test import TestCase, Client
from django.urls import reverse
from django.test.utils import CaptureQueriesContext
from django.db import connection
from usuarios.models import Usuario
from formulario.models import Inscritocomunidade, Inscritoconvenio, Tipoterapia
from coodernador.models import Prontuario
from datetime import date

class ConsultaInscritosPerfTest(TestCase):
    def setUp(self):
        # Create user
        self.user = Usuario.objects.create_user(
            matricula='12345',
            email='estag@teste.com',
            nome_completo='Estagiario Teste',
            password='123',
            cargo='ESTAG'
        )
        self.client = Client()
        self.client.force_login(self.user)

        # Create many inscritos
        # Comunidade: 60 items (should be 2 pages: 50 + 10)
        for i in range(60):
            p = Inscritocomunidade.objects.create(
                nomeinscrito=f'Comunidade {i}',
                dtnascimento=date(2000, 1, 1),
                cpfinscrito=f'111{i}',
                tellcellinscrito='999',
                contatourgencia='888',
                nomecontatourgencia='Mae',
                emailinscrito=f'c{i}@teste.com',
                identidadegenero='Masculino',
                etnia='Parda',
                religiao='Nenhuma'
            )
            # Add therapy type to test prefetch
            Tipoterapia.objects.create(idfichacomunidade=p, individualadt=True)

        # Convenio: 60 items
        for i in range(60):
            p = Inscritoconvenio.objects.create(
                nomeinscrito=f'Convenio {i}',
                dtnascimento=date(2000, 1, 1),
                cpfinscrito=f'222{i}',
                tellcellinscrito='999',
                contatourgencia='888',
                emailinscrito=f'cv{i}@teste.com',
                identidadegenero='Feminino',
                etnia='Branca',
                religiao='Catolica',
                confirmlgpd=True
            )
            Tipoterapia.objects.create(idfichaconvenio=p, individualift=True)

    def test_pagination_and_queries(self):
        url = reverse('estagiario:consulta_inscritos')
        
        # Use CaptureQueriesContext to check for N+1
        # Expected queries:
        # 1. Session/User
        # 2. Prontuarios (select_related + prefetch_related -> 1 query for main + 2 for prefetch = 3)
        # 3. Exclude IDs (2 queries)
        # 4. Count Comunidade
        # 5. Fetch Comunidade Page (1 query)
        # 6. Prefetch Tipoterapia Comunidade (1 query)
        # 7. Count Convenio
        # 8. Fetch Convenio Page (1 query)
        # 9. Prefetch Tipoterapia Convenio (1 query)
        # Total around 10-12 queries, NOT 60+
        
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(url)
        
        num_queries = len(ctx)
        # Allow some buffer for middleware/auth queries
        self.assertTrue(8 <= num_queries <= 18, f"Expected 8-18 queries, got {num_queries}")
        
        self.assertEqual(response.status_code, 200)
        
        # Check context
        self.assertIn('lista_comunidade', response.context)
        self.assertIn('lista_convenio', response.context)
        
        # Check pagination size (should be 50)
        self.assertEqual(len(response.context['lista_comunidade']), 50)
        self.assertEqual(len(response.context['lista_convenio']), 50)
        
        # Check page 2
        response = self.client.get(url, {'page_comunidade': 2, 'page_convenio': 2})
        self.assertEqual(len(response.context['lista_comunidade']), 10)
        self.assertEqual(len(response.context['lista_convenio']), 10)
