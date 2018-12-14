import os
import base64
from platform import python_version
from pyreportjasper import JasperPy
from django.http import HttpResponse, HttpResponseRedirect

from sismec.configuraciones import REPORTES_DIR


def estado_cuenta_cliente(cod_cliente,tipo_visualizacion):
    #input_file = REPORTES_DIR + '/reporte_estado_cuenta.jrxml'
    input_file = REPORTES_DIR + '/reporte_estado_cuenta.jrxml'

    #la carpeta donde se genera el pdf
    #output = REPORTES_DIR + '/output'
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

    archivo_reporte=output + '/reporte_estado_cuenta.pdf' 

    print('Reporte generado')
    print(archivo_reporte)

    reporte = open(archivo_reporte, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)


    if tipo_visualizacion=='mostrar':
        ##return reporte_codificado.decode()
        return archivo_reporte
    else:
        return archivo_reporte
    



def productos_mas_vendidos(fecha_ini, fecha_fin, tipo_visualizacion):
    input_file = REPORTES_DIR + '/productos_mas_vendidos.jrxml'

    # la carpeta donde se genera el pdf
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    # enviamos el codigo del cliente
    fecha_inicio = str(fecha_ini)
    fecha_fin = str(fecha_fin)
    # parametros='and c.id=1'

    jasper.process(
        input_file,
        output_file=output,
        parameters={'fecha_inicio': "'" + fecha_inicio + "'",
                    'fecha_fin': "'" + fecha_fin + "'"},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/productos_mas_vendidos.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion=='mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado

def movimientos_compras(fecha_ini, fecha_fin, tipo_visualizacion):
    input_file = REPORTES_DIR + '/reporte_compras.jrxml'

    # la carpeta donde se genera el pdf
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    # enviamos el codigo del cliente
    fecha_inicio = str(fecha_ini)
    fecha_fin = str(fecha_fin)
    # parametros='and c.id=1'

    jasper.process(
        input_file,
        output_file=output,
        parameters={'fecha_inicio': "'" + fecha_inicio + "'",
                    'fecha_fin': "'" + fecha_fin + "'"},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/reporte_compras.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion == 'mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado


def movimientos_ventas(fecha_ini, fecha_fin, tipo_visualizacion):
    input_file = REPORTES_DIR + '/reporte_ventas.jrxml'

    # la carpeta donde se genera el pdf
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    # enviamos el codigo del cliente
    fecha_inicio = str(fecha_ini)
    fecha_fin = str(fecha_fin)
    # parametros='and c.id=1'

    jasper.process(
        input_file,
        output_file=output,
        parameters={'fecha_inicio': "'" + fecha_inicio + "'",
                    'fecha_fin': "'" + fecha_fin + "'"},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/reporte_ventas.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion == 'mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado


def cuentas_a_pagar(fecha_ini, fecha_fin, tipo_visualizacion):
    input_file = REPORTES_DIR + '/reporte_cuentas_a_pagar.jrxml'

    # la carpeta donde se genera el pdf
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    # enviamos el codigo del cliente
    fecha_inicio = str(fecha_ini)
    fecha_fin = str(fecha_fin)
    # parametros='and c.id=1'

    jasper.process(
        input_file,
        output_file=output,
        parameters={'fecha_inicio': "'" + fecha_inicio + "'",
                    'fecha_fin': "'" + fecha_fin + "'"},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/reporte_cuentas_a_pagar.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion == 'mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado


def ventas_mensuales(tipo_visualizacion):
    # input_file = REPORTES_DIR + '/reporte_estado_cuenta.jrxml'
    input_file = REPORTES_DIR + '/reporte_ventas_mensuales.jrxml'

    # la carpeta donde se genera el pdf
    # output = REPORTES_DIR + '/output'
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    jasper.process(
        input_file,
        output_file=output,
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/reporte_ventas_mensuales.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion == 'mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado

def compras_mensuales(tipo_visualizacion):
    # input_file = REPORTES_DIR + '/reporte_estado_cuenta.jrxml'
    input_file = REPORTES_DIR + '/reporte_compras_mensuales.jrxml'

    # la carpeta donde se genera el pdf
    # output = REPORTES_DIR + '/output'
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    jasper.process(
        input_file,
        output_file=output,
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/reporte_compras_mensuales.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion == 'mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado

def mejores_clientes(fecha_ini, fecha_fin, tipo_visualizacion):
    input_file = REPORTES_DIR + '/reporte_mejores_clientes.jrxml'

    # la carpeta donde se genera el pdf
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

    # compilamos el reporte
    jasper.compile(input_file)

    # listamos todos los parametros que permite el reporte
    lista_parametros = jasper.list_parameters(input_file)
    print(lista_parametros)

    # enviamos el codigo del cliente
    fecha_inicio = str(fecha_ini)
    fecha_fin = str(fecha_fin)
    # parametros='and c.id=1'

    jasper.process(
        input_file,
        output_file=output,
        parameters={'fecha_inicio': "'" + fecha_inicio + "'",
                    'fecha_fin': "'" + fecha_fin + "'"},
        format_list=["pdf"],
        db_connection=con,
        locale='es_PY'  # LOCALE Ex.:(en_US, de_GE)
    )

    reporte_generado = output + '/reporte_mejores_clientes.pdf'

    print('Reporte generado')
    print(reporte_generado)

    reporte = open(reporte_generado, 'rb')
    reporte_leido = reporte.read()
    reporte_codificado = base64.b64encode(reporte_leido)

    if tipo_visualizacion == 'mostrar':
        ##return reporte_codificado.decode()
        return reporte_generado
    else:
        return reporte_generado