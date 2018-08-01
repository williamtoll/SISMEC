def filtros_establecidos(request, tipo_informe):
    if tipo_informe == 'listado_productos':
        try:
            tipo_busqueda=request['tipo_busqueda']
            busqueda_label=request['busqueda_label']
            return True
        except:
            print('Parametros no seteados')
    else:
        return False