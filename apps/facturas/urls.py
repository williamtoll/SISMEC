from django.conf.urls import url

import apps.facturas.views as facturas_views

urlpatterns = [
   url(r'^sismec/facturas/agregar/(?P<id>\d+)/$', facturas_views.agregarFacturaCompra,  name='facturas_agregar'),
   url(r'^sismec/facturas/generar_factura/(?P<id>\d+)/$', facturas_views.generarFacturaVenta,  name='factura_venta_agregar'),
   url(r'^sismec/facturas/listado/$', facturas_views.listarFV, name='factura_venta_listado'),
   url(r'^sismec/facturas/listado_compra/$', facturas_views.listarFC, name='factura_compra_listado'),
   url(r'^sismec/facturas/cobrar_factura/(?P<id>\d+)/$', facturas_views.cobrarFacturaVenta, name='cobrar_fv'),
   url(r'^sismec/facturas/imprimir_recibo_cobro/$', facturas_views.imprimirReciboCobro, name='imprimir_recibo'),
   
]
