from django.conf.urls import url

import apps.ajax.views as ajax_views

urlpatterns = [
    url(r'^sismec/ajax/tipo_producto_autocomplete/$', ajax_views.getTipoProductoAutocomplete),
]