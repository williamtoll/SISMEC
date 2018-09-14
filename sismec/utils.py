from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)

@decorator_with_arguments
def custom_permission_required(function, perm):
    def _function(request, *args, **kwargs):
        if request.user.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, 'No posee los privilegios suficientes')
            # Return a response or redirect to referrer or some page of your choice
            return HttpResponseRedirect(reverse('frontend_home'))
    return _function