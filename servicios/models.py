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
    esta_verificado = models.BooleanField(default=False)

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
    
    ESTADO_TRABAJO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Terminado', 'Terminado'),
    ]
    estado_trabajo = models.CharField(max_length=20, choices=ESTADO_TRABAJO_CHOICES, default='Pendiente', null=True, blank=True)

    def __str__(self):
        return f"Cita para el {self.fecha} - {self.horario}"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto_perfil = models.ImageField(upload_to='perfiles/', default='perfiles/default.png', null=True, blank=True)
    biografia = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
 
class ProuestaReagendamiento(models.Model):
    ESTATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    ]
    
    solicitud = models.ForeignKey(SolicitudServicio, on_delete=models.CASCADE, related_name='propuestas_reagendamiento')
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='propuestas_reagendamiento')
    nueva_fecha = models.DateField()
    nuevo_horario = models.CharField(max_length=50)
    motivo = models.TextField()
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reagendamiento de {self.solicitud.id} - {self.estatus}"

    class Meta:
        ordering = ['-fecha_creacion']

class ConfirmacionTerminacion(models.Model):
    ESTATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado'),
    ]
    
    solicitud = models.ForeignKey(SolicitudServicio, on_delete=models.CASCADE, related_name='confirmaciones_terminacion')
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmaciones_terminacion')
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Confirmación de {self.solicitud.id} - {self.estatus}"

    class Meta:
        ordering = ['-fecha_creacion']

class Resena(models.Model):
    solicitud = models.OneToOneField(SolicitudServicio, on_delete=models.CASCADE, related_name='resena')
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenas_recibidas')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenas_dadas')
    calificacion = models.IntegerField(default=5)
    comentario = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.calificacion} Estrellas para {self.tecnico.username} de {self.cliente.username}"