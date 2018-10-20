import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template import loader
from datetime import datetime
from apps.clientes.models import Cliente
from apps.principal.common_functions import generar_codigo
from apps.recepcion.forms import RecepcionVehiculoForm
from apps.recepcion.models import Marca, Modelo, RecepcionVehiculo
from sismec.configuraciones import ROW_PER_PAGE
from sismec.utils import custom_permission_required
from django.contrib import messages
from django.urls import NoReverseMatch, reverse
from sismec.dao import recepcion_dao


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
                form.instance.codigo_recepcion = generar_codigo()
                form.instance.fecha_recepcion =fecha_recepcion
                form.instance.año = int(año)
                form.save()
                messages.add_message(request, messages.INFO, 'Recepcion de vehiculo agregada exitosamente')
                return HttpResponseRedirect(reverse('recepcion_listado'))
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

@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar PRODUCTOS existentes.
def listarRecepcion(request):
    t = loader.get_template('recepcion/listado.html')
    if request.method == 'GET':
        data = request.GET

        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'cliente': data.get('cliente_select', ''), 'fecha_recepcion': data.get('fecha_recepcion', ''),
                   'estado': data.get('estado', '')}

        query_param_list = [filtros['row_per_page'], filtros['cliente'], filtros['fecha_recepcion']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = recepcion_dao.getRecepcionFiltro(filtros)

        c = {
            'object_list': object_list,
            'pagination': pagination,
            'filtros': filtros,
            'query_params': query_params
        }
        return HttpResponse(t.render(c, request))


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Funcion que muestra el detalle de un autor en particular.
def detalleRecepcion(request, id):
    t = loader.get_template('recepcion/detalle.html')
    object_list = RecepcionVehiculo.objects.get(pk=id)
    # Se envia el formulario
    if request.method == 'POST':
        data = request.POST
        if data.get('boton_guardar'):
            form =RecepcionVehiculoForm(data, instance=object_list)
            marca = request.POST.getlist('marca_vehiculo_select', '')
            modelo = request.POST.getlist('modelo_vehiculo_select', '')
            año = request.POST.get('año', '')
            fecha_recepcion = datetime.strptime(request.POST.get('fecha_recepcion', ''), "%Y-%m-%d")
            cliente = request.POST.getlist('cliente_select', '')
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
                messages.add_message(request, messages.INFO, 'Se actualizaron los datos')
                return HttpResponseRedirect(reverse('recepcion_listado'))
        elif data.get('boton_borrar'):
            try:
                obj = RecepcionVehiculo.objects.get(pk=id)
                obj.delete()
                messages.add_message(request, messages.INFO, 'Recepción eliminada')
                return HttpResponseRedirect(reverse('recepcion_listado'))
            except Exception as e:
                traceback.print_exc(e.args)
                messages.add_message(request, messages.ERROR,
                                     'No se puede eliminar la Recepción.')
                return HttpResponseRedirect(reverse('frontend_home') + 'recepcion/detalle/%s' % id)
    else:
        form = RecepcionVehiculoForm(instance=object_list)
        c = {
            'object_list': object_list,
            'form': form
        }
        return HttpResponse(t.render(c, request))

@require_http_methods(["POST"])
@login_required(login_url='/sismec/login/')
# Funcion para eliminar un autor desde el listado.
def eliminarRecepcion(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id_eliminar')
        try:
            obj = RecepcionVehiculo.objects.get(pk=id)
            obj.delete()
            messages.add_message(request, messages.INFO, 'Recepción eliminada')
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR,
                                 'No se puede eliminar la Recepción.')
        return HttpResponseRedirect(reverse('recepcion_listado'))