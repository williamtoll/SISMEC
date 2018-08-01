# -*- encoding: utf-8 -*-
import math
from django import template

register = template.Library()


@register.filter
def len_list(object_list):
    if (len(object_list) > 0):
        return True
    else:
        return False


@register.filter
def get_key_value(mapping, key):
    return mapping.get(key, '')


@register.filter
def extract_space(template_name):
    try:
        return template_name.lower().replace(' ', '')
    except (ValueError, TypeError):
        return ''


@register.filter
def pagination_data(pagination, object_list):
    if (len(object_list) == 0):
        pagination_text = 'No existen registros en la página'
    else:
        if (pagination['total_row'] == 1):
            pagination_text = 'Mostrando registros del 1 al 1 un total de 1 registro'
        elif (pagination['total_row'] < pagination['row_per_page']):
            pagination_text = 'Mostrando registros del 1 al ' + str(pagination['total_row']) + \
                              ' de un total de ' + str(pagination['total_row']) + ' registros'
        else:
            num_item = int(pagination['row_per_page']) * pagination['page']
            item = num_item - int(pagination['row_per_page']) + 1
            if (int(pagination['row_per_page']) < num_item):
                num_item = int(pagination['total_row'])

            pagination_text = 'Mostrando registros del ' + str(item) + ' al ' + str(num_item) + ' de un total de ' \
                              + str(pagination['total_row']) + ' registros'
    return pagination_text


@register.filter
def upper_string(string):
    try:
        return string.upper()
    except (ValueError, TypeError):
        return ''


@register.filter
def multiplo4_div(elemento):
    if (elemento % 4) == 1:
        return True
    else:
        return False


@register.filter
def multiplo4_div_cerrar(elemento):
    if (elemento % 4) == 0:
        return True
    else:
        return False


@register.filter
def multiplo3_div_row(elemento):
    if elemento <= 3:
        return True
    else:
        return False


@register.filter
def multiplo6_div(elemento):
    if (elemento % 6) == 1:
        return True
    else:
        return False


@register.filter
def multiplo6_div_cerrar(elemento):
    if (elemento % 6) == 0:
        return True
    else:
        return False


@register.filter
def multiplo6_div_row(elemento):
    if elemento <= 6:
        return True
    else:
        return False


@register.filter
def multiplo_lista(elemento, object_list):
    if elemento % len(object_list) == 0:
        return True
    else:
        return False


@register.filter
def len_lista(elemento, object_list):
    if elemento == len(object_list):
        return True
    else:
        return False


@register.filter
def pagina_lista(elemento):
    return int(elemento / 6) + 1


@register.filter
def extensionUpper(doc):
    return '.{}'.format(doc.path_file.name.split('.')[1].lower())


@register.filter
def extensionMP4(doc):
    return doc.path_file.name.split('.')[1] == 'mp4'


@register.filter
def nameMP4(doc):
    return doc.path_file.name.split('/')[len(doc.path_file.name.split('/')) - 1].split('.')[0].upper()


@register.filter
def extensionIcon(doc):
    extension_doc = doc.path_file.name.split('.')[1]
    if extension_doc in ['doc', 'docx']:
        return 'fa-file-word-o'
    elif extension_doc in ['pdf']:
        return 'fa-file-pdf-o'
    elif extension_doc in ['mp4']:
        return 'fa-file-video-o'
    elif extension_doc in ['mp3']:
        return 'fa-file-audio-o'
    else:
        return 'icon-download'


@register.filter
def formatoFecha(fecha):
    return fecha.strftime('%d/%m/%Y %H:%M') if fecha is not None else '-'


@register.filter
def nameDoc(path_file):
    if path_file != '':
        return path_file.split('/')[len(path_file.split('/')) - 1].split('.')[0].upper()
    else:
        return 'TODOS'


@register.filter
def extensionDoc(path_file):
    if path_file != '':
        return path_file.split('/')[len(path_file.split('/')) - 1].split('.')[1].upper()
    else:
        return 'ZIP'
