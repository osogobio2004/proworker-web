from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario, ProuestaReagendamiento

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
        fields = ['foto_perfil']

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            
class FormularioReagendamiento(forms.ModelForm):
    nueva_fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Nueva fecha'
    )
    
    nuevo_horario = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label='Nuevo horario'
    )
    
    motivo = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe brevemente por qué no puedes asistir a la fecha programada...'
        }),
        label='Motivo de reagendamiento'
    )

    class Meta:
        model = ProuestaReagendamiento
        fields = ['nueva_fecha', 'nuevo_horario', 'motivo']