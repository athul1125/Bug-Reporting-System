from django.core.exceptions import PermissionDenied

def has_bug_status_permission(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.has_perm('bugs.can_change_status'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view