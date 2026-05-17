from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.vista_login, name='login'),
    path('registro/', views.vista_registro, name='registro'),
    path('about/', views.about, name='nosotros'),
    path('contact/', views.contact, name='contacto'),
    path('tecnico-detalle/', views.perfil_tecnico, name='perfil_tecnico'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('solicitar/', views.crear_solicitud, name='crear_solicitud'),
    path('mis-servicios/', views.historial_cliente, name='historial_cliente'),
    path('mi-perfil/', views.editar_perfil, name='editar_perfil'),
    path('dashboard/', views.dashboard_tecnico, name='dashboard_tecnico'),
]