from django.shortcuts import render, redirect
from .models import SolicitudServicio
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistroCustom, EditarPerfilForm
from .models import SolicitudServicio, PerfilTecnico, PerfilUsuario

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
    contexto = {
        'solicitudes': solicitudes_reales
    }
    return render(request, 'servicios/historial_cliente.html', contexto)

@login_required(login_url='login')
def editar_perfil(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('index')
    return render(request, 'servicios/editar_perfil.html', {'rol': ROL_ACTUAL})

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
        
    return render(request, 'servicios/catalogo.html')