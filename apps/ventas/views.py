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
from django.views.decorators.csrf import csrf_exempt
from sismec.configuraciones import ROW_PER_PAGE

# Agregar un presupuesto
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def agregarPresupuesto(request):
    t = loader.get_template('ventas/agregar.html')
    if request.method == 'POST':
        # Obtener la recepcion
        recepcion_list = int(request.POST.get('id_recepcion_select', ''))

        # Obtener fecha
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        try:
            recepcion = RecepcionVehiculo.objects.get(id=recepcion_list)
            recepcion.estado = RecepcionVehiculo.PRESUPUESTADO
            recepcion.save()

            nuevoPresupuesto = PresupuestoCab()
            #nuevaOC.fecha_pedido = fecha
            nuevoPresupuesto.recepcion_vehiculo = recepcion
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
            return HttpResponseRedirect(reverse('presupuesto_listado'))
        except Exception as e:
            #traceback.print_exc(e.args)
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

# Funcion para consultar el detalle de una orden de compra.
@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def detallePresupuesto(request, id):
    t = loader.get_template('ventas/detalle.html')
    cabPresupuesto = PresupuestoCab.objects.get(pk = int(id))
    detPresupuesto = PresupuestoDet.objects.filter(presupuesto_cab__id=cabPresupuesto.id)
    fecha_presupuesto = datetime.strptime(str(cabPresupuesto.fecha_presupuesto),'%Y-%m-%d').strftime('%Y-%m-%d')
    # Se envia el formulario
    if request.method == 'POST':
        # Obtener la recepcion
        recepcion_list = request.POST.get('id_recepcion_select', '')
        #obterner el estado
        filename = ""
        estado_presupuesto = request.POST.get('condicion_presupuesto', '')
        # Obtener fecha
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        recepcion = RecepcionVehiculo.objects.get(id=recepcion_list)
        recepcion.estado = estado_presupuesto
        recepcion.save()
        cabPresupuesto.recepcion_vehiculo = recepcion
        cabPresupuesto.fecha_presupuesto = fecha
        cabPresupuesto.save()

        lista_detalles = json.loads(request.POST.get('detalle', ''))
        borrar_detalle = True
        for detallePresupuesto in detPresupuesto:
            borrar_detalle = True
            for key in lista_detalles:
                id_presup = int(lista_detalles[key]['id_detalle'])
                if detallePresupuesto.id == id_presup:
                    detallePresupuesto.cantidad = lista_detalles[key]['cantidad']
                    detallePresupuesto.precio_unitario = lista_detalles[key]['monto']
                    borrar_detalle = False
                    detallePresupuesto.save()
                    break
            if borrar_detalle == True:
                detallePresupuesto.delete()

        for key in lista_detalles:
            id_oc = int(lista_detalles[key]['id_detalle'])
            if id_oc ==0:
                detalle = PresupuestoDet()
                nombre_producto = lista_detalles[key]['descripcion']
                producto = Producto.objects.get(descripcion__exact=nombre_producto)
                detalle.presupuesto_cab = cabPresupuesto
                detalle.producto = producto
                detalle.cantidad = lista_detalles[key]['cantidad']
                detalle.precio_unitario = int(lista_detalles[key]['monto'])
                detalle.save()
        messages.add_message(request, messages.INFO, 'Se actualizaron los datos')
        return HttpResponseRedirect(reverse('presupuesto_listado'))

    else:
        c = {
            'cabecera_pre': cabPresupuesto,
            'detalles_pre': detPresupuesto,
            'fecha_presupuesto': fecha_presupuesto
        }
        return HttpResponse(t.render(c))

@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Funcion para eliminar una orden de compra desde el listado.
def eliminarPresupuesto(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id_eliminar')
        try:
            cabPresupuesto = PresupuestoCab.objects.get(pk=int(id))
            detPresupuesto = PresupuestoDet.objects.filter(presupuesto_cab__id=cabPresupuesto.id)
            for detallepre in detPresupuesto:
                detallepre.delete()

            cabPresupuesto.delete()
            messages.add_message(request, messages.INFO, 'Orden de Compra eliminada')
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR,
                                 'No se puede eliminar la Orden de Compra')
        return HttpResponseRedirect(reverse('oc_listado'))