from sismec.configuraciones import ROW_PER_PAGE
from sismec.dao import utils as utils_dao
from django.db import connection


def getClienteFiltro(filtros):
    object_list = []
    query = '''SELECT row_number() over (ORDER BY c.id), c.id, c.nombres, c.ruc, c.direccion, c.telefono,c.mail, c.tipo_persona
        FROM cliente AS c'''
    query_var = []

    if filtros['search'] != '':
        query += '''
          WHERE UPPER(c.nombres) like UPPER(%s)'''
        query_var = ['%' + filtros['search'] + '%']
    query += '''
      ORDER BY c.id'''

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
                        'nombres': i[2],
                        'ruc': i[3],
                        'direccion':i[4],
                        'telefono': i[5],
                        'mail': i[6],
                        'tipo_persona': i[7],
                        }
                object_list.append(data)

        except Exception as e:
            print(e.args)
        finally:
            cursor.close()
    return object_list, pagination


def getClienteAutocomplete(filtros):
    object_list = []
    tipo_producto_list =[]
    query_var = []
    query = '''SELECT c.id, c.nombres, c.ruc, c.direccion, c.telefono, c.mail, c.tipo_persona FROM cliente c '''

    if filtros['nombres'] != '':
        query += 'WHERE UPPER(c.nombres) LIKE UPPER(%s) '
        query_var.append('%' + filtros['nombres'] + '%')

    query += 'ORDER BY c.nombres'
    cursor = connection.cursor()
    try:
        cursor.execute(query, query_var)
        for i in cursor.fetchall():
            data = {'id': i[0],
                    'nombres': i[1],
                    'ruc': i[2],
                    'direccion': i[3],
                    'telefono': i[4],
                    'mail': i[5],
                    'tipo_persona': i[6],
                    }
            object_list.append(data)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
    return object_list