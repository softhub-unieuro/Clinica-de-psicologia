from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, email, nome_completo, password=None, **extra_fields):
        if not matricula:
            raise ValueError('O usuário deve ter uma matrícula (RA ou Funcional)')
        if not email:
            raise ValueError('O usuário deve ter um endereço de email')

        email = self.normalize_email(email)
        usuario = self.model(
            matricula=matricula,
            email=email,
            nome_completo=nome_completo,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, matricula, email, nome_completo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('cargo', 'COORD')

        return self.create_user(matricula, email, nome_completo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    
    CARGOS_CHOICES = [
        ("COORD", "Coordenador Geral"),
        ("SUPER", "Supervisor"),
        ("RESP_TEC", "Responsável Técnico"),
        ("ESTAG", "Estagiário"),
        ("SEC", "Secretária"),
    ]

    NIVEL_ESTAGIO_CHOICES = (
        ('BASICO', 'Básico'),
        ('AVANCADO', 'Avançado'),
    )

    ABORDAGEM_CHOICES = (
        ('TCC', 'Terapia Cognitivo-Comportamental'),
        ('Psicanalise', 'Psicanálise'),
        ('Humanista', 'Humanista / Fenomenológica'),
        ('Sistemica', 'Sistêmica'),
        ('AnaliseComportamento', 'Análise do Comportamento'),
    )

    # --- IDENTIFICAÇÃO ---
    matricula = models.CharField(max_length=20, unique=True, verbose_name='Matrícula/RA')
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF") 
    email = models.EmailField(unique=True, verbose_name="E-mail Institucional") # Mudamos de email_institucional para email para facilitar
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    data_nascimento = models.DateField(verbose_name='Data de nascimento', null=True, blank=True)
    foto_perfil = models.ImageField(
        upload_to='usuarios/fotos_perfil/',
        blank=True,
        null=True,
        verbose_name="Foto de Perfil",
        help_text="Formatos aceitos: JPG, PNG. Tamanho máximo: 5MB"
    )
    
    cargo = models.CharField(max_length=20, choices=CARGOS_CHOICES, verbose_name="Cargo")

    # --- CAMPOS ESPECÍFICOS (Faltavam estes no seu erro) ---
    crp = models.CharField(max_length=20, blank=True, null=True, verbose_name="CRP")
    abordagem_teorica = models.CharField(max_length=30, choices=ABORDAGEM_CHOICES, blank=True, null=True, verbose_name="Abordagem Teórica")
    
    semestre = models.CharField(max_length=20, blank=True, null=True)
    nivel_estagio = models.CharField(max_length=10, choices=NIVEL_ESTAGIO_CHOICES, blank=True, null=True, verbose_name="Nível do Estágio")
    
    supervisor_vinculado = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'cargo': 'SUPER'},
        related_name='estagiarios_supervisionados',
        verbose_name="Supervisor Responsável"
    )
    
    # --- AUDITORIA ---
    criado_por = models.ForeignKey(
        "self",
        models.SET_NULL,
        related_name="usuarios_criados",
        blank=True,
        null=True,
        verbose_name="Criado por"
    )
    
    dth_insert = models.DateTimeField(default=timezone.now, verbose_name="Data de Criação")
    dth_delete = models.DateTimeField(blank=True, null=True)
    status_delete = models.BooleanField(default=False, verbose_name="Excluído")

    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_staff = models.BooleanField(default=False, verbose_name='Acesso ao Admin')

    objects = UsuarioManager()

    USERNAME_FIELD = "matricula"
    REQUIRED_FIELDS = ['nome_completo', 'email', 'cpf']

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        indexes = [
            models.Index(fields=['cargo'], name='idx_usuario_cargo'),
            models.Index(fields=['cpf'], name='idx_usuario_cpf'),
            models.Index(fields=['matricula'], name='idx_usuario_matricula'),
            models.Index(fields=['supervisor_vinculado'], name='idx_usuario_supervisor'),
            models.Index(fields=['status_delete', 'is_active'], name='idx_usuario_status'),
        ]

    def __str__(self):
        return f"{self.matricula} - {self.nome_completo}"
    
    def soft_delete(self):
        self.status_delete = True
        self.dth_delete = timezone.now()
        self.is_active = False
        self.save()