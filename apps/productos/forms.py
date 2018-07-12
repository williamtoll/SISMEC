from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm

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
    # nombre = forms.CharField(widget=forms.TextInput(
    #     attrs={'placeholder': 'Ingrese el nombre del autor',
    #            'required': 'true'
    #            }), validators=[MaxLengthValidator(100)])

    class Meta:

        model = Producto
        fields = ['nombre', 'descripcion', 'marca', 'cantidad', 'precio_venta',
                  'exentas','iva10','iva5', 'tipo_producto','direccion']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)