from django import forms
from captcha.fields import ReCaptchaField


class BaseCaptchaForm(forms.Form):
    captcha = ReCaptchaField(    )
