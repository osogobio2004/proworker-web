from django.shortcuts import render

def index(request):
    # 🟢 CONTROL DE ROL SIMULADO: cambia por 'invitado', 'cliente' o 'tecnico'
    # Cambia este valor para probar cómo reacciona dinámicamente tu Header
    rol_simulado = 'invitado' 
    contexto = {
        'rol': rol_simulado
    }
    return render(request, 'servicios/home.html', contexto)

def vista_login(request):
    return render(request, 'registration/login.html')

def vista_registro(request):
    return render(request, 'registration/registro.html')

def about(request):
    return render(request, 'servicios/about.html')

def contact(request):
    return render(request, 'servicios/contact.html')

def catalogo(request):
    return render(request, 'servicios/catalogo.html')

def perfil_tecnico(request):
    return render(request, 'servicios/detalles_tecnico.html')

def crear_solicitud(request):
    return render(request, 'servicios/crear_solicitud.html')

def historial_cliente(request):
    return render(request, 'servicios/historial_cliente.html')

def editar_perfil(request):
    return render(request, 'servicios/editar_perfil.html')

def dashboard_tecnico(request):
    return render(request, 'servicios/dashboard_tecnico.html')