import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template import loader
from datetime import datetime
from apps.clientes.models import Cliente
from apps.productos.models import Producto
from apps.ventas.models import PresupuestoCab, PresupuestoDet
from django.contrib import messages
import json
from django.urls import reverse

# Agregar un presupuesto
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def agregarPresupuesto(request):
    t = loader.get_template('ventas/agregar.html')
    if request.method == 'POST':
        # Obtener el cliente
        cliente_list = request.POST.get('id_cliente_select', '')

        # Obtener fecha
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        try:
            for cliente_id in cliente_list:
                cliente = Cliente.objects.get(id=cliente_id)
            nuevoPresupuesto = PresupuestoCab()
            #nuevaOC.fecha_pedido = fecha
            nuevoPresupuesto.cliente= cliente
            nuevoPresupuesto.estado = PresupuestoCab.PENDIENTE
            nuevoPresupuesto.fecha_presupesto = fecha
            nuevoPresupuesto.save()
            lista_detalles = json.loads(request.POST.get('detalle', ''))
            for key in lista_detalles:
                detalle = PresupuestoDet()
                nombre_producto = lista_detalles[key]['descripcion']
                producto = Producto.objects.get(descripcion__exact=nombre_producto)
                detalle.presupuesto_cab = nuevoPresupuesto
                detalle.producto = producto
                detalle.cantidad = lista_detalles[key]['cantidad']
                detalle.save()

            messages.add_message(request, messages.INFO, 'Presupuesto agregado exitosamente')
            return HttpResponseRedirect(reverse('frontend_home'))
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR, e.args)
            return HttpResponse(t.render(request))
    else:
        c = {}
        return HttpResponse(t.render(c, request))
