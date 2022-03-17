import random
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_avatar

from src.extensions.upload_file_path import get_filename_ext


# Create your models here.
def upload_avatar_path(instance, filename):
    name, ext = get_filename_ext(filename)
    random_number = random.randint(1111111, 9999999)
    final_name = f"{random_number}-user-avatar-abdimt{ext}"
    return f"accounts/avatars/{final_name}"


class User(AbstractUser):
    """
    Customize user model.
    """

    bio = models.TextField(default='بیوگرافی خودرا ویرایش کنید', verbose_name='بیوگرافی')
    avatar = models.ImageField(
        upload_to=upload_avatar_path, default='accounts/avatars/default.jpg', validators=[validate_avatar],
        verbose_name='avatar'
    )
    is_employee = models.BooleanField(default=False, verbose_name='کارمند')
    is_customer = models.BooleanField(default=False, verbose_name='کارفرما')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_supporter = models.BooleanField(default=False, verbose_name='پشتیبان')

    def __str__(self):
        return self.get_full_name()


class PhoneOtp(models.Model):
    phone = models.CharField(max_length=13)
    code = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کد تائید'
        verbose_name_plural = 'کد تائید ها'

    def __str__(self):
        return f"{self.phone}"
