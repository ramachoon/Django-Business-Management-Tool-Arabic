from django import forms
from captcha.fields import ReCaptchaField, ReCaptchaV3


class BaseCaptchaForm(forms.Form):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            api_params={'hl': 'fa'}
        ),
        error_messages={
            'required': 'این فیلد اجباری است.'
        }
    )
