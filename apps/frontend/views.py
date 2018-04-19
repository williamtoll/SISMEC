from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your def index(request):
def index(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            t = loader.get_template('frontend/dashboard.html')
            c = {}
            return HttpResponse(t.render(c, request))
        else:
            return HttpResponseRedirect(reverse('frontend_login'))
    else:
        return HttpResponseRedirect(reverse('frontend_login'))