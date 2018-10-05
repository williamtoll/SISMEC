from django.conf.urls import url
import apps.principal.views


urlpatterns = [
   url(r'^sismec/principal/$', apps.principal.views.alertsservice, name='principal'),
]