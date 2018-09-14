import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods
from datetime import datetime

from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from apps.compras.models import OrdenCompraCab, OrdenCompraDet
from django.contrib import messages
from django.urls import reverse
import json

# Para crear una orden de compra
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# # Funcion para agregar una orden de compra.
def agregarOC(request):
    t = loader.get_template('compras/agregar_oc.html')
    if request.method == 'POST':
        # Obtener el proveedor
        proveedor_list = request.POST.get('id_proveedor_select', '')

        # Obtener fecha
        #fecha = datetime.datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")

        try:
            for proveedor_id in proveedor_list:
                proveedor = Proveedor.objects.get(id=proveedor_id)
            nuevaOC = OrdenCompraCab()
            #nuevaOC.fecha_pedido = fecha
            nuevaOC.proveedor= proveedor
            nuevaOC.estado = OrdenCompraCab.PENDIENTE
            nuevaOC.save()
            lista_detalles = json.loads(request.POST.get('detalle', ''))
            for key in lista_detalles:
                detalle = OrdenCompraDet()
                nombre_producto = lista_detalles[key]['descripcion']
                producto = Producto.objects.get(descripcion__exact=nombre_producto)
                detalle.compra_cab = nuevaOC
                detalle.producto = producto
                detalle.cantidad = lista_detalles[key]['cantidad']
                detalle.save()

            messages.add_message(request, messages.INFO, 'Orden de Compra agregada exitosamente')
            return HttpResponseRedirect(reverse('frontend_home'))
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR, e.args)
            return HttpResponse(t.render(request))
    else:
        c = {}
        return HttpResponse(t.render(c, request))

