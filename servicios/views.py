from django.shortcuts import render
from .models import PerfilTecnico

def index(request):
    tecnicos = PerfilTecnico.objects.all()
    return render(request, 'servicios/home.html', {'tecnicos': tecnicos})