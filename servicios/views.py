from django.shortcuts import render

# Vista de la página de inicio (ya la teníamos)
def index(request):
    return render(request, 'servicios/home.html')

# Nueva vista temporal para ver el Login
def vista_login(request):
    return render(request, 'registration/login.html')

# Nueva vista temporal para ver el Registro
def vista_registro(request):
    return render(request, 'registration/registro.html')

def about(request):
    return render(request, 'servicios/about.html')

def contact(request):
    return render(request, 'servicios/contact.html')

def perfil_tecnico(request):
    return render(request, 'servicios/detalles_tecnico.html')

def catalogo(request):
    return render(request, 'servicios/catalogo.html')

def crear_solicitud(request):
    return render(request, 'servicios/crear_solicitud.html')

def historial_cliente(request):
    return render(request, 'servicios/historial_cliente.html')

def editar_perfil(request):
    return render(request, 'servicios/editar_perfil.html')

def dashboard_tecnico(request):
    return render(request, 'servicios/dashboard_tecnico.html')

