import cx_Oracle
from django.db import connection

from apps.productos.models import TipoProducto
from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao

def getTipoProductoAutocomplete(filtros):
    object_list = []
    tipo_producto_list =[]
    query_var = []
    query = '''SELECT at.id, at.descripcion, at.fecha_hora_creacion FROM producto_tipo at '''

    if filtros['nombre'] != '':
        query += 'WHERE UPPER(at.descripcion) LIKE UPPER(%s) '
        query_var.append('%' + filtros['nombre'] + '%')

    query += 'ORDER BY at.descripcion'
    cursor = connection.cursor()
    try:
        cursor.execute(query, query_var)
        for i in cursor.fetchall():
            data = {'id': i[0],
                    'nombre': i[1],
                    'fecha_hora_creacion': i[2].strftime('%d/%m/%Y %H:%M') if i[2] is not None else '-',
                    }
            object_list.append(data)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
    return object_list



def getProductoFiltro(filtros):
    object_list = []
    query_var = []
    query = '''SELECT row_number() over (ORDER BY p.marca), p.id, p.descripcion, p.marca, p.cantidad, p.precio_venta, p.tipo_impuesto, pt.id, pt.descripcion
                FROM producto AS p
                LEFT JOIN producto_tipo AS pt ON pt.id = p.tipo_producto_id'''

    if filtros['search'] != '':
        query += '''
        WHERE UPPER(p.descripcion) like UPPER(%s)'''
        query_var = ['%' + filtros['search'] + '%']
    query += '''
    ORDER BY p.marca'''

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
                data = {'row_number': i[0],
                        'id': i[1],
                        'descripcion': i[2],
                        'marca': i[3] if i[3] is not None else '-',
                        'cantidad': i[4] if i[4] is not None else 0,
                        'precio_venta': i[5] if i[5] is not None else 0,
                        'tipo_impuesto': i[6] if i[6] is not None else '-',
                        'producto_tipo_id': i[7] if i[7] is not None else 0,
                        'producto_tipo_nombre': i[8] if i[8] is not None else '-',
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination


def getProductoAutocomplete(filtros):
    object_list = []
    query_var = []
    query = '''SELECT p.id, p.descripcion, p.marca, p.cantidad, p.precio_venta, p.tipo_impuesto, pt.id, pt.descripcion
                FROM producto AS p
                LEFT JOIN producto_tipo AS pt ON pt.id = p.tipo_producto_id'''

    if filtros['nombre'] != '':
        query += '''
        WHERE UPPER(p.descripcion) like UPPER(%s)'''
        query_var = ['%' + filtros['search'] + '%']
    query += '''
    ORDER BY p.marca'''
    cursor = connection.cursor()
    try:
        cursor.execute(query, query_var)

        for i in cursor.fetchall():
            data = {'id': i[0],
                    'descripcion': i[1],
                    'marca': i[2] if i[2] is not None else '-',
                    'cantidad': i[3] if i[3] is not None else 0,
                    'precio_venta': i[4] if i[4] is not None else 0,
                    'tipo_impuesto': i[5] if i[5] is not None else '-',
                    'producto_tipo_id': i[6] if i[6] is not None else 0,
                    'producto_tipo_nombre': i[7] if i[7] is not None else '-',
                    }
            object_list.append(data)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
    return object_list