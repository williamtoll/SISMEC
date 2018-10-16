from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm, Form
from sismec.settings import DATE_INPUT_FORMATS
from apps.recepcion.models import RecepcionVehiculo, Marca, Modelo

class MarcaForm(ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Ingrese la marca del automovil',
               'required': 'true'
               }), validators=[MaxLengthValidator(100)])

    class Meta:
        model = Marca
        fields = ["descripcion"]

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)

class ModeloForm(ModelForm):

    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Ingrese el modelo del automovil',
               'required': 'true'
               }), validators=[MaxLengthValidator(100)])

    class Meta:
        model = Modelo
        fields = ["descripcion"]

    def __init__(self, *args, **kwargs):
        super(ModeloForm, self).__init__(*args, **kwargs)

class RecepcionVehiculoForm(ModelForm):
    detalle_problema = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Ingrese el detalle del problema','required': 'true', 'cols': 40, 'rows': 3}), validators=[MaxLengthValidator(255)])

    pertencencias_vehiculo = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Ingrese las pertenencias encontradas en el vehiculo', 'required': 'true', 'cols': 40, 'rows': 3}), validators=[MaxLengthValidator(255)])

    class Meta:
        model = RecepcionVehiculo
        fields = ['fecha_recepcion', 'chapa', 'kilometraje',
                  'combustible_aprox', 'año',  'pertencencias_vehiculo',  'detalle_problema']
        exclude = ['cliente', 'marca', 'modelo']

    def __init__(self, *args, **kwargs):
        super(RecepcionVehiculoForm, self).__init__(*args, **kwargs)