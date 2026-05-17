from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.vista_login, name='login'),
    path('registro/', views.vista_registro, name='registro'),
    path('about/', views.about, name='nosotros'),   # Ruta de Nosotros
    path('contact/', views.contact, name='contacto'), # Ruta de Contacto
]