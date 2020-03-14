from django.forms import ModelForm, TextInput
from django import forms
from .models import City, Notification

class CityForm(ModelForm):
    class Meta:
        model = City 
        fields = ['requestBody']
        widgets = {'requestBody' : TextInput(attrs={'class' : 'input'})}

class ConfigurationForm(ModelForm):
    class Meta:
        model = Notification 
        fields = ['ServidorPagoEfectivo',
                  'AccessKey',
                  'SecretKey',
                  'IDComercio',
                  'NombreComercio',
                  'EmailComercio',
                  'ModoIntegracion',
                  'TiempoExpiracionPago',
                  'Pais',
                  'TipoMoneda',
                  'Monto'
                  ]
        widgets = {'ServidorPagoEfectivo' : TextInput(attrs={'class' : 'input'}),
                    'AccessKey' : TextInput(attrs={'class' : 'input'}),
                    'SecretKey' : TextInput(attrs={'class' : 'input'}),
                    'IDComercio' : TextInput(attrs={'class' : 'input'}),
                    'NombreComercio' : TextInput(attrs={'class' : 'input'}),
                    'EmailComercio' : TextInput(attrs={'class' : 'input'}),
                    'ModoIntegracion' : TextInput(attrs={'class' : 'input'})
                    }
        # ServidorPagoEfectivo = forms.CharField(max_length=25,
        # widget=forms.TextInput(
        #     attrs={'class': 'mensajeRequeridoModel', 'placeholder': 'IONGRESAA'}
        # ))