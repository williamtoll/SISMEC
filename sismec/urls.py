"""sismec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^sismec/login/$', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^sismec/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    #url(r'^sismec/logout /$', auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    #url(r'^sismec/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^sismec/logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^', include('apps.frontend.urls')),
    url(r'^', include('apps.productos.urls')),
    url(r'^', include('apps.ajax.urls')),
    url(r'^', include('apps.clientes.urls')),
    url(r'^', include('apps.proveedores.urls')),
    url(r'^', include('apps.compras.urls')),
    url(r'^', include('apps.facturas.urls')),
    url(r'^', include('apps.principal.urls')),
    url(r'^', include('apps.recepcion.urls')),
    url(r'^', include('apps.ventas.urls')),
    #path('static/', include('django.contrib.auth.urls')),
]
