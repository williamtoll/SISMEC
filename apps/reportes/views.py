from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.reportes.lista_reportes import estado_cuenta_cliente

@csrf_exempt
@require_http_methods(["GET","POST"])
@login_required(login_url='/sismec/login/')
# Funcion p existentes.
def estadoCuentacliente(request):
    t = loader.get_template('reportes/estado_cuenta_cliente.html')
    c = {}

    if request.method=='POST':
        cod_cliente=request.POST.get('cod-cliente','')
        reporte_generado = estado_cuenta_cliente(cod_cliente)

        # response = HttpResponse(pdf.read(), content_type='application/pdf')
        # response['Content-Disposition'] = 'inline;filename=reporte_estado_cuenta.pdf;charset=utf-8'

            # response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format("reporte_estado_cuenta")
            # response.write(pdf)

            #return response
        params={
            'reporte_pdf': reporte_generado
        }

        return HttpResponse(t.render(params,request))

    
    return HttpResponse(t.render(c, request))