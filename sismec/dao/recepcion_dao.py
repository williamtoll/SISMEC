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


def getRecepcionFiltro(filtros):
    object_list = []
    query_var = []
    query = '''SELECT rv.codigo_recepcion, rv.fecha_recepcion, rv.chapa,  
               rv.detalle_problema, m.descripcion, mod.descripcion, c.nombres
               FROM recepcion_vehiculo rv, marca m, modelo mod, cliente c
               where rv.marca_id = m.id and rv.modelo_id = mod.id and rv.cliente_id = c.id '''

    if filtros['cliente'] != '':
        query += '''
         AND rv.cliente_id = %s'''
        query_var.append(filtros['cliente'])
    if filtros['fecha_recepcion'] != '':
        query += ''' 
         AND rv.fecha_recepcion = %s'''
        query_var.append(filtros['fecha_recepcion'])

    pagination = utils_dao.paginationData(query, query_var, filtros)

    total_row = pagination['total_row']
    row_per_page = pagination['row_per_page'] if 'row_per_page' in pagination else ROW_PER_PAGE
    page = pagination['page']

    if total_row > 0:
        cursor = connection.cursor()
        try:
            query_row_page = 'SELECT * FROM(' + query + ') AS pagination LIMIT %s OFFSET (%s - 1) * %s'
            query_var_page = query_var
            query_var_page.append(row_per_page)
            query_var_page.append(page)
            query_var_page.append(row_per_page)
            cursor.execute(query_row_page, query_var_page)

            for i in cursor.fetchall():
                data = {'codigo_recepcion': i[0],
                        'fecha_recepcion': i[1],
                        'chapa': i[2] if i[2] is not None else '-',
                        'detalle_problema': i[3] if i[3] is not None else '-',
                        'marca': i[4] if i[4] is not None else '-',
                        'modelo': i[5] if i[5] is not None else '-',
                        'cliente': i[6] if i[6] is not None else '-',
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination