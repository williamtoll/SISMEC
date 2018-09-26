from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods
from apps.compras.models import OrdenCompraCab, OrdenCompraDet

# Agregar un factura Compra
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def agregarFacturaCompra(request, id):
    t = loader.get_template('facturas/agregar.html')
    cabeceraOc = OrdenCompraCab.objects.get(pk=id)
    cabeceraOc.fecha_pedido = cabeceraOc.fecha_pedido.strftime("%d/%m/%Y")
    detallesOc = OrdenCompraDet.objects.filter(compra_cab__id=cabeceraOc.id)
    c = {
        'cabecera_oc': cabeceraOc,
        'detalles_oc': detallesOc
    }
    return HttpResponse(t.render(c, request))
