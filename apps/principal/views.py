from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader
# Create your views here.
def index(request):
    if request.user.is_authenticated():
        if request.user.is_active:
            t = loader.get_template('principal/dashboard.html')
            c = {}
            return HttpResponse(t.render(c, request))
        else:
            return HttpResponseRedirect(reverse('frontend_login'))
    else:
        return HttpResponseRedirect(reverse('frontend_login'))