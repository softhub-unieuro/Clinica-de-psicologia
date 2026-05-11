import string
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario


# =========================
# LOGIN
# =========================
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua Matrícula',
            'autofocus': True
        }),
        label="Matrícula"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sua Senha'
        }),
        label="Senha"
    )


# =========================
# FORM BASE (REUTILIZÁVEL)
# =========================
class BaseUsuarioForm(forms.ModelForm):

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    senha2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/jpg'
        })
    )

    class Meta:
        model = Usuario

        fields = (
            'matricula',
            'nome_completo',
            'cpf',
            'email',
            'telefone',
            'data_nascimento',
            'foto_perfil',
            'crp',
            'semestre',
            'nivel_estagio',
            'supervisor_vinculado'
        )

        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    # =========================
    # VALIDAÇÕES
    # =========================

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")
        usuario_id = getattr(self.instance, "id", None)

        if Usuario.objects.filter(matricula=matricula).exclude(id=usuario_id).exists():
            raise forms.ValidationError("Esta matrícula já está cadastrada.")

        return matricula

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        # ACEITA CPF VAZIO
        if not cpf:
            return None

        cpf_limpo = re.sub(r'\D', '', cpf)

        if len(cpf_limpo) != 11:
            raise forms.ValidationError("O CPF deve ter 11 dígitos.")

        usuario_id = getattr(self.instance, "id", None)

        if Usuario.objects.filter(cpf=cpf_limpo).exclude(id=usuario_id).exists():
            raise forms.ValidationError("CPF já cadastrado.")

        return cpf_limpo

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and not (
            email.endswith('@unieuro.com.br') or
            email.endswith('@unieuro.edu.br')
        ):
            raise forms.ValidationError("Use e-mail institucional.")

        usuario_id = getattr(self.instance, "id", None)

        if Usuario.objects.filter(email=email).exclude(id=usuario_id).exists():
            raise forms.ValidationError("E-mail já cadastrado.")

        return email

    def clean_crp(self):
        crp = self.cleaned_data.get('crp')

        if crp:
            crp_limpo = re.sub(r'\D', '', crp)

            if len(crp_limpo) > 9:
                raise forms.ValidationError("CRP inválido.")

            return crp_limpo

        return crp

    def clean_foto_perfil(self):
        foto = self.cleaned_data.get('foto_perfil')

        if foto:

            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Máx 5MB.")

            extensao = foto.name.split('.')[-1].lower()

            if extensao not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Use JPG ou PNG.")

        return foto

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get('senha')
        senha2 = cleaned_data.get('senha2')

        cargo = getattr(self, 'cargo_fixo', None)

        # =========================
        # VALIDAÇÃO SENHA
        # =========================

        if senha:

            if len(senha) < 8 or len(senha) > 16:
                self.add_error('senha', '8-16 caracteres')

            if not any(c.isupper() for c in senha):
                self.add_error('senha', 'Precisa maiúscula')

            if not any(c.islower() for c in senha):
                self.add_error('senha', 'Precisa minúscula')

            if not any(c.isdigit() for c in senha):
                self.add_error('senha', 'Precisa número')

            if not any(c in string.punctuation for c in senha):
                self.add_error('senha', 'Precisa especial')

            if senha != senha2:
                self.add_error('senha2', 'Senhas não conferem')

        # =========================
        # REGRAS POR CARGO
        # =========================

        if cargo == 'ESTAG':

            if not cleaned_data.get('semestre'):
                self.add_error('semestre', 'Obrigatório')

            if not cleaned_data.get('nivel_estagio'):
                self.add_error('nivel_estagio', 'Obrigatório')

            cleaned_data['crp'] = None

        elif cargo in ['SUPER', 'RESP_TEC', 'COORD']:

            if not cleaned_data.get('crp'):
                self.add_error('crp', 'CRP obrigatório')

        return cleaned_data

    # =========================
    # SAVE CORRETO
    # =========================

    def save(self, commit=True):
        usuario = super().save(commit=False)

        # DEFINE O CARGO AUTOMATICAMENTE
        usuario.cargo = self.cargo_fixo

        # DEFINE A SENHA
        senha = self.cleaned_data.get('senha')

        if senha:
            usuario.set_password(senha)

        if commit:
            usuario.save()

        return usuario


# =========================
# ESTAGIÁRIO
# =========================
class EstagiarioForm(BaseUsuarioForm):

    def __init__(self, *args, **kwargs):
        self.cargo_fixo = 'ESTAG'
        super().__init__(*args, **kwargs)

    class Meta(BaseUsuarioForm.Meta):
        fields = [
            'matricula',
            'nome_completo',
            'email',
            'foto_perfil',
            'semestre',
            'nivel_estagio',
            'supervisor_vinculado'
        ]


# =========================
# SUPERVISOR
# =========================
class SupervisorForm(BaseUsuarioForm):

    def __init__(self, *args, **kwargs):
        self.cargo_fixo = 'SUPER'
        super().__init__(*args, **kwargs)

    class Meta(BaseUsuarioForm.Meta):
        fields = [
            'matricula',
            'nome_completo',
            'email',
            'foto_perfil',
            'crp',
            'cpf',
            'telefone',
            'data_nascimento'
        ]


# =========================
# COORDENADOR
# =========================
class CoordenadorForm(BaseUsuarioForm):

    def __init__(self, *args, **kwargs):
        self.cargo_fixo = 'COORD'
        super().__init__(*args, **kwargs)

    class Meta(BaseUsuarioForm.Meta):
        fields = [
            'matricula',
            'nome_completo',
            'email',
            'foto_perfil',
            'crp',
            'cpf',
            'telefone',
            'data_nascimento'
        ]


# =========================
# RESPONSÁVEL TÉCNICO
# =========================
class ResponsavelTecnicoForm(BaseUsuarioForm):

    def __init__(self, *args, **kwargs):
        self.cargo_fixo = 'RESP_TEC'
        super().__init__(*args, **kwargs)

    class Meta(BaseUsuarioForm.Meta):
        fields = [
            'matricula',
            'nome_completo',
            'email',
            'foto_perfil',
            'crp',
            'cpf',
            'telefone',
            'data_nascimento'
        ]


# =========================
# SECRETARIA
# =========================
class SecretariaForm(BaseUsuarioForm):

    def __init__(self, *args, **kwargs):
        self.cargo_fixo = 'SEC'
        super().__init__(*args, **kwargs)

    class Meta(BaseUsuarioForm.Meta):
        fields = [
            'matricula',
            'nome_completo',
            'email',
            'foto_perfil',
            'cpf',
            'telefone',
            'data_nascimento'
        ]