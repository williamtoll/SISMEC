from django.conf.urls import url
import apps.ventas.views as ventas_views

urlpatterns = [
    url(r'^sismec/ventas/agregar/$', ventas_views.agregarPresupuesto,  name='presupuesto_agregar'),
]
