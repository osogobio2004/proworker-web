from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FormularioRegistroCustom(UserCreationForm):
    # Campos personalizados adicionales
    nombre_completo = forms.CharField(
        max_length=150, 
        required=True, 
        label="Nombre Completo",
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Romina Aranza Osogobio'})
    )
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
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
    
    # Datos específicos para poder brindar servicios
    telefono = forms.CharField(
        max_length=15, 
        required=False, 
        label="Teléfono de Contacto",
        widget=forms.TextInput(attrs={'placeholder': '993XXXXXXX'})
    )
    
    OPCIONES_MUNICIPIO = [
        ('Balancán', 'Balancán'),
        ('Centro', 'Centro (Villahermosa)'),
        ('Cárdenas', 'Cárdenas'),
        ('Comalcalco', 'Comalcalco'),
        ('Huimanguillo', 'Huimanguillo'),
        ('Jalpa de Méndez', 'Jalpa de Méndez'),
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
        # Decimos qué campos oficiales de Django queremos conservar
        fields = UserCreationForm.Meta.fields + ('email',)