import re
from django import forms
from src.extensions.shared_forms import BaseCaptchaForm
from accounts.models import User


class LoginForm(BaseCaptchaForm):
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-solid h-auto py-5 px-6', 'placeholder': 'شماره موبایل'
        }),
        help_text='شماره موبایل با 09 شروع شود',
        label='شماره موبایل',
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        regex = r"^[0-9]{2,}[0-9]$"
        subst = ""
        result = re.sub(regex, subst, phone_number, 0, re.MULTILINE)
        if len(phone_number) != 11 and not result:
            raise forms.ValidationError('شماره موبایل صحیح نمیباشد.')
        return phone_number


class VerifyOtpForm(BaseCaptchaForm):
    code = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-solid h-auto py-5 px-6', 'placeholder': 'کد تائید'
        }),
        label='کد تائید',
        min_length=4,
        max_length=4
    )


class RegisterForm(BaseCaptchaForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-solid h-auto py-5 px-6', 'placeholder': 'نام'
        }),
        label='نام'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-solid h-auto py-5 px-6', 'placeholder': 'نام خانوادگی'
        }),
        label='نام خانوادگی'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-solid h-auto py-5 px-6', 'placeholder': 'ایمیل'
        }),
        label='ایمیل'
    )


class UsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_customer', 'is_superuser',
            'is_employee', 'is_admin', 'is_supporter'
        )
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-solid form-control-lg', 'placeholder': 'شماره موبایل'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-solid form-control-lg', 'placeholder': 'ایمیل'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control form-control-solid form-control-lg', 'placeholder': 'نام'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control form-control-solid form-control-lg', 'placeholder': 'نام خانوادگی'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].required = False
        self.fields['is_customer'].required = False
        self.fields['is_superuser'].required = False
        self.fields['is_employee'].required = False
        self.fields['is_admin'].required = False
        self.fields['is_supporter'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
