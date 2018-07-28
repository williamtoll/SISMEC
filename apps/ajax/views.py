from django.shortcuts import render

# Create your views here.
import json
import traceback
from django.views.decorators.http import require_http_methods
from sismec.dao import producto_dao
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_http_methods

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