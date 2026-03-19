"""
Management command para anonimização de dados de acordo com a LGPD.
Este comando deve ser executado periodicamente para anonimizar dados de pacientes inativos.

Uso: python manage.py anonimizar_dados_inativos --dias=365
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from formulario.models import Inscritocomunidade, Inscritoconvenio
from coodernador.models import Prontuario
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Anonimiza dados pessoais de inscritos inativos conforme LGPD (após X dias sem atividade)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=1095,  # 3 anos (padrão LGPD para dados de saúde)
            help='Número de dias de inatividade antes da anonimização (padrão: 1095 = 3 anos)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem fazer alterações, apenas mostra o que seria anonimizado'
        )

    def handle(self, *args, **options):
        dias = options['dias']
        dry_run = options['dry_run']
        data_limite = timezone.now().date() - timedelta(days=dias)

        self.stdout.write(
            self.style.WARNING(
                f"\n{'=' * 60}\n"
                f"ANONIMIZAÇÃO DE DADOS (LGPD)\n"
                f"{'=' * 60}\n"
                f"Data limite: {data_limite}\n"
                f"Modo: {'SIMULAÇÃO (dry-run)' if dry_run else 'EXECUÇÃO REAL'}\n"
                f"{'=' * 60}\n"
            )
        )

        # Encontrar inscritos da comunidade sem prontuário ativo e antigos
        inscritos_comun = Inscritocomunidade.objects.filter(
            dthinscricao__lt=data_limite,
            status=True
        ).exclude(
            prontuario__status_ativo=True
        )

        # Encontrar inscritos de convênio sem prontuário ativo e antigos
        inscritos_conv = Inscritoconvenio.objects.filter(
            dthinscricao__lt=data_limite
        ).exclude(
            prontuario__status_ativo=True
        )

        total_comun = inscritos_comun.count()
        total_conv = inscritos_conv.count()
        total = total_comun + total_conv

        self.stdout.write(f"\nInscritos da Comunidade a anonimizar: {total_comun}")
        self.stdout.write(f"Inscritos de Convênio a anonimizar: {total_conv}")
        self.stdout.write(self.style.WARNING(f"TOTAL: {total} registros\n"))

        if total == 0:
            self.stdout.write(self.style.SUCCESS("✓ Nenhum registro para anonimizar."))
            return

        if not dry_run:
            confirmacao = input(f"\nDeseja prosseguir com a anonimização de {total} registros? (sim/não): ")
            if confirmacao.lower() not in ['sim', 's', 'yes', 'y']:
                self.stdout.write(self.style.ERROR("Operação cancelada pelo usuário."))
                return

            # Anonimizar Comunidade
            for inscrito in inscritos_comun:
                self._anonimizar_comunidade(inscrito)

            # Anonimizar Convênio
            for inscrito in inscritos_conv:
                self._anonimizar_convenio(inscrito)

            logger.info(f"Anonimizados {total} registros de inscritos inativos (LGPD)")
            self.stdout.write(
                self.style.SUCCESS(f"\n✓ {total} registros anonimizados com sucesso!")
            )
        else:
            self.stdout.write(
                self.style.WARNING("\n[DRY-RUN] Nenhuma alteração foi feita no banco de dados.")
            )

    def _anonimizar_comunidade(self, inscrito):
        """Anonimiza dados sensíveis de um inscrito da comunidade."""
        inscrito.nomeinscrito = f"ANONIMIZADO_{inscrito.idfichacomunidade}"
        inscrito.cpfinscrito = f"000000000{inscrito.idfichacomunidade:02d}"
        inscrito.emailinscrito = f"anonimizado{inscrito.idfichacomunidade}@lgpd.local"
        inscrito.tellcellinscrito = "00000000000"
        inscrito.contatourgencia = "00000000000"
        inscrito.nomecontatourgencia = "ANONIMIZADO"
        
        # Responsável
        if inscrito.nomeresp:
            inscrito.nomeresp = "ANONIMIZADO"
            inscrito.cpfresp = None
            inscrito.tellcellresp = None
            inscrito.emailresp = None
        
        inscrito.status = False
        inscrito.save()

    def _anonimizar_convenio(self, inscrito):
        """Anonimiza dados sensíveis de um inscrito de convênio."""
        inscrito.nomeinscrito = f"ANONIMIZADO_{inscrito.idfichaconvenio}"
        inscrito.cpfinscrito = f"000000000{inscrito.idfichaconvenio:02d}"
        inscrito.emailinscrito = f"anonimizado{inscrito.idfichaconvenio}@lgpd.local"
        inscrito.tellcellinscrito = "00000000000"
        inscrito.contatourgencia = "00000000000"
        
        # Responsável
        if inscrito.nomeresp:
            inscrito.nomeresp = "ANONIMIZADO"
            inscrito.cpfresp = None
            inscrito.tellcellresp = None
            inscrito.emailresp = None
        
        inscrito.status = False
        inscrito.save()
