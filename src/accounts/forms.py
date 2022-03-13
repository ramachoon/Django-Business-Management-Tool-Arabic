import re
from django import forms


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-solid h-auto py-5 px-6', 'placeholder': 'شماره موبایل'
        }),
        help_text='شماره موبایل با 09 شروع شود',
        label='شماره موبایل'
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        regex = r"^[0-9]{2,}[0-9]$"
        subst = ""
        result = re.sub(regex, subst, phone_number, 0, re.MULTILINE)
        if len(phone_number) != 11 and not result:
            raise forms.ValidationError('شماره موبایل صحیح نمیباشد.')
        return phone_number
