from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class PerfilTecnico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=15)
    experiencia = models.TextField(help_text="Breve descripción de los servicios.")

    def __str__(self):
        return self.usuario.username