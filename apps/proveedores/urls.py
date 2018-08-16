from django.conf.urls import url


import apps.proveedores.views as proveedores_views


urlpatterns = [
   url(r'^sismec/proveedores/agregar/$', proveedores_views.agregarProveedor,  name='proveedores_agregar'),
   url(r'^sismec/proveedores/listado/$', proveedores_views.listarProveedor, name='proveedores_listado'),
   url(r'^sismec/proveedores/detalle/(?P<id>\d+)/$', proveedores_views.detalleProveedor, name='detalle_proveedor'),
   url(r'^sismec/proveedores/eliminar/$', proveedores_views.eliminarProveedor, name='eliminar_proveedor'),
]