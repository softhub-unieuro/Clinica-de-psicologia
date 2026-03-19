import string
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario

# --- 1. Formulário de Login (Que estava faltando) ---
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

class CadastroUsuarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        label='Senha',
        required=True,
        help_text="Requisito: 8-16 caracteres, maiúscula, minúscula, número e especial."
    )
    senha2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'}),
        label='Confirmação da senha',
        required=True
    )
    
    foto_perfil = forms.ImageField(
        required=False,
        label='Foto de Perfil',
        help_text='Formatos: JPG, PNG. Tamanho máximo: 5MB',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/jpg'
        })
    )

    class Meta:
        model = Usuario
        fields = (
            'matricula', 'nome_completo', 'cpf', 'email', 'telefone', 
            'data_nascimento', 'cargo', 'foto_perfil',
            'crp', 
            'semestre', 'nivel_estagio', 'supervisor_vinculado'
        )
        
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select', 'id': 'id_cargo'}),
        }

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")
        usuario_id = getattr(self.instance, "id", None)
        if Usuario.objects.filter(matricula=matricula).exclude(id=usuario_id).exists():
            raise forms.ValidationError("Esta matrícula já está cadastrada.")
        return matricula

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            return cpf
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        if len(cpf_limpo) != 11:
            raise forms.ValidationError("O CPF deve ter 11 dígitos.")
        
        usuario_id = getattr(self.instance, "id", None)
        if Usuario.objects.filter(cpf=cpf_limpo).exclude(id=usuario_id).exists():
            raise forms.ValidationError("CPF já cadastrado no sistema.")
            
        return cpf_limpo
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if not (email.endswith('@unieuro.com.br') or email.endswith('@unieuro.edu.br')):
                raise forms.ValidationError("O e-mail deve ser institucional: @unieuro.com.br ou @unieuro.edu.br")
        
        usuario_id = getattr(self.instance, "id", None)
        if Usuario.objects.filter(email=email).exclude(id=usuario_id).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado no sistema.")
        
        return email
    
    def clean_crp(self):
        crp = self.cleaned_data.get('crp')
        if crp:
            crp_limpo = re.sub(r'\D', '', crp)
            if len(crp_limpo) > 9:
                raise forms.ValidationError("O CRP deve ter no máximo 9 dígitos.")
            return crp_limpo
        return crp
    
    def clean_foto_perfil(self):
        foto = self.cleaned_data.get('foto_perfil')
        if foto:
            # Verifica o tamanho (máximo 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError("A foto deve ter no máximo 5MB.")
            
            # Verifica o formato
            extensao = foto.name.split('.')[-1].lower()
            if extensao not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Formato inválido. Use JPG ou PNG.")
        
        return foto

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        senha2 = cleaned_data.get('senha2')
        cargo = cleaned_data.get('cargo')

        if senha:
            if len(senha) < 8 or len(senha) > 16:
                self.add_error('senha', 'A senha deve ter entre 8 e 16 caracteres.')
            if not any(char.isupper() for char in senha):
                self.add_error('senha', 'A senha precisa ter pelo menos uma letra maiúscula.')
            if not any(char.islower() for char in senha):
                self.add_error('senha', 'A senha precisa ter pelo menos uma letra minúscula.')
            if not any(char.isdigit() for char in senha):
                self.add_error('senha', 'A senha precisa ter pelo menos um número.')
            if not any(char in string.punctuation for char in senha):
                self.add_error('senha', 'A senha precisa ter um caractere especial (@, #, $, etc).')
            if senha != senha2:
                self.add_error('senha2', 'As senhas não conferem.')

        # Validação Condicional
        if cargo == 'ESTAG':
            if not cleaned_data.get('semestre'):
                self.add_error('semestre', 'O semestre é obrigatório para estagiários.')
            if not cleaned_data.get('nivel_estagio'):
                self.add_error('nivel_estagio', 'O nível do estágio é obrigatório.')
            cleaned_data['crp'] = None # Limpa CRP se for estagiário

        elif cargo in ['SUPER', 'RESP_TEC', 'COORD']:
            if not cleaned_data.get('crp'):
                self.add_error('crp', 'O número do CRP é obrigatório para este cargo.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        senha = self.cleaned_data.get('senha')
        if senha:
            usuario.set_password(senha)
        if commit:
            usuario.save()
        return usuario