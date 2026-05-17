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