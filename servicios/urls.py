from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.vista_login, name='login'),
    path('registro/', views.vista_registro, name='registro'),
    path('about/', views.about, name='nosotros'),
    path('contact/', views.contact, name='contacto'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('tecnico-detalle/', views.perfil_tecnico, name='perfil_tecnico'),
    path('solicitar/', views.crear_solicitud, name='crear_solicitud'),
    path('mis-servicios/', views.historial_cliente, name='historial_cliente'),
    path('mi-perfil/', views.editar_perfil, name='editar_perfil'),
    path('dashboard/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('aceptar-trabajo/<int:id>/', views.aceptar_trabajo, name='aceptar_trabajo'),
    path('rechazar-trabajo/<int:id>/', views.rechazar_trabajo, name='rechazar_trabajo'),
    path('logout/', views.vista_logout, name='logout'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('tecnico/<int:id>/', views.detalle_tecnico, name='detalle_tecnico'),
]