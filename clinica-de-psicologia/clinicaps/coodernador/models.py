from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from usuarios.models import Usuario
from formulario.models import Inscritocomunidade, Inscritoconvenio

class Prontuario(models.Model):
    """
    Representa o vínculo entre o Estagiário e o Paciente (Inscrito).
    Quando o estagiário 'escolhe' um paciente da fila, este registro é criado.
    """
    idprontuario = models.AutoField(primary_key=True)
    coordenador = models.ForeignKey(
        Usuario, 
        on_delete=models.PROTECT, 
        related_name='prontuarios_coordenador',
        limit_choices_to={'cargo': 'COORD'},
        verbose_name="Coordenador Geral"
    )
    
    supervisor = models.ForeignKey(
        Usuario, 
        on_delete=models.PROTECT, 
        related_name='prontuarios_supervisor',
        limit_choices_to={'cargo': 'SUPER'},
        verbose_name="Supervisor"
    )
    
    estagiario = models.ForeignKey(
        Usuario, 
        on_delete=models.PROTECT, 
        related_name='prontuarios_estagiario',
        limit_choices_to={'cargo': 'ESTAG'},
        verbose_name="Estagiário Responsável"
    )

    paciente_convenio = models.ForeignKey(
        Inscritoconvenio, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        verbose_name="Paciente (Convénio)"
    )
    
    paciente_comunidade = models.ForeignKey(
        Inscritocomunidade, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        verbose_name="Paciente (Comunidade)"
    )

    dth_abertura = models.DateTimeField(default=timezone.now, verbose_name="Data de Abertura")
    status_ativo = models.BooleanField(default=True, verbose_name="Em Atendimento")
    tcle_assinado = models.FileField(upload_to='tcle/', null=True, blank=True, verbose_name="TCLE Assinado")

    class Meta:
        db_table = 'prontuario'
        verbose_name = 'Prontuário (Vínculo)'
        verbose_name_plural = 'Prontuários'
        indexes = [
            models.Index(fields=['estagiario', 'status_ativo'], name='idx_pront_estag_status'),
            models.Index(fields=['status_ativo'], name='idx_pront_status'),
            models.Index(fields=['paciente_comunidade'], name='idx_pront_pac_comun'),
            models.Index(fields=['paciente_convenio'], name='idx_pront_pac_conv'),
            models.Index(fields=['supervisor'], name='idx_pront_supervisor'),
        ]

    def __str__(self):
        nome = "Paciente"
        if self.paciente_comunidade:
            nome = self.paciente_comunidade.nomeinscrito
        elif self.paciente_convenio:
            nome = self.paciente_convenio.nomeinscrito
        return f"{nome} - Estagiário: {self.estagiario.nome_completo}"


class Evolucao(models.Model):
    """
    Funcionalidade simplificada de atendimento.
    O estagiário entra, seleciona a data que ocorreu a consulta e escreve um resumo curto.
    """
    idevolucao = models.AutoField(primary_key=True)
    
    prontuario = models.ForeignKey(
        Prontuario, 
        on_delete=models.CASCADE, 
        related_name='evolucoes',
        verbose_name="Paciente Vinculado"
    )
    
    descricao = models.TextField(
        validators=[MaxLengthValidator(500)],
        verbose_name="Comentário sobre a consulta (Máx 500 caracteres)",
        help_text="Descreva brevemente como foi o atendimento."
    )
    data_atendimento = models.DateField(verbose_name="Data da Consulta")
    dth_registro = models.DateTimeField(default=timezone.now, verbose_name="Registrado em")

    class Meta:
        db_table = 'evolucao'
        verbose_name = 'Anotação de Consulta'
        verbose_name_plural = 'Anotações de Consultas'
        ordering = ['-data_atendimento']

    def __str__(self):
        return f"Consulta dia {self.data_atendimento} - {self.prontuario}"