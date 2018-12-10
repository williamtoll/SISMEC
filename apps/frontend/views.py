from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your def index(request):
from apps.recepcion.models import RecepcionVehiculo


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def index(request):
    t = loader.get_template('index.html')
    vehiculos_totales = RecepcionVehiculo.objects.count()
    vehiculos_entregados = RecepcionVehiculo.objects.filter(estado__iexact='FACTURADO').count()
    vehiculos_pendientes = RecepcionVehiculo.objects.filter(estado__iexact='RECIBIDO').count()
    object_list = RecepcionVehiculo.objects.filter(estado__iexact='RECIBIDO')
    c = {
        'object_list' : object_list,
        'vehiculos_totales' : vehiculos_totales,
        'vehiculos_entregados' : vehiculos_entregados,
        'vehiculos_pendientes' : vehiculos_pendientes
    }
    return HttpResponse(t.render(c, request))