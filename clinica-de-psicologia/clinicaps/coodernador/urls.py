from django.urls import path
from . import views

app_name = 'coodernador'

urlpatterns = [
    # path('', views.dashboard_home, name='home'),
    path('coord/', views.DashboardCoordenadorView.as_view(), name='coord'),
]