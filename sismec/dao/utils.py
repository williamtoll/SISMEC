from django.db import connection
import math
import traceback

from sismec.configuraciones import ROW_PER_PAGE


def paginationData(query, query_var, filtro):
    cursor = connection.cursor()
    pagination_data = {}
    try:
        query_total_row = 'SELECT COUNT(*) FROM (' + query + ') AS pagination'
        page = int(filtro['page']) if 'page' in filtro else 1
        row_per_page = int(filtro['row_per_page']) if 'row_per_page' in filtro else ROW_PER_PAGE
        pagination_data = {'page': page, 'row_per_page': row_per_page, 'total_row': 0, 'total_page': 0,
                           'has_other_pages': False, 'has_previous': True, 'has_next': True, 'range': []}
        if len(query_var) > 0:
            cursor.execute(query_total_row, query_var)
        else:
            cursor.execute(query_total_row)

        for i in cursor.fetchall():
            if i[0] > 0:
                pagination_data['has_other_pages'] = True
                pagination_data['total_row'] = i[0]
                pagination_data['total_page'] = math.ceil(pagination_data['total_row'] / row_per_page)

        range_previous = []
        range_next = []
        range_paginator = []

        if page <= pagination_data['total_page']:
            if page == 1:
                pagination_data['has_previous'] = False
            else:
                pagination_data['previous_page_number'] = page - 1
                if page - 5 <= 0:
                    range_previous = range(1, page)
                else:
                    range_previous = range((page - 5), page)

            if page == pagination_data['total_page']:
                pagination_data['has_next'] = False
            else:
                pagination_data['next_page_number'] = page + 1
                if page + 5 < pagination_data['total_page']:
                    range_next = range(page + 1, (page + 6))
                else:
                    range_next = range(page + 1, pagination_data['total_page'] + 1)

            for i in range_previous:
                range_paginator.append(i)
            range_paginator.append(page)
            for i in range_next:
                range_paginator.append(i)

            pagination_data['range'] = range_paginator
        else:
            pagination_data['has_previous'] = False
            pagination_data['has_next'] = False

    except Exception:
        print(traceback.format_exc())
    finally:
        cursor.close()

    return pagination_data