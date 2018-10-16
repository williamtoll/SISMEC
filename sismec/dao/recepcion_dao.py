from django.db import connection

from apps.recepcion.models import Marca, Modelo
from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao

def getMarcaAutocomplete(filtros):
    object_list = []
    tipo_producto_list =[]
    query_var = []
    query = '''SELECT m.id, m.descripcion FROM marca m '''

    if filtros['descripcion'] != '':
        query += 'WHERE UPPER(m.descripcion) LIKE UPPER(%s) '
        query_var.append('%' + filtros['descripcion'] + '%')

    query += 'ORDER BY m.descripcion'
    cursor = connection.cursor()
    try:
        cursor.execute(query, query_var)
        for i in cursor.fetchall():
            data = {'id': i[0],
                    'descripcion': i[1],
                    }
            object_list.append(data)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
    return object_list

def getModeloAutocomplete(filtros):
    object_list = []
    query_var = []
    query = '''SELECT mo.id, mo.descripcion FROM modelo mo
            LEFT JOIN marca ma
            ON mo.marca_id = ma.id 
            WHERE 1 = 1 AND  '''

    if filtros['marca'] != '':
        query += '''
        ma.id = %s'''
        query_var.append(filtros['marca'])
    if filtros['descripcion'] != '':
        query += ''' 
         AND UPPER(mo.descripcion)  LIKE UPPER(%s) '''
        query_var.append('%' + filtros['descripcion'] + '%')

    query += ' ORDER BY mo.descripcion'
    cursor = connection.cursor()
    try:
        cursor.execute(query, query_var)
        for i in cursor.fetchall():
            data = {'id': i[0],
                    'descripcion': i[1],
                    }
            object_list.append(data)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
    return object_list