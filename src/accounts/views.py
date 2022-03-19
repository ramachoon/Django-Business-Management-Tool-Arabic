import random
from hashlib import sha256

from django.contrib.auth import login
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from src.extensions.sms_services import send_otp_sms
from .forms import LoginForm, VerifyOtpForm, RegisterForm
from accounts.models import PhoneOtp, User
from core.decorators import authenticated_user


# Create your views here.

@authenticated_user()
def otp_login(request):
    login_form = LoginForm(request.POST or None)

    if login_form.is_valid():
        phone_number = login_form.cleaned_data.get('phone_number')
        _code = random.randint(111111, 999999)
        send_otp_sms(phone_number, _code)
        hash_code = sha256(str(_code).encode('utf-8')).hexdigest()

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
    # raise http404, if http referer is not equal to login.
    # http_referer = request.META.get('HTTP_REFERER')
    # login_full_url = f"{request.scheme}://{request.get_host()}{reverse('account:login')}"
    # verify_otp_full_url = f"{request.scheme}://{request.get_host()}{reverse('account:verify_otp')}"
    # if not http_referer == login_full_url and not http_referer == verify_otp_full_url:
    #     raise Http404

    verify_otp_form = VerifyOtpForm(request.POST or None)
    phone_number = request.session['phone_number']

    if verify_otp_form.is_valid():
        _code = verify_otp_form.cleaned_data.get('code')
        hash_code = sha256(str(_code).encode('utf-8')).hexdigest()
        phone_otp = PhoneOtp.objects.filter(phone=phone_number, code=hash_code)
        # check phone_otp is exist and check the past moments.
        if phone_otp.exists() and \
                timezone.now().minute - phone_otp.first().updated.minute <= 5:
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


@authenticated_user()
def register(request):
    http_referer = request.META.get('HTTP_REFERER')
    verify_otp_full_url = f"{request.scheme}://{request.get_host()}{reverse('account:verify_otp')}"
    register_full_url = f"{request.scheme}://{request.get_host()}{reverse('account:register')}"
    if not http_referer == verify_otp_full_url and not http_referer == register_full_url:
        raise Http404

    register_form = RegisterForm(request.POST or None)
    phone_number = request.session['phone_number']

    if register_form.is_valid():
        cd = register_form.cleaned_data

        try:
            user = User.objects.get(username=phone_number)
            return redirect(reverse('core:main_view'))
        except User.DoesNotExist:
            user = User(
                username=phone_number, first_name=cd.get('first_name'), last_name=cd.get('last_name'),
                email=cd.get('email'), is_customer=True
            )
            user.save()
            login(request, user=user)
            del request.session['phone_number']
            return redirect(reverse('core:main_view'))

    context = {
        'form': register_form,
        'phone_number': phone_number
    }
    return render(request, 'accounts/registration/register.html', context)
