from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm


# Create your views here.


def login_view(request):
    login_form = LoginForm(request.POST or None)

    if login_form.is_valid():
        phone_number = login_form.cleaned_data.get('phone_number')
        return HttpResponse('ok')

    context = {
        'form': login_form
    }
    return render(request, 'accounts/registration/login.html', context)
