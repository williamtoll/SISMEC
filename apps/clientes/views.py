import traceback

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from apps.clientes.forms import ClienteForm
from apps.clientes.models import Cliente
from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import cliente_dao
from django.contrib import messages

# listar clientes
from sismec.utils import custom_permission_required


@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar Clientes existentes.
def listarCliente(request):
    t = loader.get_template('clientes/listado.html')
    if request.method == 'GET':
        data = request.GET
        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'search': data.get('search', '')}

        query_param_list = [filtros['row_per_page'], filtros['search']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = cliente_dao.getClienteFiltro(filtros)

        c = {
            'object_list': object_list,
            'pagination': pagination,
            'filtros': filtros,
            'query_params': query_params
        }
        return HttpResponse(t.render(c, request))



@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('clientes.add_cliente')
# # Funcion para agregar un cliente.
def agregarCliente(request):
    t = loader.get_template('clientes/agregar.html')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Cliente agregado exitosamente')
                return HttpResponseRedirect(reverse('clientes_listado'))
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
        form = ClienteForm()
        c = {'form': form}
        return HttpResponse(t.render(c, request))


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
# Funcion que muestra el detalle de un cliente en particular.
def detalleCliente(request, id):
    t = loader.get_template('clientes/detalle.html')
    object_list = Cliente.objects.get(pk=id)
    # Se envia el formulario
    if request.method == 'POST':
        data = request.POST
        if data.get('boton_guardar'):
            form =ClienteForm(data, instance=object_list)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Se actualizaron los datos')
                return HttpResponseRedirect(reverse('clientes_listado'))
        elif data.get('boton_borrar'):
            try:
                obj = Cliente.objects.get(pk=id)
                obj.delete()
                messages.add_message(request, messages.INFO, 'Cliente eliminado')
                return HttpResponseRedirect(reverse('clientes_listado'))
            except Exception as e:
                traceback.print_exc(e.args)
                messages.add_message(request, messages.ERROR,
                                     'No se puede eliminar el Cliente.')
                return HttpResponseRedirect(reverse('frontend_home') + 'clientes/detalle/%s' % id)
    else:
        form = ClienteForm(instance=object_list)
        c = {
            'object_list': object_list,
            'form': form
        }
        return HttpResponse(t.render(c, request))

@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('clientes.delete_cliente')
# Funcion para eliminar un autor desde el listado.
def eliminarCliente(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id_eliminar')
        try:
            obj = Cliente.objects.get(pk=id)
            obj.delete()
            messages.add_message(request, messages.INFO, 'Cliente eliminado')
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR,
                                 'No se puede eliminar el Cliente.')
        return HttpResponseRedirect(reverse('clientes_listado'))