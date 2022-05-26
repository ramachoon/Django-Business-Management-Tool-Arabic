from django.core.exceptions import PermissionDenied
from django.http import Http404


class SuperuserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class StaffAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
