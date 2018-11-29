from django.conf.urls import url
import apps.principal.views


urlpatterns = [
   url(r'^sismec/principal/$', apps.principal.views.alertsservice, name='principal'),
   url(r'^sismec/principal_ventas/$', apps.principal.views.alertsserviceVentas, name='principal_ventas'),
   url(r'^sismec/principal_cobros/$', apps.principal.views.alertsserviceCobros, name='principal_cobros'),
]