from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader
#El home principal de productos
from django.views.decorators.http import require_http_methods

from apps.productos.forms import ProductoForm
from apps.productos.models import Producto


def index(request):
    if request.user.is_authenticated:
            t = loader.get_template('productos/home_productos.html')
            c = {}
            return HttpResponse(t.render(c, request))
    else:
       return HttpResponseRedirect(reverse('login'))


@require_http_methods(["GET", "POST"])
# # Funcion para agregar un producto.
def agregarProducto(request):
    if request.user.is_authenticated:
        t = loader.get_template('productos/agregar.html')
        # if request.method == 'POST':
        #form = Producto(request.POST)
        #     #tipo_autor_list = request.POST.getlist('id_tipo_autor_select', '')
        #     try:
        #         if form.is_valid():
        #             # for tipo_autor_o in tipo_autor_list:
        #             #     tipo_autor = TipoAutor.objects.get(id=tipo_autor_o)
        #             #     form.instance.tipo_autor = tipo_autor
        #             form.save()
        #             messages.add_message(request, messages.INFO, 'Autor agregado exitosamente')
        #             return HttpResponseRedirect(reverse('frontend_listado_autor'))
        #         else:
        #             messages.add_message(request, messages.ERROR, form.errors)
        #             c = {'form': form}
        #             return HttpResponse(t.render(c, request))
        #     except Exception as e:
        #         traceback.print_exc(e.args)
        #         messages.add_message(request, messages.ERROR, e.args)
        #         c = {'form': form}
        #         return HttpResponse(t.render(c, request))
        # else:
        form = ProductoForm()
        c = {'form': form}
        return HttpResponse(t.render(c, request))
    else:
        return HttpResponseRedirect(reverse('frontend_login'))
#
#
# @require_http_methods(["GET"])
# # Funcion para listar autores existentes.
# def listarAutor(request):
#     if request.user.is_authenticated():
#         t = loader.get_template('autor/listado.html')
#         if request.method == 'GET':
#             data = request.GET
#             filtros = {'row_per_page': data.get('row_per_page', ROW_PER_PAGE),
#                        'page': data.get('page', 1), 'search': data.get('search', '')}
#
#             query_param_list = [filtros['row_per_page'], filtros['search']]
#
#             query_params = '?row_per_page={}&search={}'.format(*query_param_list)
#             object_list, pagination = autor_dao.getAutorFiltro(filtros)
#
#             c = {
#                 'object_list': object_list,
#                 'pagination': pagination,
#                 'filtros': filtros,
#                 'query_params': query_params
#             }
#             return HttpResponse(t.render(c, request))
#     else:
#         return HttpResponseRedirect(reverse('frontend_login'))
#
