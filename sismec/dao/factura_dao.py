from django.db import connection

from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao

def getFacturaVentaFiltro(filtros):
    object_list = []
    query_var = []
    query = '''SELECT mc.id, mc.fecha_emision, mc.numero_factura, mc.tipo_factura, mc.estado, mc.monto_total, mc.saldo, c.nombres, c.id, pc.id
               FROM movimiento_cabecera mc, cliente c, presupuesto_cabecera pc
               WHERE mc.cliente_id = c.id and mc.presupuesto_id = pc.id '''

    if filtros['cliente'] != '':
        query += '''
         AND c.id = %s'''
        query_var.append(filtros['cliente'])
    if filtros['fecha'] != '':
        query += ''' 
         AND mc.fecha_emision = %s'''
        query_var.append(filtros['fecha'])
    if filtros['estado'] != '':
        query += '''  
         AND mc.estado = %s'''
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
                        'fecha_emision': i[1],
                        'numero_factura': i[2] if i[2] is not None else 0,
                        'tipo_factura': i[3] if i[3] is not None else '-',
                        'estado': i[4] if i[4] is not None else '-',
                        'monto_total': i[5] if i[5] is not None else '-',
                        'saldo': i[6] if i[6] is not None else '-',
                        'nombres': i[7] if i[7] is not None else '-',
                        'cliente_id': i[8] if i[8] is not None else '-',
                        'presupuesto_id': i[9] if i[9] is not None else '-',
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination