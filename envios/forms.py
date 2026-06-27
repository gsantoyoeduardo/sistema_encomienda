from django import forms
from envios.models import Encomienda
from clientes.models import Cliente
from rutas.models import Ruta


class EncomiendaForm(forms.ModelForm):
    class Meta:
        model = Encomienda
        fields = [
            'codigo',
            'descripcion',
            'peso_kg',
            'estado',
            'fecha_entrega_estimada',
            'remitente',
            'destinatario',
            'ruta',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ENC-000001-LM'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del paquete'
            }),
            'peso_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Ej: 2.50'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_entrega_estimada': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'remitente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'destinatario': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ruta': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remitente'].queryset = Cliente.objects.all()
        self.fields['destinatario'].queryset = Cliente.objects.all()
        self.fields['ruta'].queryset = Ruta.objects.all()
        self.fields['remitente'].label_from_instance = lambda obj: f"{obj.nombre_completo} ({obj.numero_documento})"
        self.fields['destinatario'].label_from_instance = lambda obj: f"{obj.nombre_completo} ({obj.numero_documento})"
        self.fields['ruta'].label_from_instance = lambda obj: f"{obj.origen} → {obj.destino}"
