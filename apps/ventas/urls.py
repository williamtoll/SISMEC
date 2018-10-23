from django.conf.urls import url
import apps.ventas.views as ventas_views

urlpatterns = [
    url(r'^sismec/ventas/agregar/$', ventas_views.agregarPresupuesto,  name='presupuesto_agregar'),
    url(r'^sismec/ventas/listado/$', ventas_views.listarPresupuestos, name='presupuesto_listado'),
    url(r'^sismec/ventas/detalle/(?P<id>\d+)/$', ventas_views.detallePresupuesto, name='presupuesto_detalle'),
    url(r'^sismec/ventas/eliminar/$', ventas_views.eliminarPresupuesto, name='eliminar_pre'),
]
