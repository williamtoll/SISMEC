from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.template import loader

from apps.reportes.lista_reportes import estado_cuenta_cliente


@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion p existentes.
def estadoCuentacliente(request):
    t = loader.get_template('reportes/estado_cuenta_cliente.html')
    c = {}
    estado_cuenta_cliente()
    return HttpResponse(t.render(c, request))