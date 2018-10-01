from django.conf.urls import url
import apps.compras.views as compras_views

urlpatterns = [
    url(r'^sismec/compras/agregar/$', compras_views.agregarOC,  name='oc_agregar'),
    url(r'^sismec/compras/listado/$', compras_views.listarOC, name='oc_listado'),
    url(r'^sismec/compras/detalle/(?P<id>\d+)/$', compras_views.detalleOC, name='oc_detalle'),
    url(r'^sismec/compras/eliminar/$', compras_views.eliminarOC, name='eliminar_oc'),
]