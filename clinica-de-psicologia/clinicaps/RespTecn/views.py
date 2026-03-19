from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q, Exists, OuterRef
from usuarios.models import Usuario
from coodernador.models import Prontuario
from formulario.models import Inscritocomunidade, Inscritoconvenio

def contar_inscritos_sem_vinculo_ativo():
    """
    Conta inscritos (comunidade + convênio) que não possuem prontuário ativo.
    Retorna o total de inscritos aguardando triagem.
    """
    # IDs de inscritos que possuem prontuário ATIVO
    ids_comunidade_vinculados = Prontuario.objects.filter(
        status_ativo=True,
        paciente_comunidade__isnull=False
    ).values_list('paciente_comunidade_id', flat=True)
    
    ids_convenio_vinculados = Prontuario.objects.filter(
        status_ativo=True,
        paciente_convenio__isnull=False
    ).values_list('paciente_convenio_id', flat=True)
    
    # Conta inscritos da comunidade com status=True e sem vínculo ativo
    count_comunidade = Inscritocomunidade.objects.filter(
        status=True
    ).exclude(
        idfichacomunidade__in=ids_comunidade_vinculados
    ).count()
    
    # Conta inscritos de convênio (status=True ou NULL) e sem vínculo ativo
    count_convenio = Inscritoconvenio.objects.filter(
        Q(status=True) | Q(status__isnull=True)
    ).exclude(
        idfichaconvenio__in=ids_convenio_vinculados
    ).count()
    
    return count_comunidade + count_convenio

class RespTecnRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.cargo == 'RESP_TEC'

class DashboardRespTecnView(LoginRequiredMixin, RespTecnRequiredMixin, ListView):
    model = Prontuario
    template_name = 'dashboard_resptecn.html'
    context_object_name = 'prontuarios'
    paginate_by = 20

    def get_queryset(self):
        queryset = Prontuario.objects.filter(status_ativo=True).select_related(
            'estagiario', 
            'estagiario__supervisor_vinculado',
            'paciente_comunidade', 
            'paciente_convenio'
        )
        
        # Filtros
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(paciente_comunidade__nomeinscrito__icontains=search) |
                Q(paciente_convenio__nomeinscrito__icontains=search) |
                Q(estagiario__nome_completo__icontains=search)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fila_espera_count'] = contar_inscritos_sem_vinculo_ativo()
        return context


class ListaSupervisoresView(LoginRequiredMixin, RespTecnRequiredMixin, ListView):
    model = Usuario
    template_name = 'lista_supervisores.html'
    context_object_name = 'supervisores'
    paginate_by = 10

    def get_queryset(self):
        queryset = Usuario.objects.filter(cargo='SUPER').annotate(
            num_estagiarios=Count('estagiarios_supervisionados')
        )
        
        # Filtro de busca por nome ou CRP
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome_completo__icontains=search) |
                Q(crp__icontains=search)
            )
        
        # Filtro por abordagem teórica
        abordagem = self.request.GET.get('abordagem')
        if abordagem:
            queryset = queryset.filter(abordagem_teorica=abordagem)
        
        return queryset.order_by('nome_completo')

class SupervisorDetailView(LoginRequiredMixin, RespTecnRequiredMixin, DetailView):
    model = Usuario
    template_name = 'supervisor_detail_rt.html'
    context_object_name = 'supervisor'

    def get_queryset(self):
        return Usuario.objects.filter(cargo='SUPER')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estagiarios = Usuario.objects.filter(
            supervisor_vinculado=self.object, 
            cargo='ESTAG'
        ).annotate(
            num_pacientes=Count('prontuarios_estagiario', filter=Q(prontuarios_estagiario__status_ativo=True))
        )
        context['estagiarios'] = estagiarios
        
        # Calcula total de pacientes de todos os estagiários
        total_pacientes = sum(e.num_pacientes for e in estagiarios)
        context['total_pacientes'] = total_pacientes
        
        return context
