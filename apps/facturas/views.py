import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods
from sismec.dao import factura_dao
from apps.clientes.models import Cliente
from apps.compras.models import OrdenCompraCab, OrdenCompraDet
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
# Agregar un factura Compra
from apps.facturas.models import MovimientoCabecera, MovimientoDetalle, CobroPagomodels, Timbrado
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor
from apps.ventas.models import PresupuestoCab, PresupuestoDet
from apps.recepcion.models import RecepcionVehiculo
from apps.facturas.factura_venta_reporte import imprimir_factura_venta_jasper

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from sismec.configuraciones import ROW_PER_PAGE


@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def agregarFacturaCompra(request, id):
    t = loader.get_template('facturas/agregar.html')
    cabeceraOc = OrdenCompraCab.objects.get(pk=id)
    detallesOc = OrdenCompraDet.objects.filter(compra_cab__id=cabeceraOc.id)
    fecha_pedido = datetime.strptime(str(cabeceraOc.fecha_pedido), '%Y-%m-%d').strftime('%Y-%m-%d')
    if request.method == 'POST':
        cabeceraOc.estado = "FACTURADO"
        cabeceraOc.save()
        # Obtener tipo de movimiento
        tipo_movimiento = request.POST.get('tipo_movimiento', '')
        # Obtener el proveedor
        proveedor_list = request.POST.get('id_prov_client_select', '')
        # Obtener condicion de compra
        condicion_compra = request.POST.get('condicion_compra', '')
        # Obtener timbrado
        timbrado = request.POST.get('timbrado', '')
        # Obtener fecha ini timbrado
        fecha_ini_timbrado = datetime.strptime(request.POST.get('fecha_ini_timbrado', ''), "%Y-%m-%d")
        # Obtener fecha fin timbrado
        fecha_fin_timbrado = datetime.strptime(request.POST.get('fecha_fin_timbrado', ''), "%Y-%m-%d")
        # Obtener fecha emision de la factura
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        # Obtener numero factura
        numero_factura = request.POST.get('numero_factura', '')
        #TOTALES
        # precio_uni por cantidad
        sub_exentas = int(request.POST.get('sub_exentas', ''))
        # precio_uni por cantidad
        sub_iva5 = int(request.POST.get('sub_iva5', ''))
        # precio_uni por cantidad
        sub_iva10 = int(request.POST.get('sub_iva10', ''))
        # subtotal_iva5 / 21
        total_iva5 = int(request.POST.get('total_iva5', ''))
        # subtotal_iva10/ 11
        total_iva10 = int(request.POST.get('total_iva10', ''))

        plazo_dias = int(request.POST.get('nro_cuota', ''))

        try:
            for proveedor_id in proveedor_list:
                proveedor = Proveedor.objects.get(id=proveedor_id)

            # Verificar si ya existe una fc con el mismo proveedor,numero de factura ytimbrado
            object_list = MovimientoCabecera.objects.filter(timbrado__iexact=timbrado,
                                                            numero_factura__iexact=numero_factura,
                                                            proveedor_id=proveedor.id).count()
            if(object_list > 0):
                status = 500
                mensajes = 'Ya existe una factura con el mismo proveedor, numero factura y timbrado'
                json_response = {'status': status, 'mensajes': mensajes}
                cabeceraOc.estado = "CONFIRMADO"
                cabeceraOc.save()
                return HttpResponse(json.dumps(json_response), content_type='application/json')
            else:
                movimiento = MovimientoCabecera()
                movimiento.fecha_emision = fecha
                movimiento.proveedor = proveedor
                movimiento.numero_factura = numero_factura
                movimiento.tipo_movimiento = tipo_movimiento
                movimiento.tipo_factura = condicion_compra
                movimiento.plazo_dias = plazo_dias
                movimiento.monto_total = sub_exentas + sub_iva10 + sub_iva5
                if movimiento.tipo_factura == 'Contado':
                    movimiento.estado = MovimientoCabecera.COMPLETADO
                    movimiento.saldo = 0
                else:
                    movimiento.estado = MovimientoCabecera.PENDIENTE
                    movimiento.saldo = movimiento.monto_total
                    #movimiento.fecha_vencimiento = fecha_vencimiento
                movimiento.grav10_total = sub_iva10 - total_iva10
                movimiento.grav5_total = sub_iva5 - total_iva5
                movimiento.iva10_total = sub_iva10
                movimiento.iva5_total = sub_iva5
                movimiento.timbrado = timbrado
                movimiento.fecha_inicio = fecha_ini_timbrado
                movimiento.fecha_fin = fecha_fin_timbrado
                movimiento.orden_compra = cabeceraOc
                movimiento.save()
                #agregar detalles de la factura
                lista_detalles = json.loads(request.POST.get('detalle_factura', ''))
                for key in lista_detalles:
                    detalle = MovimientoDetalle()
                    id_producto = lista_detalles[key]['id_producto']
                    producto = Producto.objects.get(id=id_producto)
                    cantidad_item = int(lista_detalles[key]['cantidad_item'])
                    precio_uni = lista_detalles[key]['precio_uni']
                    exentas = lista_detalles[key]['exentas']
                    iva_5 = lista_detalles[key]['iva_5']
                    iva_10 = lista_detalles[key]['iva_10']
                    detalle.compra_cab = id
                    detalle.cantidad = cantidad_item
                    detalle.producto = producto
                    detalle.precio_unitario = precio_uni
                    detalle.exentas = exentas
                    detalle.iva5 = iva_5
                    detalle.iva10 = iva_10
                    detalle.movimiento_cab = movimiento
                    detalle.save()
                    #SE ACTUALIZA EL STOCK DE PRODUCTO
                    cantidad_producto = int(producto.cantidad) + int(detalle.cantidad)
                    producto.cantidad = cantidad_producto
                    producto.save()
                #ACTUALIZAR ESTADO DE OC

                status = 200
                mensajes = 'Movimiento agregado exitosamente'
                json_response = {'status' : status, 'mensajes' : mensajes}
                return HttpResponse(json.dumps(json_response), content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            status = 500
            mensajes = 'Ha ocurrido un error'
            json_response = {'status': status, 'mensajes': mensajes}
            return HttpResponse(json.dumps(json_response), content_type='application/json')
    else:
        c = {
            'cabecera_oc': cabeceraOc,
            'detalles_oc': detallesOc,
            'fecha_pedido': fecha_pedido
        }
    return HttpResponse(t.render(c, request))


@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def generarFacturaVenta(request, id):
    t = loader.get_template('facturas/agregar_venta.html')
    cabPresupuesto = PresupuestoCab.objects.get(pk=id)
    detPresupuesto = PresupuestoDet.objects.filter(presupuesto_cab__id=cabPresupuesto.id)
    timbrado_bd = Timbrado.objects.latest('id')
    fecha_ini_tim = datetime.strptime(str(timbrado_bd.fecha_inicio),'%Y-%m-%d').strftime('%Y-%m-%d')
    fecha_fin_tim = datetime.strptime(str(timbrado_bd.fecha_fin),'%Y-%m-%d').strftime('%Y-%m-%d')
    nro_fact = timbrado_bd.ultima_factura + 1
    if request.method == 'POST':
        cabPresupuesto.estado = "FACTURADO"
        cabPresupuesto.save()
        # Obtener tipo de movimiento
        tipo_movimiento = request.POST.get('tipo_movimiento', '')
        # Obtener el cliente
        cliente_list = request.POST.get('id_prov_client_select', '')
        # Obtener condicion de compra
        condicion_compra = request.POST.get('condicion_compra', '')
        # Obtener timbrado
        timbrado = request.POST.get('timbrado', '')
        # Obtener fecha ini timbrado
        fecha_ini_timbrado = datetime.strptime(request.POST.get('fecha_ini_timbrado', ''), "%Y-%m-%d")
        # Obtener fecha fin timbrado
        fecha_fin_timbrado = datetime.strptime(request.POST.get('fecha_fin_timbrado', ''), "%Y-%m-%d")
        # Obtener fecha emision de la factura
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        # Obtener numero factura
        numero_factura = request.POST.get('numero_factura', '')
        #TOTALES
        # precio_uni por cantidad
        sub_exentas = int(request.POST.get('sub_exentas', ''))
        # precio_uni por cantidad
        sub_iva5 = int(request.POST.get('sub_iva5', ''))
        # precio_uni por cantidad
        sub_iva10 = int(request.POST.get('sub_iva10', ''))
        # subtotal_iva5 / 21
        total_iva5 = int(request.POST.get('total_iva5', ''))
        # subtotal_iva10/ 11
        total_iva10 = int(request.POST.get('total_iva10', ''))

        plazo_dias = int(request.POST.get('nro_cuota', ''))

        #fecha_vencimiento = datetime.strptime(request.POST.get('fecha_vencimiento', ''), "%Y-%m-%d")
        try:
            for cliente_id in cliente_list:
                cliente = Cliente.objects.get(id=cliente_id)
            #Recepcion de Vehiculo asociado
            recepcion = RecepcionVehiculo()
            recepcion = RecepcionVehiculo.objects.get(pk=cabPresupuesto.recepcion_vehiculo.id)

            movimiento = MovimientoCabecera()
            movimiento.fecha_emision = fecha
            movimiento.cliente = cliente
            movimiento.numero_factura = numero_factura
            movimiento.tipo_movimiento = tipo_movimiento
            movimiento.tipo_factura = condicion_compra
            movimiento.plazo_dias = plazo_dias
            movimiento.monto_total = sub_exentas + sub_iva10 + sub_iva5
            if movimiento.tipo_factura == 'Contado':
                movimiento.estado = MovimientoCabecera.COMPLETADO
                movimiento.saldo = 0
                recepcion.estado = RecepcionVehiculo.FACTURADO
                recepcion.save()
            else:
                movimiento.estado = MovimientoCabecera.PENDIENTE
                movimiento.saldo = movimiento.monto_total
                recepcion.estado = RecepcionVehiculo.PENDIENTEDEPAGO
                recepcion.save()
                #movimiento.fecha_vencimiento = fecha_vencimiento

            movimiento.grav10_total = sub_iva10 - total_iva10
            movimiento.grav5_total = sub_iva5 - total_iva5
            movimiento.iva10_total = sub_iva10
            movimiento.iva5_total = sub_iva5
            movimiento.timbrado = timbrado
            movimiento.fecha_inicio = fecha_ini_timbrado
            movimiento.fecha_fin = fecha_fin_timbrado
            movimiento.presupuesto = cabPresupuesto
            movimiento.save()
            # se actualiza ultimo numero de factura del timbrado
            timbrado_bd.ultima_factura = int(numero_factura)
            timbrado_bd.save()
            #agregar detalles de la factura
            lista_detalles = json.loads(request.POST.get('detalle_factura', ''))
            for key in lista_detalles:
                detalle = MovimientoDetalle()
                id_producto = lista_detalles[key]['id_producto']
                producto = Producto.objects.get(id=id_producto)
                cantidad_item = int(lista_detalles[key]['cantidad_item'])
                precio_uni = lista_detalles[key]['precio_uni']
                exentas = lista_detalles[key]['exentas']
                iva_5 = lista_detalles[key]['iva_5']
                iva_10 = lista_detalles[key]['iva_10']
                #detalle.compra_cab = id
                detalle.cantidad = cantidad_item
                detalle.producto = producto
                detalle.precio_unitario = precio_uni
                detalle.exentas = exentas
                detalle.iva5 = iva_5
                detalle.iva10 = iva_10
                detalle.movimiento_cab = movimiento
                detalle.save()
                #SE ACTUALIZA EL STOCK DE PRODUCTO
                cantidad_producto = int(producto.cantidad) - int(detalle.cantidad)
                producto.cantidad = cantidad_producto
                producto.save()
            #ACTUALIZAR ESTADO DE OC
            mov_id = movimiento.id
            status = 200
            mensajes = 'Movimiento agregado exitosamente'
            json_response = {'status' : status, 'mensajes' : mensajes, 'id': mov_id}
            return HttpResponse(json.dumps(json_response), content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            status = 500
            mensajes = 'Ha ocurrido un error'
            json_response = {'status': status, 'mensajes': mensajes}
            return HttpResponse(json.dumps(json_response), content_type='application/json')
    else:
        c = {
            'cabecera_pre': cabPresupuesto,
            'detalles_pre': detPresupuesto,
            'timbrado': timbrado_bd,
            'fecha_ini_tim': fecha_ini_tim,
            'fecha_fin_tim': fecha_fin_tim,
            'nro_fact': nro_fact
        }
        
    return HttpResponse(t.render(c, request))

@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
def imprimirFacturaVenta(request):
    nro_movimiento=request.GET.get("nro_movimiento",'')
    factura_generada=imprimir_factura_venta_jasper(nro_movimiento)
    params={
        'reporte_pdf': factura_generada
    }
    ##return HttpResponse(t.render(params,request))
    ##return HttpResponse(factura_generada,content_type='application/pdf')
    fs = FileSystemStorage()
    if fs.exists(factura_generada):
        with fs.open(factura_generada) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=reporte_estado_cuenta.pdf;charset=utf-8'
            return response




@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar facturas ventas.
def listarFV(request):
    t = loader.get_template('facturas/listado_fventas.html')
    if request.method == 'GET':
        data = request.GET

        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'cliente': data.get('cliente_select', ''), 'fecha': data.get('fecha', ''),
                   'estado': data.get('estado', '')}

        query_param_list = [filtros['row_per_page'], filtros['cliente'], filtros['fecha'], filtros['estado']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = factura_dao.getFacturaVentaFiltro(filtros)

        c = {
            'object_list': object_list,
            'pagination': pagination,
            'filtros': filtros,
            'query_params': query_params
        }
        return HttpResponse(t.render(c, request))

@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar facturas compras.
def listarFC(request):
    t = loader.get_template('facturas/listado_fcompras.html')
    if request.method == 'GET':
        data = request.GET

        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'proveedor': data.get('proveedor_select', ''), 'fecha': data.get('fecha', ''),
                   'estado': data.get('estado', '')}

        query_param_list = [filtros['row_per_page'], filtros['proveedor'], filtros['fecha'], filtros['estado']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = factura_dao.getFacturaCompraFiltro(filtros)

        c = {
            'object_list': object_list,
            'pagination': pagination,
            'filtros': filtros,
            'query_params': query_params
        }
        return HttpResponse(t.render(c, request))

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def cobrarFacturaVenta(request, id):
    t = loader.get_template('facturas/cobrar_venta.html')
    cabMovimiento = MovimientoCabecera.objects.get(pk=id)
    detPresupuesto = PresupuestoDet.objects.filter(presupuesto_cab__id=cabMovimiento.id)
    if request.method == 'POST':
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        forma_pago = request.POST.get('forma_pago', '')
        monto_pagado = int(request.POST.get('monto_pagado', ''))
        saldo_Actual = cabMovimiento.saldo - monto_pagado
        cobro_pago = CobroPagomodels()
        cobro_pago.movimiento_cab = cabMovimiento
        cobro_pago.fecha = fecha
        cobro_pago.forma_pago = forma_pago
        cobro_pago.monto = monto_pagado
        cobro_pago.estado = CobroPagomodels.ACTIVO
        cobro_pago.tipo = CobroPagomodels.COBRO
        cobro_pago.dato_adicional = request.POST.get('dato_adicional', '')
        cobro_pago.nro_recibo = request.POST.get('numero_recibo', '')
        cobro_pago.save()

        recepcion = RecepcionVehiculo()
        recepcion = RecepcionVehiculo.objects.get(pk=cabMovimiento.presupuesto.recepcion_vehiculo.id)

        cabMovimiento.saldo = saldo_Actual
        if saldo_Actual > 0:
            recepcion.estado = RecepcionVehiculo.PENDIENTEDEPAGO
            cabMovimiento.estado = MovimientoCabecera.PENDIENTE
        else:
            recepcion.estado = RecepcionVehiculo.PAGADO
            cabMovimiento.estado = MovimientoCabecera.COMPLETADO
        recepcion.save()
        cabMovimiento.save()

        # ACTUALIZAR ESTADO DE OC
        status = 200
        mensajes = 'Cobro agregado exitosamente'
        json_response = {'status': status, 'mensajes': mensajes}
        return HttpResponse(json.dumps(json_response), content_type='application/json')
    else:
        c = {
            'cabecera_mov': cabMovimiento
        }
    return HttpResponse(t.render(c, request))

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def pagarFacturaCompra(request, id):
    t = loader.get_template('facturas/pagar_compra.html')
    cabMovimiento = MovimientoCabecera.objects.get(pk=id)
    if request.method == 'POST':
        fecha = datetime.strptime(request.POST.get('fecha', ''), "%Y-%m-%d")
        forma_pago = request.POST.get('forma_pago', '')
        monto_pagado = int(request.POST.get('monto_pagado', ''))
        saldo_Actual = cabMovimiento.saldo - monto_pagado
        cobro_pago = CobroPagomodels()
        cobro_pago.movimiento_cab = cabMovimiento
        cobro_pago.fecha = fecha
        cobro_pago.forma_pago = forma_pago
        cobro_pago.monto = monto_pagado
        cobro_pago.estado = CobroPagomodels.ACTIVO
        cobro_pago.tipo = CobroPagomodels.PAGO
        cobro_pago.dato_adicional = request.POST.get('dato_adicional', '')
        cobro_pago.nro_recibo = request.POST.get('numero_recibo', '')
        cobro_pago.save()

        cabMovimiento.saldo = saldo_Actual
        if saldo_Actual > 0:
            cabMovimiento.estado = MovimientoCabecera.PENDIENTE
        else:
            cabMovimiento.estado = MovimientoCabecera.COMPLETADO
        cabMovimiento.save()

        # ACTUALIZAR ESTADO DE OC
        status = 200
        mensajes = 'Pago agregado exitosamente'
        json_response = {'status': status, 'mensajes': mensajes}
        return HttpResponse(json.dumps(json_response), content_type='application/json')
    else:
        c = {
            'cabecera_mov': cabMovimiento
        }
    return HttpResponse(t.render(c, request))