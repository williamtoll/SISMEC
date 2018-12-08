import os
import base64
from platform import python_version
from pyreportjasper import JasperPy
from django.http import HttpResponse, HttpResponseRedirect

from sismec.configuraciones import REPORTES_DIR


def estado_cuenta_cliente(cod_cliente):
    input_file = REPORTES_DIR + '/reporte_estado_cuenta.jrxml'

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
    
    #enviamos el codigo del cliente 
    parametros='and c.id='+cod_cliente
    #parametros='and c.id=1'

    jasper.process(
        input_file,
        output_file=output,
        parameters={'parametros': parametros},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado=output + '/reporte_estado_cuenta.pdf' 

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    return reporte_codificado.decode()
    





        

