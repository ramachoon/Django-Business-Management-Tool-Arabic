import random
from hashlib import sha256

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.cache import cache

from core.mixins import AuthenticatedUserMixin
from extensions.sms_services import send_otp_sms
from .forms import LoginForm, VerifyOtpForm, RegisterForm, PasswordLoginForm
from accounts.models import PhoneOtp, User
from core.decorators import authenticated_user


# Create your views here.

@authenticated_user()
def otp_login(request):
    """
    Display login form.

    ** CONTEXT **
        ``form``
            login_form for send otp code.

    ** TEMPLATE **
        :template: `accounts/registration/login.html`

    :param: `request`
    """

    login_form = LoginForm(request.POST or None)

    if login_form.is_valid():
        phone_number = login_form.cleaned_data.get('phone_number')
        _code = random.randint(1111, 9999)
        send_otp_sms(phone_number, _code)
        hash_code = sha256(str(_code).encode('utf-8')).hexdigest()
        cache.set(phone_number, hash_code, 500)

        request.session['phone_number'] = phone_number

        try:
            phone_otp = PhoneOtp.objects.get(phone=phone_number)
            phone_otp.code = hash_code
            phone_otp.save()
        except PhoneOtp.DoesNotExist:
            phone_otp = PhoneOtp(phone=phone_number, code=hash_code)
            phone_otp.save()

        return redirect(reverse('account:verify_otp'))

    context = {
        'form': login_form
    }
    return render(request, 'accounts/registration/login.html', context)


@authenticated_user()
def verify_phone_otp(request):
    """
    Display verify otp form.

    ** CONTEXT **
        ``form``
            verify_otp_form.
        ``phone_number``
            received from session.

    ** TEMPLATE **
        :template: `accounts/registration/verify_otp.html`

    :param: `request`
    """

    try:
        phone_number = request.session['phone_number']

        verify_otp_form = VerifyOtpForm(request.POST or None)

        if verify_otp_form.is_valid():
            _code = verify_otp_form.cleaned_data.get('code')
            hash_code = sha256(str(_code).encode('utf-8')).hexdigest()
            cached_code = cache.get(phone_number)
            phone_otp = PhoneOtp.objects.filter(phone=phone_number, code=cached_code)

            if hash_code == cached_code and phone_otp:
                # get user and authenticate
                try:
                    user = User.objects.get(username=phone_number)
                    login(request, user=user)
                    del request.session['phone_number']
                    return redirect(reverse('core:main_view'))
                except User.DoesNotExist:
                    return redirect(reverse('account:register'))
            else:
                messages.error(request, 'کد تائید اشتباه وارد شده است.')

        context = {
            'form': verify_otp_form,
            'phone_number': phone_number
        }
        return render(request, 'accounts/registration/verify_otp.html', context)
    except:
        raise Http404


@authenticated_user()
def register(request):
    """
    Display register form.

    ** CONTEXT **
        ``form``
            register_form
        ``phone_number``
            received from sessions

    ** TEMPLATE **
        :template: `accounts/registration/register.html`

    :param: `request`
    """

    try:
        phone_number = request.session['phone_number']
        register_form = RegisterForm(request.POST or None)

        if register_form.is_valid():
            cd = register_form.cleaned_data

            try:
                user = User.objects.get(username=phone_number)
                return redirect(reverse('core:main_view'))
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=phone_number, first_name=cd.get('first_name'), last_name=cd.get('last_name'),
                    email=cd.get('email'), is_customer=True, password=cd.get('password')
                )
                login(request, user=user)
                del request.session['phone_number']
                return redirect(reverse('core:main_view'))

        context = {
            'form': register_form,
            'phone_number': phone_number
        }
        return render(request, 'accounts/registration/register.html', context)
    except:
        raise Http404


class PasswordLogin(AuthenticatedUserMixin, LoginView):
    template_name = 'accounts/registration/password_login.html'
    form_class = PasswordLoginForm
