from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Tip

def author_or_has_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            tip_id = kwargs.get('pk')
            if not tip_id:
                return HttpResponseForbidden("Tip ID not provided")
            tip = get_object_or_404(Tip, pk=kwargs['pk'])
            if request.user == tip.author or request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to perform this action")
        return _wrapped_view
    return decorator