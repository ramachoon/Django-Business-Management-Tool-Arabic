from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.


@login_required(login_url='account:login')
def main_view(request):
    if request.user.is_superuser:
        return redirect(reverse('managers:home'))
    elif request.user.is_staff:
        return redirect((reverse('staff_module:home')))
    return HttpResponse('خوش آمدید')
