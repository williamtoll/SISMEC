from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm, Form

from apps.productos.models import Producto, TipoProducto

class TipoProductoForm(ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Ingrese el nombre del tipo de producto',
               'required': 'true'
               }), validators=[MaxLengthValidator(100)])

    class Meta:
        model = TipoProducto
        fields = ["nombre"]
        exclude = ['fecha_hora_creacion']

    def __init__(self, *args, **kwargs):
        super(TipoProductoForm, self).__init__(*args, **kwargs)


class ProductoForm(ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Ingrese la descripcion del producto', 'required': 'true', 'cols': 40, 'rows': 3}),
        validators=[MaxLengthValidator(255)])
    marca = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Ingrese la marca del producto', 'required': 'true', 'cols': 40, 'rows': 3}),
        validators=[MaxLengthValidator(255)])

    class Meta:

        model = Producto
        fields = ['descripcion', 'marca', 'precio_venta',
                  'tipo_impuesto']
        exclude = ['tipo_producto']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
