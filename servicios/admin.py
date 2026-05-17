from django.contrib import admin
from .models import SolicitudServicio, PerfilTecnico, PerfilUsuario

admin.site.register(SolicitudServicio)
admin.site.register(PerfilTecnico)
admin.site.register(PerfilUsuario)