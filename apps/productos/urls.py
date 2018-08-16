from django.conf.urls import url


import apps.productos.views as productos_views

urlpatterns = [
   url(r'^sismec/productos/agregar/$', productos_views.agregarProducto,  name='productos_agregar'),
   url(r'^sismec/productos/listado/$', productos_views.listarProducto, name='productos_listado'),
   url(r'^sismec/productos/detalle/(?P<id>\d+)/$', productos_views.detalleProducto, name='detalle_producto'),
   url(r'^sismec/productos/eliminar/$', productos_views.eliminarProducto, name='eliminar_producto'),
]