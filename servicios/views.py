from urllib import request

from django.shortcuts import render, redirect
from .models import Especialidad, SolicitudServicio, ProuestaReagendamiento, ConfirmacionTerminacion
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistroCustom, EditarPerfilForm, FormularioReagendamiento
from .models import SolicitudServicio, PerfilTecnico, PerfilUsuario
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

ROL_ACTUAL = 'invitado' 

def index(request):
    return render(request, 'servicios/home.html', {'rol': ROL_ACTUAL})

def vista_login(request):
    return render(request, 'registration/login.html', {'rol': ROL_ACTUAL})

def vista_registro(request):
    if request.method == 'POST':
        formulario = FormularioRegistroCustom(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            nombre_completo = formulario.cleaned_data.get('nombre_completo')
            partes = nombre_completo.split(' ', 1)
            usuario.first_name = partes[0]
            usuario.last_name = partes[1] if len(partes) > 1 else ''
            
            usuario.email = formulario.cleaned_data.get('email')
            
            tipo = formulario.cleaned_data.get('tipo_usuario')
            if tipo == 'tecnico':
                usuario.is_staff = True
            
            usuario.save()
            
            if tipo == 'tecnico':
                PerfilTecnico.objects.create(
                    usuario=usuario,
                    telefono=formulario.cleaned_data.get('telefono'),
                )
            
            messages.success(request, '¡Cuenta creada con éxito! Inicia sesión para comprobar tu rol.')
            return redirect('login')
    else:
        formulario = FormularioRegistroCustom()
        
    return render(request, 'registration/registro.html', {'form': formulario})

    return render(request, 'registration/registro.html', {'form': formulario, 'rol': ROL_ACTUAL})
def about(request):
    return render(request, 'servicios/about.html', {'rol': ROL_ACTUAL})

def contact(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        try:
            # Enviar correo al administrador
            asunto = f'Nuevo mensaje de contacto de {nombre}'
            contenido = f"""
            Nombre: {nombre}
            Correo: {email}
            
            Mensaje:
            {mensaje}
            """
            
            send_mail(
                asunto,
                contenido,
                email,
                ['proworker288@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Nos pondremos en contacto pronto.')
            return redirect('contacto')
        except Exception as e:
            messages.error(request, f'Error al enviar el mensaje: {str(e)}')
            return redirect('contacto')
    
    return render(request, 'servicios/contact.html', {'rol': ROL_ACTUAL})

def catalogo(request):
    return render(request, 'servicios/catalogo.html', {'rol': ROL_ACTUAL})

@login_required(login_url='login')
def perfil_tecnico(request):
    return render(request, 'servicios/detalles_tecnico.html', {'rol': ROL_ACTUAL})

@login_required(login_url='login')
def crear_solicitud(request):
    if request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard_tecnico')
    if request.method == 'POST':
        cliente=request.user,
        v_descripcion = request.POST.get('descripcion')
        v_fecha = request.POST.get('fecha')
        v_horario = request.POST.get('horario')
        v_direccion = request.POST.get('direccion')
        v_referencias = request.POST.get('referencias')

        SolicitudServicio.objects.create(
            cliente=request.user,
            descripcion=v_descripcion,
            fecha=v_fecha,
            horario=v_horario,
            direccion=v_direccion,
            referencias=v_referencias
        )
        return redirect('historial_cliente')

    return render(request, 'servicios/crear_solicitud.html', {'rol': ROL_ACTUAL})

@login_required(login_url='login')
def historial_cliente(request):
    solicitudes_reales = SolicitudServicio.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    if request.user.is_staff and not request.user.is_superuser:
        return redirect('dashboard_tecnico')
    
    # Obtener propuestas de reagendamiento pendientes
    propuestas_pendientes = ProuestaReagendamiento.objects.filter(
        solicitud__cliente=request.user,
        estatus='Pendiente'
    ).order_by('-fecha_creacion')
    
    # Obtener confirmaciones de terminación pendientes
    confirmaciones_pendientes = ConfirmacionTerminacion.objects.filter(
        solicitud__cliente=request.user,
        estatus='Pendiente'
    ).order_by('-fecha_creacion')
    
    contexto = {
        'solicitudes': solicitudes_reales,
        'propuestas_reagendamiento_pendientes': propuestas_pendientes,
        'confirmaciones_terminacion_pendientes': confirmaciones_pendientes
    }
    return render(request, 'servicios/historial_cliente.html', contexto)

@login_required(login_url='login')
def editar_perfil(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('index')

    perfil, created = PerfilTecnico.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        print("DATOS RECIBIDOS DEL FORMULARIO:", request.POST)
        perfil.telefono = request.POST.get('telefono', '')
        perfil.municipio = request.POST.get('municipio', '')
        perfil.presentacion = request.POST.get('presentacion', '')
        
        if 'foto_trabajo' in request.FILES:
            perfil.foto_trabajo = request.FILES['foto_trabajo']
            
        perfil.save() 

        ids_especialidades = request.POST.getlist('especialidades')
        perfil.especialidades.set(ids_especialidades)
        
        messages.success(request, '¡Tu oficina ha sido actualizada con éxito!')
        return redirect('dashboard_tecnico')

    # Para poder pintar los checkboxes en el HTML, necesitamos mandarle todas las opciones disponibles
    all_especialidades = Especialidad.objects.all()
    
    contexto = {
        'perfil': perfil,
        'all_especialidades': all_especialidades
    }
    return render(request, 'servicios/editar_perfil.html', contexto)
    

@login_required(login_url='login')
def dashboard_tecnico(request):
    solicitudes_nuevas = SolicitudServicio.objects.filter(estatus='Pendiente').order_by('-fecha_creacion')
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('index')
    contexto = {
        'rol': ROL_ACTUAL,
        'solicitudes': solicitudes_nuevas
    }
    return render(request, 'servicios/dashboard_tecnico.html', contexto)

@login_required(login_url='login')
def aceptar_trabajo(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    solicitud.estatus = 'Aceptado'  
    solicitud.save()                
    return redirect('dashboard_tecnico') 

@login_required(login_url='login')
def rechazar_trabajo(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    solicitud.estatus = 'Rechazado'
    solicitud.save()
    return redirect('dashboard_tecnico')


def vista_login(request):
    if request.method == 'POST':
        usuario_txt = request.POST.get('username')
        clave_txt = request.POST.get('password')

        usuario_valido = authenticate(request, username=usuario_txt, password=clave_txt)

        if usuario_valido is not None:
            auth_login(request, usuario_valido)
            messages.success(request, f'¡Bienvenido de nuevo, {usuario_txt}!')
            return redirect('index') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Intenta de nuevo.')

    return render(request, 'registration/login.html', {'rol': ROL_ACTUAL})

def vista_logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def mi_cuenta(request):
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            # Guardamos datos del User
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            # Guardamos datos del Perfil (foto)
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado!")
            return redirect('mi_cuenta')
    else:
        form = EditarPerfilForm(instance=perfil)
    
    return render(request, 'servicios/mi_cuenta.html', {'form': form})

def catalogo(request):
    if not request.user.is_authenticated:
        messages.info(request, "Inicia sesión para ver nuestro catálogo de expertos.")
        return redirect('login')
    
    if request.user.is_staff:
        return redirect('dashboard_tecnico')
        
    tecnicos = PerfilTecnico.objects.all()
    
    f_especialidad = request.GET.get('especialidad')
    f_municipio = request.GET.get('municipio')
    
    if f_especialidad:
        tecnicos = tecnicos.filter(especialidades__nombre=f_especialidad)
    if f_municipio:
        tecnicos = tecnicos.filter(municipio=f_municipio)
    
    return render(request, 'servicios/catalogo.html', {'tecnicos': tecnicos})

@login_required(login_url='login')
def detalle_tecnico(request, id):
    tecnico = PerfilTecnico.objects.get(id=id)
    return render(request, 'servicios/detalle_tecnico.html', {'tecnico': tecnico})

@login_required(login_url='login')
def agenda_tecnico(request):

    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('index')
    
  
    trabajos_aceptados = SolicitudServicio.objects.filter(estatus='Aceptado').order_by('fecha')
    
    contexto = {
        'trabajos': trabajos_aceptados
    }
    return render(request, 'servicios/agenda_tecnico.html', contexto)
@login_required(login_url='login')
def proponer_reagendamiento(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    
    # Validar que el técnico sea quien aceptó el trabajo
    if solicitud.estatus != 'Aceptado':
        messages.error(request, 'Solo puedes reagendar trabajos que hayas aceptado.')
        return redirect('dashboard_tecnico')
    
    if request.method == 'POST':
        formulario = FormularioReagendamiento(request.POST)
        if formulario.is_valid():
            propuesta = formulario.save(commit=False)
            propuesta.solicitud = solicitud
            propuesta.tecnico = request.user
            propuesta.save()
            
            messages.success(request, '¡Propuesta de reagendamiento enviada al cliente!')
            return redirect('agenda_tecnico')
    else:
        formulario = FormularioReagendamiento()
    
    contexto = {
        'solicitud': solicitud,
        'formulario': formulario
    }
    return render(request, 'servicios/proponer_reagendamiento.html', contexto)

@login_required(login_url='login')
def aceptar_reagendamiento(request, id):
    propuesta = ProuestaReagendamiento.objects.get(id=id)
    
    # Validar que el cliente sea quien solicita aceptar
    if propuesta.solicitud.cliente != request.user:
        messages.error(request, 'No tienes permiso para aceptar esta propuesta.')
        return redirect('historial_cliente')
    
    propuesta.estatus = 'Aceptado'
    propuesta.fecha_respuesta = timezone.now()
    propuesta.save()
    
    # Actualizar la solicitud original con la nueva fecha y horario
    solicitud = propuesta.solicitud
    solicitud.fecha = propuesta.nueva_fecha
    solicitud.horario = propuesta.nuevo_horario
    solicitud.save()
    
    messages.success(request, '¡Has aceptado la nueva fecha para el trabajo!')
    return redirect('historial_cliente')

@login_required(login_url='login')
def rechazar_reagendamiento(request, id):
    propuesta = ProuestaReagendamiento.objects.get(id=id)
    
    # Validar que el cliente sea quien solicita rechazar
    if propuesta.solicitud.cliente != request.user:
        messages.error(request, 'No tienes permiso para rechazar esta propuesta.')
        return redirect('historial_cliente')
    
    propuesta.estatus = 'Rechazado'
    propuesta.fecha_respuesta = timezone.now()
    propuesta.save()
    
    # Actualizar la solicitud original a rechazado
    solicitud = propuesta.solicitud
    solicitud.estatus = 'Rechazado'
    solicitud.save()
    
    messages.info(request, 'Has rechazado la propuesta de reagendamiento.')
    return redirect('historial_cliente')

@login_required(login_url='login')
def marcar_trabajo_terminado(request, id):
    solicitud = SolicitudServicio.objects.get(id=id)
    
    # Validar que sea el técnico quien puede marcar como terminado
    if solicitud.estatus != 'Aceptado':
        messages.error(request, 'Solo puedes marcar como terminado trabajos que hayas aceptado.')
        return redirect('agenda_tecnico')
    
    # Crear una confirmación de terminación
    confirmacion, created = ConfirmacionTerminacion.objects.get_or_create(
        solicitud=solicitud,
        tecnico=request.user,
        estatus='Pendiente'
    )
    
    if created:
        messages.success(request, '¡Propuesta de terminación enviada al cliente! Esperando confirmación...')
    else:
        messages.info(request, 'Ya existe una propuesta de terminación pendiente para este trabajo.')
    
    return redirect('agenda_tecnico')

@login_required(login_url='login')
def aceptar_terminacion(request, id):
    confirmacion = ConfirmacionTerminacion.objects.get(id=id)
    
    # Validar que el cliente sea quien solicita aceptar
    if confirmacion.solicitud.cliente != request.user:
        messages.error(request, 'No tienes permiso para aceptar esta confirmación.')
        return redirect('historial_cliente')
    
    confirmacion.estatus = 'Aceptado'
    confirmacion.fecha_respuesta = timezone.now()
    confirmacion.save()
    
    # Actualizar la solicitud como terminada
    solicitud = confirmacion.solicitud
    solicitud.estado_trabajo = 'Terminado'
    solicitud.save()
    
    messages.success(request, '¡Has confirmado que el trabajo está terminado!')
    return redirect('historial_cliente')

@login_required(login_url='login')
def rechazar_terminacion(request, id):
    confirmacion = ConfirmacionTerminacion.objects.get(id=id)
    
    # Validar que el cliente sea quien solicita rechazar
    if confirmacion.solicitud.cliente != request.user:
        messages.error(request, 'No tienes permiso para rechazar esta confirmación.')
        return redirect('historial_cliente')
    
    confirmacion.estatus = 'Rechazado'
    confirmacion.fecha_respuesta = timezone.now()
    confirmacion.save()
    
    messages.info(request, 'Has rechazado la confirmación de terminación. El técnico podrá intentar de nuevo.')
    return redirect('historial_cliente')