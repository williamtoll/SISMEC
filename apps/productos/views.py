from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader, RequestContext
from django.contrib import messages
import traceback
from django.contrib.auth.decorators import login_required
from apps.principal.common_functions import filtros_establecidos
from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import producto_dao
from django.views.decorators.http import require_http_methods

from apps.productos.forms import ProductoForm
from apps.productos.models import Producto, TipoProducto
from django.contrib.auth.decorators import permission_required

from sismec.utils import custom_permission_required


@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('productos.add_producto')
# # Funcion para agregar un producto.
def agregarProducto(request):
    t = loader.get_template('productos/agregar.html')
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        tipo_producto_list = request.POST.getlist('id_tipo_producto_select', '')
        try:
            if form.is_valid():
                for tipo_producto_o in tipo_producto_list:
                    tipo_producto = TipoProducto.objects.get(id=tipo_producto_o)
                    form.instance.tipo_producto = tipo_producto
                form.save()
                messages.add_message(request, messages.INFO, 'Producto agregado exitosamente')
                return HttpResponseRedirect(reverse('productos_listado'))
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
        form = ProductoForm()
        c = {'form': form}
        return HttpResponse(t.render(c, request))


@require_http_methods(["GET"])
@login_required(login_url='/sismec/login/')
# Funcion para listar PRODUCTOS existentes.
def listarProducto(request):
    t = loader.get_template('productos/listado.html')
    if request.method == 'GET':
        data = request.GET
        filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
                   'page': data.get('page', 1), 'search': data.get('search', '')}

        query_param_list = [filtros['row_per_page'], filtros['search']]

        query_params = '?row_per_page={}&search={}'.format(*query_param_list)
        object_list, pagination = producto_dao.getProductoFiltro(filtros)

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
def detalleProducto(request, id):
    t = loader.get_template('productos/detalle.html')
    object_list = Producto.objects.get(pk=id)
    # Se envia el formulario
    if request.method == 'POST':
        data = request.POST
        if data.get('boton_guardar'):
            form =ProductoForm(data, instance=object_list)
            tipo_producto_list = request.POST.getlist('id_tipo_producto_select', '')
            if form.is_valid():
                for tipo_producto_o in tipo_producto_list:
                    tipo_producto = TipoProducto.objects.get(id=tipo_producto_o)
                    form.instance.tipo_producto = tipo_producto
                form.save()
                messages.add_message(request, messages.INFO, 'Se actualizaron los datos')
                return HttpResponseRedirect(reverse('productos_listado'))
        elif data.get('boton_borrar'):
            try:
                obj = Producto.objects.get(pk=id)
                obj.delete()
                messages.add_message(request, messages.INFO, 'Producto eliminado')
                return HttpResponseRedirect(reverse('productos_listado'))
            except Exception as e:
                traceback.print_exc(e.args)
                messages.add_message(request, messages.ERROR,
                                     'No se puede eliminar el Producto.')
                return HttpResponseRedirect(reverse('frontend_home') + 'productos/detalle/%s' % id)
    else:
        form = ProductoForm(instance=object_list)
        c = {
            'object_list': object_list,
            'form': form,
            'tipo_producto': object_list.tipo_producto.id
        }
        return HttpResponse(t.render(c, request))


@require_http_methods(["POST"])
@login_required(login_url='/sismec/login/')
@custom_permission_required('productos.delete_producto')
# Funcion para eliminar un autor desde el listado.
def eliminarProducto(request):
    if request.method == 'POST':
        data = request.POST
        id = data.get('id_eliminar')
        try:
            obj = Producto.objects.get(pk=id)
            obj.delete()
            messages.add_message(request, messages.INFO, 'Producto eliminado')
        except Exception as e:
            traceback.print_exc(e.args)
            messages.add_message(request, messages.ERROR,
                                 'No se puede eliminar el Producto.')
        return HttpResponseRedirect(reverse('productos_listado'))