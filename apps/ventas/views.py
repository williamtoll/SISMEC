import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template import loader
from datetime import datetime
from apps.clientes.models import Cliente
from apps.productos.models import Producto
from apps.recepcion.models import RecepcionVehiculo
from apps.ventas.models import PresupuestoCab, PresupuestoDet
from django.contrib import messages
import json
from django.urls import reverse
from sismec.dao import venta_dao

# Agregar un presupuesto
from sismec.configuraciones import ROW_PER_PAGE


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def agregarPresupuesto(request):
    t = loader.get_template('ventas/agregar.html')
    if request.method == 'POST':
        # Obtener la recepcion
        recepcion_list = request.POST.get('id_recepcion_select', '')

        # Obtener fecha
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        try:
            for recepcion_id in recepcion_list:
                recepcion = RecepcionVehiculo.objects.get(id=recepcion_id)

            nuevoPresupuesto = PresupuestoCab()
            #nuevaOC.fecha_pedido = fecha
            nuevoPresupuesto.recepcion_vehiculo = recepcion
            nuevoPresupuesto.estado = PresupuestoCab.PENDIENTE
            nuevoPresupuesto.fecha_presupuesto = fecha
            nuevoPresupuesto.save()
            lista_detalles = json.loads(request.POST.get('detalle', ''))
            for key in lista_detalles:
                detalle = PresupuestoDet()
                nombre_producto = lista_detalles[key]['descripcion']
                producto = Producto.objects.get(descripcion__exact=nombre_producto)
                detalle.presupuesto_cab = nuevoPresupuesto
                detalle.producto = producto
                detalle.cantidad = lista_detalles[key]['cantidad']
                detalle.precio_unitario = lista_detalles[key]['monto']
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

@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar PRODUCTOS existentes.
def listarPresupuestos(request):
    t = loader.get_template('ventas/listado.html')
    if request.method == 'GET':
        data = request.GET

        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'codigo': data.get('codigo_select', ''), 'fecha': data.get('fecha', ''),
                   'estado': data.get('estado', '')}

        query_param_list = [filtros['row_per_page'], filtros['codigo'], filtros['fecha'], filtros['estado']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = venta_dao.getPresupuestoFiltro(filtros)

        c = {
            'object_list': object_list,
            'pagination': pagination,
            'filtros': filtros,
            'query_params': query_params
        }
        return HttpResponse(t.render(c, request))
