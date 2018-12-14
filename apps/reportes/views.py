from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from apps.reportes.lista_reportes import estado_cuenta_cliente, productos_mas_vendidos, movimientos_compras, \
    movimientos_ventas, cuentas_a_pagar, ventas_mensuales, compras_mensuales


@csrf_exempt
@require_http_methods(["GET","POST"])
@login_required(login_url='/sismec/login/')
# Funcion p existentes.
def estadoCuentacliente(request):
    t = loader.get_template('reportes/estado_cuenta_cliente.html')
    c = {}
    if request.method=='POST':
        tipo_visualizacion=request.POST.get('tipo-visualizacion','')
        cliente=request.POST.get('cliente_select','');
        print("cliente")
        print(cliente)

        archivo_reporte = estado_cuenta_cliente(cliente,tipo_visualizacion)

        if tipo_visualizacion=='mostrar':
            params={
                'reporte_pdf': archivo_reporte
            }
            # return HttpResponse(t.render(params,request))
            ##return HttpResponse(archivo_reporte,content_type='application/pdf')
            fs = FileSystemStorage()
            if fs.exists(archivo_reporte):
                with fs.open(archivo_reporte) as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    response['Content-Disposition'] = 'inline;filename=reporte_estado_cuenta.pdf;charset=utf-8'
                    return response

        else:
            fs = FileSystemStorage()
            if fs.exists(archivo_reporte):
                with fs.open(archivo_reporte) as pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment;filename=reporte_estado_cuenta.pdf;charset=utf-8'
                    ##response['Content-Disposition'] = 'inline;filename=reporte_estado_cuenta.pdf;charset=utf-8'

                    # response = HttpResponse(content_type='application/pdf')
                    # response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format("reporte_estado_cuenta")
                    # response.write(pdf)
                    
                    return response
        
    return HttpResponse(t.render(c, request))


@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Reporte de Compras por meses
def productosMasVendidos(request):
    t = loader.get_template('reportes/productos_mas_vendidos.html')
    c = {}
    if request.method == 'POST':
        fecha_ini = datetime.strptime(request.POST.get('fecha_ini', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        reporte_generado = productos_mas_vendidos(fecha_ini,fecha_fin)

        params = {
            'reporte_pdf': reporte_generado
        }
        return HttpResponse(t.render(params, request))
    return HttpResponse(t.render(c, request))

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Reporte de Compras
def movimientosCompras(request):
    t = loader.get_template('reportes/movimientos_compras.html')
    c = {}
    if request.method == 'POST':
        fecha_ini = datetime.strptime(request.POST.get('fecha_ini', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        reporte_generado = movimientos_compras(fecha_ini,fecha_fin)

        params = {
            'reporte_pdf': reporte_generado
        }
        return HttpResponse(t.render(params, request))
    return HttpResponse(t.render(c, request))

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Reporte de Compras
def movimientosVentas(request):
    t = loader.get_template('reportes/movimientos_ventas.html')
    c = {}
    if request.method == 'POST':
        fecha_ini = datetime.strptime(request.POST.get('fecha_ini', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        reporte_generado = movimientos_ventas(fecha_ini,fecha_fin)

        params = {
            'reporte_pdf': reporte_generado
        }
        return HttpResponse(t.render(params, request))
    return HttpResponse(t.render(c, request))


@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Reporte de Cuentas a Pagar
def cuentasAPagar(request):
    t = loader.get_template('reportes/cuentas_a_pagar.html')
    c = {}
    if request.method == 'POST':
        fecha_ini = datetime.strptime(request.POST.get('fecha_ini', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin', ''),'%Y-%m-%d').strftime('%Y-%m-%d')
        reporte_generado = cuentas_a_pagar(fecha_ini,fecha_fin)

        params = {
            'reporte_pdf': reporte_generado
        }
        return HttpResponse(t.render(params, request))
    return HttpResponse(t.render(c, request))

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Reporte de Cuentas a Pagar
def ventasPorMes(request):
    t = loader.get_template('reportes/ventas_por_mes.html')
    c = {}
    if request.method == 'POST':
        reporte_generado = ventas_mensuales()

        params = {
            'reporte_pdf': reporte_generado
        }
        return HttpResponse(t.render(params, request))
    return HttpResponse(t.render(c, request))

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Reporte de Compras realizadas por mes
def comprasPorMes(request):
    t = loader.get_template('reportes/compras_por_mes.html')
    c = {}
    if request.method == 'POST':
        reporte_generado = compras_mensuales()

        params = {
            'reporte_pdf': reporte_generado
        }
        return HttpResponse(t.render(params, request))
    return HttpResponse(t.render(c, request))