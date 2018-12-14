import os
import base64
from platform import python_version
from pyreportjasper import JasperPy
from django.http import HttpResponse, HttpResponseRedirect

from sismec.configuraciones import REPORTES_DIR
from apps.facturas.models import MovimientoCabecera
from num2words import num2words

def imprimir_factura_venta_jasper(nro_movimiento):
    input_file = REPORTES_DIR + '/factura_venta.jrxml'

    #la carpeta donde se genera el pdf
    output = REPORTES_DIR + '/output'

    con = {
        'driver': 'postgres',
        'username': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'database': 'sismecdb',
        'schema': 'public',
        'port': '5432'
    }
    
    jasper = JasperPy()

    #compilamos el reporte
    jasper.compile(input_file)

    #listamos todos los parametros que permite el reporte
    lista_parametros=jasper.list_parameters(input_file)
    print(lista_parametros)
    print("el nro de movimiento es: ")
    print(nro_movimiento)
    if nro_movimiento:
        #enviamos el codigo del cliente 
        parametros='and cab.id='+nro_movimiento

    print("parametros")
    print(parametros)

    #generamos el monto en letras
    movimientoCab = MovimientoCabecera.objects.get(pk=nro_movimiento)

    #total_en_letras=convertirNumeroALetras(movimientoCab.monto_total)
    total_en_letras=num2words(int(movimientoCab.monto_total),lang='es')
    print("total en letras")
    print(total_en_letras)

    jasper.process(
        input_file,
        output_file=output,
        parameters={'parametros': parametros,'total_en_letras': total_en_letras},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado=output + '/factura_venta.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    ##return reporte_codificado.decode()
    return reporte_generado;




  