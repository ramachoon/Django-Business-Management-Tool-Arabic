from extensions.utils import get_client_ip
from .models import IPAddress


class SaveClientInformationMiddleware:
    """
    The middleware save ip address and user information before response.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        ip = get_client_ip(request)
        request_path = request.path
        # These routes should not be saved.
        blocked_routes = ['/serviceworker.js', '/admin/jsi18n/']

        if request.user.is_authenticated and request_path not in blocked_routes and not request.user.is_superuser:
            user = request.user
            user_agent = request.META['HTTP_USER_AGENT']
            request_path += f' -- {request.method}'

            ip_address_object = IPAddress(
                ip=ip,
                user=user,
                url=request_path,
                user_agent=user_agent
            )
            ip_address_object.save()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
