from django.conf.urls import url

import apps.ajax.views as ajax_views

urlpatterns = [
    url(r'^sismec/ajax/tipo_producto_autocomplete/$', ajax_views.getTipoProductoAutocomplete),
    url(r'^sismec/ajax/get_producto_name_by_id/$', ajax_views.getTipoProductoById),
    url(r'^sismec/ajax/getProveedorAutocomplete/$', ajax_views.getProveedorAutocomplete),
    url(r'^sismec/ajax/getProductoAutocomplete/$', ajax_views.getProductoAutocomplete),
]