from django.urls import path
from .views import DashboardRespTecnView, ListaSupervisoresView, SupervisorDetailView

app_name = 'resptecn'

urlpatterns = [
    path('dashboard/', DashboardRespTecnView.as_view(), name='dashboard'),
    path('supervisores/', ListaSupervisoresView.as_view(), name='lista_supervisores'),
    path('supervisor/<int:pk>/', SupervisorDetailView.as_view(), name='supervisor_detail'),
]
