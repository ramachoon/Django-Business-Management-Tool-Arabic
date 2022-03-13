import random
from hashlib import sha256

from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .forms import LoginForm, VerifyOtpForm
from accounts.models import PhoneOtp, User


# Create your views here.


def otp_login(request):
    login_form = LoginForm(request.POST or None)

    if login_form.is_valid():
        phone_number = login_form.cleaned_data.get('phone_number')
        _code = random.randint(111111, 999999)
        print(_code)
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


def verify_phone_otp(request):
    # raise http404, if http referer is not equal to login.
    if not request.META.get('HTTP_REFERER') == f"{request.scheme}://{request.get_host()}{reverse('account:login')}":
        raise Http404

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
            except User.DoesNotExist:
                raise Http404
        else:
            messages.error(request, 'کد تائید اشتباه وارد شده است.')

    context = {
        'form': verify_otp_form,
        'phone_number': phone_number
    }
    return render(request, 'accounts/registration/verify_otp.html', context)
