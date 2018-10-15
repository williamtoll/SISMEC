from django.conf.urls import url


import apps.recepcion.views as recepcion_views

urlpatterns = [
   url(r'^sismec/recepcion/agregar/$', recepcion_views.agregarRecepcionVehiculo,  name='recepcion_agregar'),
   # url(r'^sismec/productos/listado/$', productos_views.listarProducto, name='productos_listado'),
   # url(r'^sismec/productos/detalle/(?P<id>\d+)/$', productos_views.detalleProducto, name='detalle_producto'),
   # url(r'^sismec/productos/eliminar/$', productos_views.eliminarProducto, name='eliminar_producto'),
]