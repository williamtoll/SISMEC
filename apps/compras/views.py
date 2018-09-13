import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods
from datetime import datetime
from apps.proveedores.models import Proveedor
from apps.compras.models import OrdenCompraCab, OrdenCompraDet
from django.contrib import messages
from django.urls import reverse


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
        detalle = request.POST.get('detalle', '')
        detalle = request.POST.getlist('detalle')
        try:
            for proveedor_id in proveedor_list:
                proveedor = Proveedor.objects.get(id=proveedor_id)
            nuevaOC = OrdenCompraCab()
            #nuevaOC.fecha_pedido = fecha
            nuevaOC.proveedor= proveedor
            nuevaOC.estado = OrdenCompraCab.PENDIENTE
            ret = request.POST
            for item in request.POST.get('detalle', ''):
                item['id']
            #nuevaOC.save()
            detalle = request.POST.get('detalle', '')

            messages.add_message(request, messages.INFO, 'Producto agregado exitosamente')
            return HttpResponseRedirect(reverse('productos_listado'))
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR, e.args)
            return HttpResponse(t.render(request))
    else:
        c = {}
        return HttpResponse(t.render(c, request))

