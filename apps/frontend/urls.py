from django.conf.urls import url

import apps.frontend.views

urlpatterns = [
   url(r'^sismec/$', apps.frontend.views.index, name='frontend_home'),
]
