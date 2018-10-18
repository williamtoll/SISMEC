import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime, time
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from apps.compras.models import OrdenCompraCab, OrdenCompraDet
from django.contrib import messages
from django.urls import reverse
from sismec.dao import compra_dao
import json
from sismec.configuraciones import ROW_PER_PAGE
from sismec.utils import custom_permission_required
from base64 import decodestring
import base64
from sismec.configuraciones import PRESUPUESTO_DIR

# Para crear una orden de compra
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('compras.add_ordencompracab')
# # Funcion para agregar una orden de compra.
def agregarOC(request):
    t = loader.get_template('compras/agregar_oc.html')
    if request.method == 'POST':
        # Obtener el proveedor
        proveedor_list = request.POST.get('id_proveedor_select', '')

        # Obtener fecha
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")

        try:
            for proveedor_id in proveedor_list:
                proveedor = Proveedor.objects.get(id=proveedor_id)
            nuevaOC = OrdenCompraCab()
            #nuevaOC.fecha_pedido = fecha
            nuevaOC.proveedor= proveedor
            nuevaOC.estado = OrdenCompraCab.PENDIENTE
            nuevaOC.fecha_pedido = fecha
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

@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar PRODUCTOS existentes.
def listarOC(request):
    t = loader.get_template('compras/listado.html')
    if request.method == 'GET':
        data = request.GET

        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'proveedor': data.get('proveedor_select', ''), 'fecha': data.get('fecha', ''),
                   'estado': data.get('estado', '')}

        query_param_list = [filtros['row_per_page'], filtros['proveedor'], filtros['fecha'], filtros['estado']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = compra_dao.getOCFiltro(filtros)

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
def detalleOC(request, id):
    t = loader.get_template('compras/detalle.html')
    cabeceraOc = OrdenCompraCab.objects.get(pk = int(id))
    detallesOc = OrdenCompraDet.objects.filter(compra_cab__id=cabeceraOc.id)
    fecha_pedido = datetime.strptime(str(cabeceraOc.fecha_pedido),'%Y-%m-%d').strftime('%Y-%m-%d')
    # Se envia el formulario
    if request.method == 'POST':
        # Obtener el proveedor
        proveedor_list = request.POST.get('id_proveedor_select', '')
        #obterner el estado
        filename = ""
        estado_compra = request.POST.get('condicion_compra', '')
        if (str(request.POST.get('presupuesto_path', '')).__len__() != 0):
            image = str(request.POST.get('presupuesto_path', '')).split(",")
            b64_string = image[1]
            b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
            imgdata = base64.b64decode(b64_string)
            filename = str(PRESUPUESTO_DIR + str(cabeceraOc.id) + '_' + str(datetime.now().microsecond) + '.jpg')
            with open(filename, 'wb') as f:
                f.write(imgdata)
        # Obtener fecha
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        for proveedor_id in proveedor_list:
            proveedor = Proveedor.objects.get(id=proveedor_id)
        cabeceraOc.proveedor = proveedor
        cabeceraOc.estado = request.POST.get('condicion_compra', '')
        cabeceraOc.fecha_pedido = fecha
        cabeceraOc.presupuesto_compra = filename
        cabeceraOc.save()

        lista_detalles = json.loads(request.POST.get('detalle', ''))
        borrar_detalle = True
        for detallecompra in detallesOc:
            borrar_detalle = True
            for key in lista_detalles:
                id_oc = int(lista_detalles[key]['id_detalle'])
                if detallecompra.id == id_oc:
                    detallecompra.cantidad = lista_detalles[key]['cantidad']
                    detallecompra.monto = lista_detalles[key]['monto']
                    borrar_detalle = False
                    detallecompra.save()
                    break
            if borrar_detalle == True:
                detallecompra.delete()

        for key in lista_detalles:
            id_oc = int(lista_detalles[key]['id_detalle'])
            if id_oc ==0:
                detalle = OrdenCompraDet()
                nombre_producto = lista_detalles[key]['descripcion']
                producto = Producto.objects.get(descripcion__exact=nombre_producto)
                detalle.compra_cab = detallecompra.compra_cab
                detalle.producto = producto
                detalle.cantidad = lista_detalles[key]['cantidad']
                detalle.monto = lista_detalles[key]['monto']
                detalle.save()
        messages.add_message(request, messages.INFO, 'Se actualizaron los datos')
        return HttpResponseRedirect(reverse('oc_listado'))

    else:
        c = {
            'cabecera_oc': cabeceraOc,
            'detalles_oc': detallesOc,
            'fecha_pedido': fecha_pedido
        }
        return HttpResponse(t.render(c))

@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Funcion para eliminar una orden de compra desde el listado.
def eliminarOC(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id_eliminar')
        try:
            cabeceraOc = OrdenCompraCab.objects.get(pk=int(id))
            detallesOc = OrdenCompraDet.objects.filter(compra_cab__id=cabeceraOc.id)
            for detallecompra in detallesOc:
                detallecompra.delete()

            cabeceraOc.delete()
            messages.add_message(request, messages.INFO, 'Orden de Compra eliminada')
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR,
                                 'No se puede eliminar la Orden de Compra')
        return HttpResponseRedirect(reverse('oc_listado'))