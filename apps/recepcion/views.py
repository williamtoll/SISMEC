import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template import loader
from datetime import datetime

from apps.clientes.models import Cliente
from apps.recepcion.forms import RecepcionVehiculoForm
from apps.recepcion.models import Marca, Modelo
from sismec.utils import custom_permission_required
from django.contrib import messages
from django.urls import NoReverseMatch, reverse


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('productos.add_producto')
# # Funcion para agregar un producto.
def agregarRecepcionVehiculo(request):
    t = loader.get_template('recepcion/agregar.html')
    if request.method == 'POST':
        form = RecepcionVehiculoForm(request.POST)
        marca = request.POST.getlist('marca_vehiculo_select', '')
        modelo = request.POST.getlist('modelo_vehiculo_select', '')
        año = request.POST.get('año', '')
        fecha_recepcion = datetime.strptime(request.POST.get('fecha_recepcion', ''), "%Y-%m-%d")
        cliente = request.POST.getlist('cliente_select', '')
        try:
            if form.is_valid():
                for m in marca:
                    marca_r = Marca.objects.get(id=m)
                    form.instance.marca = marca_r
                for mod in modelo:
                    modelo_r = Modelo.objects.get(id=mod)
                    form.instance.modelo = modelo_r
                for cli in cliente:
                    cliente_r = Cliente.objects.get(id=cli)
                    form.instance.cliente = cliente_r
                form.instance.fecha_recepcion =fecha_recepcion
                form.instance.año = int(año)
                form.save()
                messages.add_message(request, messages.INFO, 'Recepcion de vehiculo agregada exitosamente')
                return HttpResponseRedirect(reverse('frontend_home'))
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                c = {'form': form}
                return HttpResponse(t.render(c, request))
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR, e.args)
            c = {'form': form}
            return HttpResponse(t.render(c, request))
    else:
        form = RecepcionVehiculoForm()
        c = {'form': form}
        return HttpResponse(t.render(c, request))