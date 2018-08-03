from django.shortcuts import render

# Create your views here.
import json
import traceback
from django.views.decorators.http import require_http_methods

from apps.productos.models import TipoProducto
from sismec.dao import producto_dao
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
@require_http_methods(["GET"])
def getTipoProductoAutocomplete(request):
    if request.method == 'GET':
        try:
            data = request.GET
            nombre = data.get('nombre', '')
            filtros = {'nombre': nombre}
            object_list = producto_dao.getTipoProductoAutocomplete(filtros)
            json_response = json.dumps(object_list)
            return HttpResponse(json_response, content_type='application/json')
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')


@require_http_methods(["GET"])
def getTipoProductoById(request):
    if request.method == 'GET':
        try:
            id_producto = request.GET['producto_id']
            print("id ->" + id_producto);
            object_list = TipoProducto.objects.filter(id=id_producto)
            data = serializers.serialize('json', list(object_list))
            return HttpResponse(data, content_type="application/json")
        except Exception as e:
            traceback.print_exc(e.args)
            return HttpResponseServerError('No se ha podido obtener un resultado')