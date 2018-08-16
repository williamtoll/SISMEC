import traceback

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from apps.proveedores.forms import ProveedorForm
from apps.proveedores.models import Proveedor
from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import proveedor_dao
from django.contrib import messages

# listar clientes
@require_http_methods(["GET"])
# Funcion para listar PROVEEDORES existentes.
def listarProveedor(request):
    if request.user.is_active:
        t = loader.get_template('proveedores/listado.html')
        if request.method == 'GET':
            data = request.GET
            filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                       'page': data.get('page', 1), 'search': data.get('search', '')}

            query_param_list = [filtros['row_per_page'], filtros['search']]

            query_params = '?row_per_page={}&search={}'.format(*query_param_list)
            object_list, pagination = proveedor_dao.getProveedorFiltro(filtros)

            c = {
                'object_list': object_list,
                'pagination': pagination,
                'filtros': filtros,
                'query_params': query_params
            }
            return HttpResponse(t.render(c, request))
    else:
        return HttpResponseRedirect(reverse('frontend_login'))



@require_http_methods(["GET", "POST"])
# # Funcion para agregar un PROVEEDOR.
def agregarProveedor(request):
    if request.user.is_active:
        t = loader.get_template('proveedores/agregar.html')
        if request.method == 'POST':
            form = ProveedorForm(request.POST)
            try:
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, 'Proveedor agregado exitosamente')
                    return HttpResponseRedirect(reverse('proveedores_listado'))
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
            form = ProveedorForm()
            c = {'form': form}
            return HttpResponse(t.render(c, request))
    else:
        return HttpResponseRedirect(reverse('login'))


@require_http_methods(["GET", "POST"])
# Funcion que muestra el detalle de un proveedor en particular.
def detalleProveedor(request, id):
    if request.user.is_active:
        t = loader.get_template('proveedores/detalle.html')
        object_list = Proveedor.objects.get(pk=id)
        # Se envia el formulario
        if request.method == 'POST':
            data = request.POST
            if data.get('boton_guardar'):
                form =ProveedorForm(data, instance=object_list)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.INFO, 'Se actualizaron los datos')
                    return HttpResponseRedirect(reverse('proveedores_listado'))
            elif data.get('boton_borrar'):
                try:
                    obj = Proveedor.objects.get(pk=id)
                    obj.delete()
                    messages.add_message(request, messages.INFO, 'Proveedor eliminado')
                    return HttpResponseRedirect(reverse('proveedores_listado'))
                except Exception as e:
                    traceback.print_exc(e.args)
                    messages.add_message(request, messages.ERROR,
                                         'No se puede eliminar el Cliente.')
                    return HttpResponseRedirect(reverse('frontend_home') + 'proveedores/detalle/%s' % id)
        else:
            form = ProveedorForm(instance=object_list)
            c = {
                'object_list': object_list,
                'form': form
            }
            return HttpResponse(t.render(c, request))
    else:
        return HttpResponseRedirect(reverse('login'))

# Funcion para eliminar un proveedor desde el listado.
def eliminarProveedor(request):
    if request.user.is_active:
        if request.method == 'POST':
            data = request.POST
            id = data.get('id_eliminar')
            try:
                obj = Proveedor.objects.get(pk=id)
                obj.delete()
                messages.add_message(request, messages.INFO, 'Proveedor eliminado')
            except Exception as e:
                traceback.print_exc(e.args)
                messages.add_message(request, messages.ERROR,
                                     'No se puede eliminar el Proveedor.')
            return HttpResponseRedirect(reverse('proveedores_listado'))
    else:
        return HttpResponseRedirect(reverse('login'))