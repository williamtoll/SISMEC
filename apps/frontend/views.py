from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import NoReverseMatch, reverse
from django.template import loader
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your def index(request):
@require_http_methods(["GET", "POST"])
@login_required(login_url='/sismec/login/')
def index(request):
    t = loader.get_template('index.html')
    c = {}
    return HttpResponse(t.render(c, request))