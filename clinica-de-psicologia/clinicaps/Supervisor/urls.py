from django.urls import path
from .views import (
    DashboardSupervisorView, 
    EstagiarioDetailView, 
    FinalizarCicloView, 
    DesvincularDevolverView,
    VincularInscritoView,
    ListaProntuariosArquivadosView
)

app_name = 'supervisor'

urlpatterns = [
    path('dashboard/', DashboardSupervisorView.as_view(), name='dashboard'),
    path('estagiario/<int:pk>/', EstagiarioDetailView.as_view(), name='estagiario_detail'),
    path('finalizar-ciclo/<int:pk>/', FinalizarCicloView.as_view(), name='finalizar_ciclo'),
    path('desvincular-devolver/<int:pk>/', DesvincularDevolverView.as_view(), name='desvincular_devolver'),
    path('vincular-inscrito/<str:tipo>/<int:pk>/', VincularInscritoView.as_view(), name='vincular_inscrito'),
    path('arquivados/', ListaProntuariosArquivadosView.as_view(), name='lista_arquivados'),
]
