import os
from platform import python_version
from pyreportjasper import JasperPy

from sismec.configuraciones import REPORTES_DIR


def estado_cuenta_cliente():
    input_file = REPORTES_DIR + 'reporte_estado_cuenta.jrxml'
    output = REPORTES_DIR + '\\output'
    con = {
        'driver': 'postgres',
        'username': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'database': 'sismecdb',
        'schema': 'PUBLIC',
        'port': '5432'
    }
    jasper = JasperPy()
    jasper.process(
        input_file,
        output_file=output,
        format_list=["pdf", "rtf", "xml"],
        db_connection=con,
        locale='pt_BR'  # LOCALE Ex.:(en_US, de_GE)
    )