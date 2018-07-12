from django.conf.urls import url


import apps.productos.views as productos_views

urlpatterns = [
   url(r'^sismec/productos/$',productos_views.index, name='productos_home'),
   url(r'^sismec/productos/agregar/$', productos_views.agregarProducto,  name='productos_agregar'),
]