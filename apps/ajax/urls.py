from django.conf.urls import url

import apps.ajax.views as ajax_views

urlpatterns = [
    url(r'^sismec/ajax/tipo_producto_autocomplete/$', ajax_views.getTipoProductoAutocomplete),
    url(r'^sismec/ajax/get_producto_name_by_id/$', ajax_views.getTipoProductoById),
    url(r'^sismec/ajax/getProveedorAutocomplete/$', ajax_views.getProveedorAutocomplete),
    url(r'^sismec/ajax/getProductoAutocomplete/$', ajax_views.getProductoAutocomplete),
    url(r'^sismec/ajax/marca_vehiculo_autocomplete/$', ajax_views.getMarcaAutocomplete),
    url(r'^sismec/ajax/modelo_vehiculo_autocomplete/$', ajax_views.getModeloAutocomplete),
    url(r'^sismec/ajax/getClienteAutocomplete/$', ajax_views.getClienteAutocomplete),
    url(r'^sismec/ajax/getRecepcionAutocomplete/$', ajax_views.getRecepcionAutocomplete),
    url(r'^sismec/ajax/getRecepcionById/$', ajax_views.getRecepcionById),

]