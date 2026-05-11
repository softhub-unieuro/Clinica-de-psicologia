from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required 
from django.views.generic import UpdateView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import (
    CustomLoginForm,
    EstagiarioForm,
    SupervisorForm,
    CoordenadorForm,
    ResponsavelTecnicoForm,
    SecretariaForm
)
from .models import Usuario


# ==========================================
# REDIRECIONAMENTO APÓS LOGIN
# ==========================================
@login_required
def redirect_after_login(request):
    user = request.user

    if user.cargo == 'COORD':
        return redirect('coodernador:coord')
    elif user.cargo == 'SUPER':
        return redirect('supervisor:dashboard')
    elif user.cargo == 'ESTAG':
        return redirect('estagiario:home')
    elif user.cargo == 'RESP_TEC':
        return redirect('resptecn:dashboard')

    return render(request, 'dashboard_coord.html')


# ==========================================
# LOGIN
# ==========================================
class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        from axes.models import AccessAttempt
        AccessAttempt.objects.filter(username=self.request.POST.get('username')).delete()
        return reverse_lazy('redirect_dashboard')


# ==========================================
# CADASTRO COM MULTIPLOS FORMS
# ==========================================
class CadastroUsuarioView(View):
    template_name = 'cadastro.html'

    def get(self, request):
        context = {
            'supervisores': Usuario.objects.filter(cargo='SUPER', is_active=True)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cargo = request.POST.get('cargo')

        # 🔥 Escolhe o form baseado no cargo
        form_class = {
            'ESTAG': EstagiarioForm,
            'SUPER': SupervisorForm,
            'COORD': CoordenadorForm,
            'RESP_TEC': ResponsavelTecnicoForm,
            'SEC': SecretariaForm
        }.get(cargo)

        if not form_class:
            messages.error(request, "Cargo inválido.")
            return redirect('cadastro')

        form = form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('login')

        # Se der erro, volta com os dados preenchidos
        context = {
            'form': form,
            'supervisores': Usuario.objects.filter(cargo='SUPER', is_active=True)
        }
        return render(request, self.template_name, context)


# ==========================================
# SEGURANÇA (APENAS COORDENADOR)
# ==========================================
class CoordenadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.cargo == 'COORD' or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado. Apenas Coordenadores.")
        return redirect('coodernador:home')


# ==========================================
# EDITAR USUÁRIO
# ==========================================
class EditarUsuarioView(LoginRequiredMixin, CoordenadorRequiredMixin, View):
    template_name = 'cadastro.html'

    def get(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)

        form_class = {
            'ESTAG': EstagiarioForm,
            'SUPER': SupervisorForm,
            'COORD': CoordenadorForm,
            'RESP_TEC': ResponsavelTecnicoForm,
            'SEC': SecretariaForm
        }.get(usuario.cargo)

        form = form_class(instance=usuario)

        context = {
            'form': form,
            'usuario': usuario,
            'supervisores': Usuario.objects.filter(cargo='SUPER', is_active=True)
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)

        form_class = {
            'ESTAG': EstagiarioForm,
            'SUPER': SupervisorForm,
            'COORD': CoordenadorForm,
            'RESP_TEC': ResponsavelTecnicoForm,
            'SEC': SecretariaForm
        }.get(usuario.cargo)

        form = form_class(request.POST, request.FILES, instance=usuario)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect('coodernador:coord')

        context = {
            'form': form,
            'usuario': usuario,
            'supervisores': Usuario.objects.filter(cargo='SUPER', is_active=True)
        }
        return render(request, self.template_name, context)


# ==========================================
# DELETAR USUÁRIO
# ==========================================
class DeletarUsuarioView(LoginRequiredMixin, CoordenadorRequiredMixin, View):
    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)

        if usuario == request.user:
            messages.error(request, "Você não pode excluir a si mesmo.")
            return redirect('coodernador:coord')

        usuario.soft_delete()
        messages.success(request, "Usuário desativado.")
        return redirect('coodernador:coord')


# ==========================================
# NOVA SENHA
# ==========================================
class NovaSenhaView(TemplateView):
    template_name = 'NovaSenha.html'
    
    def post(self, request, *args, **kwargs):
        nova_senha = request.POST.get('novaSenha')
        confirma_senha = request.POST.get('confirmaSenha')
        
        if nova_senha == confirma_senha:
            messages.success(request, "Senha atualizada com sucesso! (Simulação)")
            return redirect('login')
        else:
            messages.error(request, "As senhas não conferem.")
        
        return render(request, self.template_name)


# ==========================================
# VERIFICAR CÓDIGO
# ==========================================
class VerificarCodigoView(TemplateView):
    template_name = 'VerificarCodigo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = self.request.session.get('reset_email', 'usuario@exemplo.com')
        
        try:
            user_part, domain_part = email.split('@')
            masked_user = user_part[:2] + '*' * (len(user_part) - 2)
            context['email_mascarado'] = f"{masked_user}@{domain_part}"
        except:
            context['email_mascarado'] = email
            
        return context

    def post(self, request, *args, **kwargs):
        codigo_digitado = request.POST.get('codigo')
        codigo_correto = '123456'

        if codigo_digitado == codigo_correto:
            messages.success(request, "Código verificado com sucesso!")
            return redirect('nova_senha')
        else:
            messages.error(request, "Código inválido ou expirado.")
            return self.render_to_response(self.get_context_data())