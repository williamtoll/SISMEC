from django.conf.urls import url
import apps.compras.views as compras_views

urlpatterns = [
    url(r'^sismec/compras/agregar/$', compras_views.agregarOC,  name='oc_agregar'),
    url(r'^sismec/compras/listado/$', compras_views.listarOC, name='oc_listado'),
]