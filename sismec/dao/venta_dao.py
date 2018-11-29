from django.db import connection

from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao

def getPresupuestoFiltro(filtros):
    object_list = []
    query_var = []
    query = '''SELECT pc.id, pc.fecha_presupuesto, rv.codigo_recepcion, rv.estado
	           FROM public.presupuesto_cabecera as pc
	           LEFT JOIN recepcion_vehiculo AS rv ON rv.id = pc.recepcion_vehiculo_id WHERE 1=1 '''

    if filtros['codigo'] != '':
        query += '''
        AND UPPER(rv.codigo_recepcion) LIKE UPPER(%s)'''
        query_var.append('%' + filtros['codigo'] + '%')
    if filtros['fecha'] != '':
        query += ''' 
         AND pc.fecha_presupuesto = %s'''
        query_var.append(filtros['fecha'])
    if filtros['estado'] != '':
        query += '''  
         AND pc.estado = %s'''
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
                        'fecha_presupuesto': i[1],
                        'codigo_recepcion': i[2] if i[2] is not None else 0,
                        'estado': i[3] if i[3] is not None else '-',
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination