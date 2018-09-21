from django.db import connection

from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao


def getOCFiltro(filtros):
    object_list = []
    query_var = []
    query = '''SELECT oc.id, oc.fecha_pedido,  p.id, p.nombres
                FROM orden_compra_cabecera AS oc
                LEFT JOIN proveedor AS p ON p.id = oc.proveedor_id WHERE 1=1 '''

    if filtros['proveedor'] != '':
        query += '''
         AND oc.proveedor_id = %s'''
        query_var.append(filtros['proveedor'])
    if filtros['fecha'] != '':
        query += ''' 
         AND oc.fecha_pedido = %s'''
        query_var.append(filtros['fecha'])
    if filtros['estado'] != '':
        query += '''  
         AND oc.estado = %s'''
        query_var.append(filtros['estado'])

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
                data = {'id': i[0],
                        'fecha_pedido': i[1],
                        'proveedor_id': i[2] if i[2] is not None else 0,
                        'proveedor_descripcion': i[3] if i[3] is not None else '-',
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination

