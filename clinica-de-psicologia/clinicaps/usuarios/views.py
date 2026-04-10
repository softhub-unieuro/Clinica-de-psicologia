from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required 
from django.views.generic import CreateView, ListView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomLoginForm, CadastroUsuarioForm
from .models import Usuario
from django.views.generic import TemplateView


@login_required
def redirect_after_login(request):
    """
    View principal que redireciona para o dashboard específico do cargo.
    """
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

# --- 2. LOGIN E CADASTRO ---

class CustomLoginView(LoginView):
    # CORREÇÃO: Apontando para a pasta do app usuarios
    template_name = 'login.html' 
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        from axes.models import AccessAttempt
        AccessAttempt.objects.filter(username=self.request.POST.get('username')).delete()

        return reverse_lazy('redirect_dashboard')

class CadastroUsuarioView(CreateView):
    model = Usuario
    form_class = CadastroUsuarioForm
    template_name = 'cadastro.html' 
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passa os supervisores para o template
        context['supervisores'] = Usuario.objects.filter(cargo='SUPER', is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Usuário cadastrado com sucesso!")
        return super().form_valid(form) 

# --- 3. MIXIN DE SEGURANÇA ---

class CoordenadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.cargo == 'COORD' or self.request.user.is_superuser)

    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado. Apenas Coordenadores.")
        return redirect('coodernador:home')

# --- 4. DASHBOARDS ---
# (Movidos para o app daashboard)

# --- 5. CRUD ---

class EditarUsuarioView(LoginRequiredMixin, CoordenadorRequiredMixin, UpdateView):
    model = Usuario
    form_class = CadastroUsuarioForm
    template_name = 'cadastro.html'
    success_url = reverse_lazy('coodernador:coord')

    def form_valid(self, form):
        messages.success(self.request, "Dados atualizados com sucesso.")
        return super().form_valid(form)

class DeletarUsuarioView(LoginRequiredMixin, CoordenadorRequiredMixin, View):
    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        if usuario == request.user:
            messages.error(request, "Você não pode excluir a si mesmo.")
            return redirect('coodernador:coord')
            
        usuario.soft_delete()
        messages.success(request, "Usuário desativado.")
        return redirect('coodernador:coord')

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

class VerificarCodigoView(TemplateView):
    template_name = 'VerificarCodigo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tenta pegar o e-mail que foi salvo na sessão na etapa anterior (Esqueci Senha)
        # Como ainda não temos a tela anterior, vou deixar um valor fixo de teste se não encontrar
        email = self.request.session.get('reset_email', 'usuario@exemplo.com')
        
        # Lógica simples para mascarar o e-mail (ex: vit***@gmail.com)
        try:
            user_part, domain_part = email.split('@')
            if len(user_part) > 2:
                masked_user = user_part[:2] + '*' * (len(user_part) - 2)
            else:
                masked_user = user_part
            context['email_mascarado'] = f"{masked_user}@{domain_part}"
        except:
            context['email_mascarado'] = email
            
        return context

    def post(self, request, *args, **kwargs):
        codigo_digitado = request.POST.get('codigo')
        
        # --- LÓGICA DE VERIFICAÇÃO (MOCK / SIMULAÇÃO) ---
        # Aqui, no futuro, vamos comparar com o código salvo no Banco ou Redis.
        # Por enquanto, vamos aceitar o código '123456' para teste.
        codigo_correto = '123456' 

        if codigo_digitado == codigo_correto:
            messages.success(request, "Código verificado com sucesso!")
            # Redireciona para a tela de Nova Senha que criamos antes
            return redirect('nova_senha')
        else:
            messages.error(request, "Código inválido ou expirado. Tente novamente.")
            return self.render_to_response(self.get_context_data())