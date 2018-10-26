import datetime

from apps.recepcion.models import SecuenciaNumerica


def filtros_establecidos(request, tipo_informe):
    if tipo_informe == 'listado_productos':
        try:
            tipo_busqueda=request['tipo_busqueda']
            busqueda_label=request['busqueda_label']
            return True
        except:
            print('Parametros no seteados')
    else:
        return False

def generar_codigo():
    now = datetime.datetime.now()
    currentYear = now.year
    try:
        secuencia = SecuenciaNumerica.objects.get(anho= currentYear)
    except SecuenciaNumerica.DoesNotExist:
        secuencia = None
    if secuencia == None:
        secuencia = SecuenciaNumerica()
        secuencia.anho = currentYear
        secuencia.ultimo_numero = 1
        secuencia.save()
        codigo = str(secuencia.ultimo_numero) + "-" + str(secuencia.anho)
    else:
        codigo = str(int(secuencia.ultimo_numero + 1)) + "-" + str(secuencia.anho)
        nro_secuencia = secuencia.ultimo_numero + 1
        secuencia.ultimo_numero = nro_secuencia
        secuencia.save()
    return codigo
