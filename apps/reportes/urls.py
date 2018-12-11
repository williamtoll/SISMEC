from django.conf.urls import url
import apps.reportes.views as reportes_views

urlpatterns = [
    url(r'^sismec/reportes/estado_cuenta/$', reportes_views.estadoCuentacliente, name='estado_cuenta_cliente'),
    url(r'^sismec/reportes/productos_mas_vendidos/$', reportes_views.productosMasVendidos, name='productos_mas_vendidos'),
]