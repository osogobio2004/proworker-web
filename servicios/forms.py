from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario

class FormularioRegistroCustom(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=150, 
        required=True, 
        label="Nombre completo",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Juan Pérez'})
    )
    email = forms.EmailField(
        required=True, 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'})
    )
    
    OPCIONES_ROL = [
        ('cliente', 'Quiero buscar y contratar técnicos (Cliente)'),
        ('tecnico', 'Quiero ofrecer mis servicios técnicos (Técnico)')
    ]
    tipo_usuario = forms.ChoiceField(
        choices=OPCIONES_ROL, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="¿Cómo deseas usar ProWorker?"
    )
    
    telefono = forms.CharField(
        max_length=15, 
        required=False, 
        label="Teléfono de contacto",
        widget=forms.TextInput(attrs={'placeholder': '993XXXXXXX'})
    )
    
    OPCIONES_MUNICIPIO = [
        ('Balancán', 'Balancán'),
        ('Cárdenas', 'Cárdenas'),
        ('Centla', 'Centla'),
        ('Centro', 'Centro (Villahermosa)'),
        ('Comalcalco', 'Comalcalco'),
        ('Cunduacán', 'Cunduacán'),
        ('Emiliano Zapata', 'Emiliano Zapata'),
        ('Huimanguillo', 'Huimanguillo'),
        ('Jalapa', 'Jalapa'),
        ('Jalpa de Méndez', 'Jalpa de Méndez'),
        ('Jonuta', 'Jonuta'),
        ('Macuspana', 'Macuspana'),
        ('Nacajuca', 'Nacajuca'),
        ('Paraíso', 'Paraíso'),
        ('Tacotalpa', 'Tacotalpa'),
        ('Teapa', 'Teapa'),
        ('Tenosique', 'Tenosique')
    ]
    municipio = forms.ChoiceField(
        choices=OPCIONES_MUNICIPIO,
        required=False,
        label="Municipio base de operación"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Nombre(s)")
    last_name = forms.CharField(max_length=100, label="Apellidos")
    email = forms.EmailField(label="Correo Electrónico")

    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil', 'biografia']

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email