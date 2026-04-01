from django.urls import path
from . import views

app_name = 'formulario'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cadastro/comunidade/', views.formulario_comunidade_view, name='formulario_comunidade'),
    path('cadastro/convenio/', views.formulario_convenio_view, name='formulario_convenio'),
]

