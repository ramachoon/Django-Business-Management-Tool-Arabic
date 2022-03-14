from django.shortcuts import redirect
from django.urls import reverse


def authenticated_user():
    """
    This decorator redirect authenticated users to main page.
    """

    def decorator(view_func):
        def inner(request):
            if request.user.is_authenticated:
                return redirect(reverse('core:main_view'))
            return view_func(request)

        return inner

    return decorator
