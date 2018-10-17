from django.conf.urls import url


import apps.recepcion.views as recepcion_views

urlpatterns = [
   url(r'^sismec/recepcion/agregar/$', recepcion_views.agregarRecepcionVehiculo,  name='recepcion_agregar'),
   url(r'^sismec/recepcion/listado/$', recepcion_views.listarRecepcion, name='recepcion_listado'),
   url(r'^sismec/recepcion/detalle/(?P<id>\d+)/$', recepcion_views.detalleRecepcion, name='detalle_recepcion'),
   url(r'^sismec/recepcion/eliminar/$', recepcion_views.eliminarRecepcion, name='eliminar_recepcion'),
]