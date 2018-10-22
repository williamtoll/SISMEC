from django.conf.urls import url
import apps.ventas.views as ventas_views

urlpatterns = [
    url(r'^sismec/ventas/agregar/$', ventas_views.agregarPresupuesto,  name='presupuesto_agregar'),
    url(r'^sismec/ventas/listado/$', ventas_views.listarPresupuestos, name='presupuesto_listado'),
    #url(r'^sismec/compras/detalle/(?P<id>\d+)/$', compras_views.detalleOC, name='oc_detalle'),
    #url(r'^sismec/compras/eliminar/$', compras_views.eliminarOC, name='eliminar_oc'),
]
