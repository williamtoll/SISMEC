from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader
from django.contrib import messages
# Create your views here.
def index(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            t = loader.get_template('principal/dashboard.html')
            c = {}
            return HttpResponse(t.render(c, request))
        else:
            return HttpResponseRedirect(reverse('frontend_login'))
    else:
        return HttpResponseRedirect(reverse('frontend_login'))


def alertsservice(request):
    data = request.GET
    mensaje = data.get('mensajes', '')
    status = data.get('status', '')
    if status == "200":
        messages.add_message(request, messages.INFO, mensaje)
        return HttpResponseRedirect(reverse('oc_listado'))
    else:
        messages.add_message(request, messages.ERROR, mensaje)
        return HttpResponseRedirect(reverse('oc_listado'))

def alertsserviceVentas(request):
    data = request.GET
    mensaje = data.get('mensajes', '')
    status = data.get('status', '')
    if status == "200":
        messages.add_message(request, messages.INFO, mensaje)
        return HttpResponseRedirect(reverse('presupuesto_listado'))
    else:
        messages.add_message(request, messages.ERROR, mensaje)
        return HttpResponseRedirect(reverse('presupuesto_listado'))

def alertsserviceCobros(request):
    data = request.GET
    mensaje = data.get('mensajes', '')
    status = data.get('status', '')
    if status == "200":
        messages.add_message(request, messages.INFO, mensaje)
        return HttpResponseRedirect(reverse('factura_venta_listado'))
    else:
        messages.add_message(request, messages.ERROR, mensaje)
        return HttpResponseRedirect(reverse('factura_venta_listado'))

def alertsservicePagos(request):
    data = request.GET
    mensaje = data.get('mensajes', '')
    status = data.get('status', '')
    if status == "200":
        messages.add_message(request, messages.INFO, mensaje)
        return HttpResponseRedirect(reverse('factura_compra_listado'))
    else:
        messages.add_message(request, messages.ERROR, mensaje)
        return HttpResponseRedirect(reverse('factura_compra_listado'))