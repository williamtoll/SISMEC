from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template import loader

from apps.recepcion.forms import RecepcionVehiculoForm
from sismec.utils import custom_permission_required


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('productos.add_producto')
# # Funcion para agregar un producto.
def agregarRecepcionVehiculo(request):
    t = loader.get_template('recepcion/agregar.html')
    if request.method == 'POST':
        form = RecepcionVehiculoForm(request.POST)
        # tipo_producto_list = request.POST.getlist('id_tipo_producto_select', '')
        # try:
        #     if form.is_valid():
        #         for tipo_producto_o in tipo_producto_list:
        #             tipo_producto = TipoProducto.objects.get(id=tipo_producto_o)
        #             form.instance.tipo_producto = tipo_producto
        #         form.save()
        #         messages.add_message(request, messages.INFO, 'Producto agregado exitosamente')
        #         return HttpResponseRedirect(reverse('productos_listado'))
        #     else:
        #         messages.add_message(request, messages.ERROR, form.errors)
        #         c = {'form': form}
        #         return HttpResponse(t.render(c, request))
        # except Exception as e:
        #     traceback.print_exc(e.args)
        #     messages.add_message(request, messages.ERROR, e.args)
        #     c = {'form': form}
        #     return HttpResponse(t.render(c, request))
    else:
        form = RecepcionVehiculoForm()
        c = {'form': form}
        return HttpResponse(t.render(c, request))