from django.conf.urls import url


import apps.clientes.views as clientes_views


urlpatterns = [
   url(r'^sismec/clientes/agregar/$', clientes_views.agregarCliente,  name='clientes_agregar'),
   url(r'^sismec/clientes/listado/$', clientes_views.listarCliente, name='clientes_listado'),
   url(r'^sismec/clientes/detalle/(?P<id>\d+)/$', clientes_views.detalleCliente, name='detalle_cliente'),
   url(r'^sismec/clientes/eliminar/$', clientes_views.eliminarCliente, name='eliminar_cliente'),
]