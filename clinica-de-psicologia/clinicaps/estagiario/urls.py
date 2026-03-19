from django.urls import path
from . import views

app_name = 'estagiario'

urlpatterns = [
    path('dashboard/', views.dashboard_estagiario, name='home'),
    path('consulta-inscritos/', views.consulta_inscritos, name='consulta_inscritos'),
    path('vincular-paciente/', views.vincular_paciente, name='vincular_paciente'),
    path('adicionar-evolucao/', views.adicionar_evolucao, name='adicionar_evolucao'),
    path('prontuario/<int:pk>/nova-evolucao/', views.nova_evolucao, name='nova_evolucao'),
    path('dados-inscrito/<int:pk>/', views.dados_inscrito, name='dados_inscrito'),
    path('dados-inscrito-detalhe/<str:tipo>/<int:pk>/', views.dados_inscrito_detalhe, name='dados_inscrito_detalhe'),
]
