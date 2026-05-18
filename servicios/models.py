from django.db import models
from django.contrib.auth.models import User


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class PerfilTecnico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    presentacion = models.TextField(blank=True, null=True)
    
    foto_trabajo = models.ImageField(upload_to='trabajos_tecnicos/', null=True, blank=True)
    especialidades = models.ManyToManyField(Especialidad, blank=True)
    def __str__(self):
        return self.usuario.username
    
class SolicitudServicio(models.Model):
    descripcion = models.TextField()
    fecha = models.DateField()
    horario = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    referencias = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    estatus = models.CharField(max_length=20, default='Pendiente')

    def __str__(self):
        return f"Cita para el {self.fecha} - {self.horario}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto_perfil = models.ImageField(upload_to='perfiles/', default='perfiles/default.png', null=True, blank=True)
    biografia = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    
