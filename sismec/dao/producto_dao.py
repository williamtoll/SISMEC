import cx_Oracle
from django.db import connection

from apps.productos.models import TipoProducto


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
    query = '''SELECT row_number() over (ORDER BY a.marca), a.id, a.nombre, a.fecha_hora_creacion, at.id, at.descripcion 
                FROM autor AS a 
                LEFT JOIN autor_tipo AS at ON at.id = a.tipo_autor_id'''

    if filtros['search'] != '':
        query += ''' 
        WHERE UPPER(a.nombre) like UPPER(%s)'''
        query_var = ['%' + filtros['search'] + '%']
    query += '''
    ORDER BY a.nombre'''

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
                        'nombre': i[2],
                        'fecha_hora_creacion': i[3].strftime('%d/%m/%Y %H:%M') if i[3] is not None else '-',
                        'autor_tipo_id': i[4] if i[4] is not None else 0,
                        'autor_tipo_nombre': i[5] if i[5] is not None else '-',
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination
