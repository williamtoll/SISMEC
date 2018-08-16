from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm
from apps.proveedores.models import Proveedor

class ProveedorForm(ModelForm):
    nombres = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Ingrese nombre y apellido o razon social',
                'required': 'true'
                }), validators=[MaxLengthValidator(100)])

    ruc = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Ingrese RUC',
               'required': 'true'
               }), validators=[MaxLengthValidator(12)])

    class Meta:

        model = Proveedor
        fields = ['nombres', 'ruc', 'direccion', 'telefono', 'mail']

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)