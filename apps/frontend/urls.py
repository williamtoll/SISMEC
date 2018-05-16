from django.conf.urls import url

import apps.frontend.views

urlpatterns = [
   url(r'^sismec/home/$', apps.frontend.views.index, name='frontend_home'),
]
