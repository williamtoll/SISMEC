from django.conf.urls import url

import apps.facturas.views as facturas_views

urlpatterns = [
   url(r'^sismec/facturas/agregar/(?P<id>\d+)/$', facturas_views.agregarFacturaCompra,  name='facturas_agregar'),
]
