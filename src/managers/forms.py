from django import forms
from accounts.models import User


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
