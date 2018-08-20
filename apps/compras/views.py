from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.http import require_http_methods



# Para crear una orden de compra
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# # Funcion para agregar un cliente.
def agregarOC(request):
    t = loader.get_template('compras/agregar_oc.html')
    c = {}
    return HttpResponse(t.render(c, request))
