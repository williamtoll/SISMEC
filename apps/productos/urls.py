from django.conf.urls import url

from apps.productos.views import index

urlpatterns = [
   url(r'^sismec/productos/$',index, name='productos_home'),
]